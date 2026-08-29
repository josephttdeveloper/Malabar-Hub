from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    business_name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    owner_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    
    # KYC Details
    pan_card = models.CharField(max_length=50, blank=True, null=True)
    gst_number = models.CharField(max_length=50, blank=True, null=True)
    fssai_license = models.CharField(max_length=50, blank=True, null=True)
    bank_account = models.CharField(max_length=50, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)
    
    # KYC Document Uploads
    pan_document = models.FileField(upload_to='kyc_docs/', blank=True, null=True)
    gst_document = models.FileField(upload_to='kyc_docs/', blank=True, null=True)
    fssai_document = models.FileField(upload_to='kyc_docs/', blank=True, null=True)
    
    # Restaurant Section Images
    outside_view = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    inside_view = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    table_images = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    room_images = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    banquet_images = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    rooftop_images = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    bar_images = models.ImageField(upload_to='restaurant_images/', blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    is_accepting_orders = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.business_name)
            slug = base_slug
            while Restaurant.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{uuid.uuid4().hex[:6]}"
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.business_name} ({'Verified' if self.is_verified else 'Pending'})"


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ('starters', 'Starters / Appetizers'),
        ('main_course', 'Main Course'),
        ('beverages', 'Beverages'),
        ('desserts', 'Desserts'),
        ('snacks', 'Snacks'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='main_course')
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    is_veg = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.restaurant.business_name}"


class Space(models.Model):
    SPACE_TYPES = [
        ('table', 'Dining Table'),
        ('room', 'Hotel Room'),
        ('banquet', 'Banquet Hall'),
        ('rooftop', 'Rooftop Space'),
        ('bar', 'Bar Seating'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='spaces')
    name = models.CharField(max_length=100)
    space_type = models.CharField(max_length=50, choices=SPACE_TYPES, default='table')
    capacity = models.PositiveIntegerField(default=4)
    price_per_slot = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    image = models.ImageField(upload_to='spaces/', blank=True, null=True)
    is_available = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.get_space_type_display()}) - {self.restaurant.business_name}"


class Booking(models.Model):
    BOOKING_TYPES = [
        ('table', 'Table Booking'),
        ('room', 'Room Booking'),
        ('banquet', 'Banquet Booking'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE, null=True, blank=True)
    booking_type = models.CharField(max_length=20, choices=BOOKING_TYPES, default='table')
    booking_date = models.DateTimeField()
    
    checkin = models.DateField(blank=True, null=True)
    checkout = models.DateField(blank=True, null=True)
    
    guests_count = models.PositiveIntegerField(default=1)
    
    name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    extra_bed = models.BooleanField(default=False)
    payment_mode = models.CharField(max_length=50, blank=True, null=True)
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=50, default='Paid') # Added field
    status = models.CharField(max_length=50, default='Pending')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else (self.name or 'Guest')
        return f"{username} - {self.booking_type} at {self.restaurant.business_name}"


class HomeDeliveryOrder(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items_summary = models.TextField()
    delivery_address = models.TextField()
    phone = models.CharField(max_length=20)
    notes = models.TextField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Order Placed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.customer.username} from {self.restaurant.business_name}"