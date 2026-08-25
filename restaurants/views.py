from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.db.models import Q
from datetime import datetime
from .models import Restaurant, MenuItem, Space, Booking, HomeDeliveryOrder
from django.http import JsonResponse, HttpResponse



from .models import Restaurant, MenuItem, Space

def home_view(request):
    return render(request, 'home.html')

def get_started_view(request):
    """Allows user to choose whether they are registering as a Customer or a Partner."""
    return render(request, 'get_started.html')

def customer_register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('customer_register')

        user = User.objects.create_user(username=email, email=email, password=password, first_name=name)
        login(request, user)
        return redirect('customer_dashboard')
    
    return render(request, 'restaurants/customer_register.html')

def partner_register_view(request):
    if request.method == 'POST':
        business_name = request.POST.get('business_name')
        owner_name = request.POST.get('owner_name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('partner_register')

        if User.objects.filter(email=email).exists() or Restaurant.objects.filter(email=email).exists():
            messages.error(request, "An account with this email already exists.")
            return redirect('partner_register')

        
        user = User.objects.create_user(username=email, email=email, password=password, first_name=business_name)
        
        
        Restaurant.objects.create(
            user=user,
            business_name=business_name,
            owner_name=owner_name,
            email=email,
            phone_number=phone_number,
        is_verified=False  
    )
        
    
        login(request, user)
        messages.success(request, "Registration successful! Welcome to your Partner Dashboard.")
        return redirect('partner_dashboard')

    return render(request, 'restaurants/partner_register.html')


@login_required
def edit_restaurant_profile(request):
    try:
        restaurant = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        messages.error(request, "Restaurant profile not found.")
        return redirect('partner_dashboard')

    if request.method == 'POST':
        
        restaurant.business_name = request.POST.get('business_name', restaurant.business_name)
        restaurant.owner_name = request.POST.get('owner_name', restaurant.owner_name)
        restaurant.phone_number = request.POST.get('phone_number', restaurant.phone_number)
        
        restaurant.pan_card = request.POST.get('pan_card', restaurant.pan_card)
        restaurant.gst_number = request.POST.get('gst_number', restaurant.gst_number)
        restaurant.fssai_license = request.POST.get('fssai_license', restaurant.fssai_license)
        restaurant.bank_account = request.POST.get('bank_account', restaurant.bank_account)
        restaurant.ifsc_code = request.POST.get('ifsc_code', restaurant.ifsc_code)

        
        if request.FILES.get('pan_document'):
            restaurant.pan_document = request.FILES['pan_document']
        if request.FILES.get('gst_document'):
            restaurant.gst_document = request.FILES['gst_document']
        if request.FILES.get('fssai_document'):
            restaurant.fssai_document = request.FILES['fssai_document']

        
        if request.FILES.get('outside_view'):
            restaurant.outside_view = request.FILES['outside_view']
        if request.FILES.get('inside_view'):
            restaurant.inside_view = request.FILES['inside_view']
        if request.FILES.get('table_images'):
            restaurant.table_images = request.FILES['table_images']
        if request.FILES.get('room_images'):
            restaurant.room_images = request.FILES['room_images']
        if request.FILES.get('banquet_images'):
            restaurant.banquet_images = request.FILES['banquet_images']
        if request.FILES.get('rooftop_images'):
            restaurant.rooftop_images = request.FILES['rooftop_images']
        if request.FILES.get('bar_images'):
            restaurant.bar_images = request.FILES['bar_images']

        restaurant.save()
        messages.success(request, "Profile and KYC documents updated successfully!")
        return redirect('partner_dashboard')

    context = {'restaurant': restaurant}
    return render(request, 'restaurants/edit_profile.html', context)


@login_required
def manage_menu_view(request):
    try:
        restaurant = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        messages.error(request, "Restaurant profile not found.")
        return redirect('partner_dashboard')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        price = request.POST.get('price')
        category = request.POST.get('category')
        is_veg = request.POST.get('is_veg') == 'on'
        image = request.FILES.get('image')

        MenuItem.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            category=category,
            is_veg=is_veg,
            image=image
        )
        messages.success(request, f"'{name}' added to menu successfully!")
        return redirect('manage_menu')

    items = MenuItem.objects.filter(restaurant=restaurant)
    return render(request, 'restaurants/manage_menu.html', {'restaurant': restaurant, 'items': items})


@login_required
def delete_menu_item(request, item_id):
    item = MenuItem.objects.get(id=item_id, restaurant__user=request.user)
    item.delete()
    messages.success(request, "Menu item removed successfully.")
    return redirect('manage_menu')

@never_cache
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return redirect('/admin/')
            
            try:
                restaurant = Restaurant.objects.get(user=user)
                return redirect('partner_dashboard')
            except Restaurant.DoesNotExist:
                return redirect('customer_dashboard')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('login')

    return render(request, 'restaurants/login.html')


@login_required
def manage_spaces_view(request, space_type=None):
    try:
        restaurant = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        messages.error(request, "Restaurant profile not found.")
        return redirect('partner_dashboard')

    if not space_type:
        space_type = 'room'

    if request.method == 'POST':
        name = request.POST.get('name')
        stype = request.POST.get('space_type', space_type)
        capacity = request.POST.get('capacity')
        price_per_slot = request.POST.get('price_per_slot', 0.00)
        description = request.POST.get('description', '')
        
        
        seating_category = request.POST.get('seating_category', '')
        view_tag = request.POST.get('view_tag', '')
        
    
        image = request.FILES.get('image')
        
        
        extra_details = []
        if seating_category:
            extra_details.append(f"Category: {seating_category}")
        if view_tag:
            extra_details.append(f"View/Bed/Setup: {view_tag}")
        
        combined_description = " | ".join(extra_details)
        if description:
            combined_description = f"{combined_description} - {description}" if combined_description else description

        Space.objects.create(
            restaurant=restaurant,
            name=name,
            space_type=stype,
            capacity=capacity,
            price_per_slot=price_per_slot,
            image=image,  # Save the uploaded file here
            description=combined_description
        )
        
        messages.success(request, f"{stype.title()} '{name}' added successfully!")
        return redirect('manage_spaces_by_type', space_type=stype)

    spaces = Space.objects.filter(restaurant=restaurant, space_type=space_type)

    return render(request, 'restaurants/manage_spaces.html', {
        'restaurant': restaurant, 
        'spaces': spaces, 
        'selected_type': space_type
    })



def manage_delivery_view(request):
    try:
        restaurant = Restaurant.objects.get(user=request.user)
    except Restaurant.DoesNotExist:
        messages.error(request, "Please complete your restaurant profile first.")
        return redirect('edit_restaurant_profile')

    if request.method == 'POST':
        dish_name = request.POST.get('dish_name')
        category = request.POST.get('category', 'main_course')
        price = request.POST.get('price')
        
        # Map dietary tag from radio buttons/form
        dietary_tag = request.POST.get('dietary_tag', 'Veg')
        is_veg = True if dietary_tag.lower() == 'veg' else False

        MenuItem.objects.create(
            restaurant=restaurant,
            name=dish_name,
            category=category,
            price=price,
            is_veg=is_veg,
            is_available=True
        )
        messages.success(request, f"Successfully added '{dish_name}' to your delivery menu!")
        return redirect('manage_delivery')
    
    
    menu_items = MenuItem.objects.filter(restaurant=restaurant)
    
    context = {
        'menu_items': menu_items
    }
    return render(request, 'restaurants/manage_delivery.html', context)


@login_required
def delete_space(request, space_id):
    space = Space.objects.get(id=space_id, restaurant__user=request.user)
    space.delete()
    messages.success(request, "Space removed successfully.")
    return redirect('manage_spaces')



@never_cache
@login_required
def customer_dashboard_view(request):
    restaurants = Restaurant.objects.filter(is_verified=True)
    context = {
        'restaurants': restaurants,
        'customer_name': request.user.get_full_name() or request.user.username,
    }
    return render(request, 'restaurants/customer_dashboard.html', context)


@login_required
def customer_restaurant_view(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id, is_verified=True)
    menu_items = restaurant.menu_items.all()
    spaces = restaurant.spaces.all()
    
    context = {
        'restaurant': restaurant,
        'menu_items': menu_items,
        'spaces': spaces,
    }
    return render(request, 'restaurants/customer_restaurant_view.html', context)



@never_cache
@login_required
def customer_table_booking(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    spaces = Space.objects.filter(restaurant=restaurant, space_type='table')
    
    if request.method == 'POST':
        space_id = request.POST.get('space_id')
        guests = request.POST.get('guests', 1)
        booking_time = request.POST.get('booking_time')
        
        space = Space.objects.filter(id=space_id).first() if space_id else None
        
        Booking.objects.create(
            user=request.user,
            restaurant=restaurant,
            space=space,
            booking_type='table',
            booking_date=datetime.now(), 
            guests_count=int(guests)
        )
        messages.success(request, "Table booked successfully!")
        return redirect('customer_bookings')
    
    context = {
        'restaurant': restaurant,
        'spaces': spaces,
    }
    return render(request, 'restaurants/customer_table_booking.html', context)



@never_cache
@login_required
def customer_room_booking(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    spaces = Space.objects.filter(restaurant=restaurant, space_type='room')
    
    if request.method == 'POST':
        space_id = request.POST.get('space_id')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        guests = request.POST.get('guests', 2)
        
        
        booking_name = request.POST.get('booking_name')
        booking_phone = request.POST.get('booking_phone')
        extra_bed = True if request.POST.get('extra_bed') == 'on' else False
        payment_mode = request.POST.get('payment_mode')        
        advance_amount = request.POST.get('advance_amount')    
        payment_method = request.POST.get('roomPaymentMethod') 
        
        space = Space.objects.filter(id=space_id).first() if space_id else None
        
    
        
        Booking.objects.create(
            user=request.user,
            restaurant=restaurant,
            space=space,
            booking_type='room',
            booking_date=datetime.now(),
            guests_count=int(guests),
            name=booking_name,              
            phone=booking_phone,            
            extra_bed=extra_bed,            
            payment_mode=payment_mode,      
            paid_amount=advance_amount,
            payment_method=payment_method,  
                    
            
            status='Confirmed'
        )
        
        messages.success(request, f"Room reservation confirmed successfully! Advance paid: Rs. {advance_amount}")
        return redirect('customer_bookings')
    
    
    checkin_date = request.GET.get('checkin')
    checkout_date = request.GET.get('checkout')
    guest_count = request.GET.get('guests')
    
    
    room_types = request.GET.getlist('room_type')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by')
    has_ac = request.GET.get('has_ac')
    free_breakfast = request.GET.get('free_breakfast')
    extra_bed = request.GET.get('extra_bed')
    floor_pref = request.GET.get('floor_pref')

    if guest_count and hasattr(Space, 'capacity'):
        try:
            spaces = spaces.filter(capacity__gte=int(guest_count))
        except ValueError:
            pass

    if room_types and hasattr(Space, 'room_type'):
        spaces = spaces.filter(room_type__in=room_types)
        
    if max_price and hasattr(Space, 'price'):
        try:
            spaces = spaces.filter(price__lte=float(max_price))
        except ValueError:
            pass
            
    if has_ac == 'on' and hasattr(Space, 'has_ac'):
        spaces = spaces.filter(has_ac=True)
        
    if free_breakfast == 'on' and hasattr(Space, 'free_breakfast'):
        spaces = spaces.filter(free_breakfast=True)
        
    if extra_bed == 'on' and hasattr(Space, 'extra_bed_available'):
        spaces = spaces.filter(extra_bed_available=True)
        
    if floor_pref and hasattr(Space, 'floor'):
        spaces = spaces.filter(floor=floor_pref)

    if sort_by == 'price_asc' and hasattr(Space, 'price'):
        spaces = spaces.order_by('price')
    elif sort_by == 'price_desc' and hasattr(Space, 'price'):
        spaces = spaces.order_by('-price')

    context = {
        'restaurant': restaurant,
        'rooms': spaces,  
        'filters': request.GET,
        'checkin': checkin_date or '',
        'checkout': checkout_date or '',
        'guests': guest_count or '2',
    }
    return render(request, 'restaurants/customer_room_booking.html', context)

@never_cache
@login_required
def customer_banquet_booking(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    spaces = Space.objects.filter(restaurant=restaurant, space_type='banquet')
    
    if request.method == 'POST':
        space_id = request.POST.get('space_id')
        guests = request.POST.get('guests', 10)
        
        space = Space.objects.filter(id=space_id).first() if space_id else None
        
        Booking.objects.create(
            user=request.user,
            restaurant=restaurant,
            space=space,
            booking_type='banquet',
            booking_date=datetime.now(),
            guests_count=int(guests)
        )
        messages.success(request, "Banquet hall booked successfully!")
        return redirect('customer_bookings')
        
    context = {
        'restaurant': restaurant,
        'spaces': spaces,
    }
    return render(request, 'restaurants/customer_bookings.html' if False else 'restaurants/customer_banquet_booking.html', context)


login_required
def customer_home_delivery(request, restaurant_id):
  restaurant = get_object_or_404(Restaurant, id=restaurant_id)
  menu_items = MenuItem.objects.filter(restaurant=restaurant)

  if request.method == 'POST':
    address = request.POST.get('delivery_address')
    phone = request.POST.get('delivery_phone')
    notes = request.POST.get('delivery_notes', '')
    payment_method = request.POST.get('payment_method', 'UPI')
    cart_data = request.POST.get('cart_data')
    total_amount = request.POST.get('total_amount', 0)

    
    HomeDeliveryOrder.objects.create(
        customer=request.user,
        restaurant=restaurant,
        items_summary=cart_data,
        delivery_address=address,
        phone=phone,
        notes=notes,
        total_amount=total_amount,
        payment_method=payment_method,
    )

    messages.success(request, 'Home delivery order placed successfully!')
    return JsonResponse({'status': 'success'})

  context = {
      'restaurant': restaurant,
      'menu_items': menu_items,
  }
  return render(request, 'restaurants/customer_home_delivery.html', context)

@staff_member_required
def super_admin_dashboard_view(request):
    restaurants = Restaurant.objects.all()
    pending_restaurants = restaurants.filter(is_verified=False)
    
    
    if request.method == 'POST':
        action_type = request.POST.get('action_type')
        selected_ids = request.POST.getlist('selected_restaurants')
        
        if action_type == 'approve' and selected_ids:
            Restaurant.objects.filter(id__in=selected_ids).update(is_verified=True)
            return redirect('super_admin_dashboard')

    context = {
        'restaurants': restaurants,
        'pending_count': pending_restaurants.count(),
        'active_count': restaurants.filter(is_verified=True).count(),
    }
    return render(request, 'restaurants/admin_dashboard.html', context)



@never_cache
@login_required
def customer_bookings_view(request):
    table_bookings = Booking.objects.filter(user=request.user, booking_type='table')
    room_bookings = Booking.objects.filter(user=request.user, booking_type='room')
    banquet_bookings = Booking.objects.filter(user=request.user, booking_type='banquet')
    
    
    delivery_orders = HomeDeliveryOrder.objects.filter(customer=request.user).order_by('-created_at')
    

    context = {
        'table_bookings': table_bookings,
        'room_bookings': room_bookings,
        'banquet_bookings': banquet_bookings,
        'delivery_orders': delivery_orders, 
    }
    return render(request, 'restaurants/customer_bookings.html', context)


@never_cache
def partner_dashboard_view(request):
    return render(request, 'restaurants/partner_dashboard.html')

def partner_pending_view(request):
    return render(request, 'restaurants/partner_pending.html')

@never_cache
def logout_view(request):
    logout(request)
    request.session.flush()  
    messages.success(request, "Logged out successfully.")
    return redirect('home')

def custom_logout_view(request):
    logout(request)
    
    storage = messages.get_messages(request)
    storage.used = True
    return redirect('home') # or



@staff_member_required # Adjust to your admin auth check
def delete_restaurant(request, restaurant_id):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    
    
    
    
    restaurant_name = restaurant.business_name
    restaurant.delete()
    messages.success(request, f"Restaurant '{restaurant_name}' has been deleted successfully.")
    return redirect('super_admin_dashboard')



def password_reset_view(request):
    if request.method == 'POST':
        # You can render a success message or handle recovery logic here
        return render(request, 'password_reset_done.html')
    return render(request, 'password_reset.html')



@login_required
def manage_spaces_by_type(request, space_type):
    
    spaces = Space.objects.filter(restaurant=request.user.restaurant, space_type=space_type)
    return render(request, 'restaurants/manage_spaces.html', {'spaces': spaces, 'space_type': space_type})


@login_required
def cancel_table_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Table reservation cancelled successfully.")
    return redirect('customer_bookings')

@login_required
def cancel_room_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Room booking cancelled successfully.")
    return redirect('customer_bookings')

@login_required
def cancel_banquet_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Banquet hall booking cancelled successfully.")
    return redirect('customer_bookings')

@login_required
def cancel_delivery_order(request, order_id):
    
    order = get_object_or_404(HomeDeliveryOrder, id=order_id, customer=request.user)
    if request.method == 'POST':
        if order.status in ['Order Placed', 'Pending']:
            order.status = 'Cancelled'
            order.save()
            messages.success(request, "Home delivery order cancelled successfully.")
        else:
            messages.error(request, "Cannot cancel this order as preparation has already started.")
    return redirect('customer_bookings')
