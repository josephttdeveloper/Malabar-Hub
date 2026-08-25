from django.contrib import admin
from django.urls import path
<<<<<<< HEAD
from django.conf import settings
from django.conf.urls.static import static
from restaurants import views
=======
from restaurants.views import super_admin_dashboard_view
from restaurants.views import (
    home_view, 
    get_started_view, 
    customer_register_view, 
    partner_register_view, 
    login_view, 
    customer_dashboard_view, 
    partner_dashboard_view, 
    partner_pending_view,
    logout_view,
    edit_restaurant_profile,
    manage_menu_view,
    delete_menu_item,
    manage_spaces_view,
    delete_space,
    manage_delivery_view,
    customer_restaurant_view,
    customer_table_booking, 
    customer_room_booking,
    customer_banquet_booking,
    customer_home_delivery,
    customer_bookings_view, 
    super_admin_dashboard_view,
    delete_restaurant,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('get-started/', get_started_view, name='get_started'),
    path('register/customer/', customer_register_view, name='customer_register'),
    path('register/partner/', partner_register_view, name='partner_register'),
    path('login/', login_view, name='login'),
    path('customer/dashboard/', customer_dashboard_view, name='customer_dashboard'),
    path('partner/dashboard/', partner_dashboard_view, name='partner_dashboard'),
    path('partner/pending/', partner_pending_view, name='partner_pending'),
    path('logout/', logout_view, name='logout'),
    path('partner/profile/edit/', edit_restaurant_profile, name='edit_restaurant_profile'),
    path('partner/menu/', manage_menu_view, name='manage_menu'),
    path('partner/menu/delete/<int:item_id>/', delete_menu_item, name='delete_menu_item'),

    path('partner/spaces/', manage_spaces_view, name='manage_spaces'),
    path('partner/spaces/delete/<int:space_id>/', delete_space, name='delete_space'),
    path('partner/spaces/<str:space_type>/', manage_spaces_view, name='manage_spaces_by_type'),
    path('partner/delivery/manage/', manage_delivery_view, name='manage_delivery'),
    
    
    path('customer/restaurant/<int:restaurant_id>/', customer_restaurant_view, name='customer_restaurant_view'),
    path('customer/restaurant/<int:restaurant_id>/table-booking/', customer_table_booking, name='customer_table_booking'),
    path('customer/restaurant/<int:restaurant_id>/room-booking/', customer_room_booking, name='customer_room_booking'),
    path('customer/restaurant/<int:restaurant_id>/banquet-booking/', customer_banquet_booking, name='customer_banquet_booking'),
    path('customer/restaurant/<int:restaurant_id>/home-delivery/', customer_home_delivery, name='customer_home_delivery'),
    path('super-admin/dashboard/', super_admin_dashboard_view, name='super_admin_dashboard'),
    path('customer/bookings/', customer_bookings_view, name='customer_bookings'),
    path('super-admin/delete-restaurant/<int:restaurant_id>/', delete_restaurant, name='delete_restaurant'),
]
>>>>>>> 03043805c53f36e9bdfa07b943138b22ea8ff7af

urlpatterns = [
    
    path('', views.home_view, name='home'),
    path('explore/', views.get_started_view, name='get_started'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('password-reset/', views.password_reset_view, name='password_reset'),

    
    path('customer/register/', views.customer_register_view, name='customer_register'),
    path('partner/register/', views.partner_register_view, name='partner_register'),

    path('admin/', admin.site.urls),

    
    path('customer/dashboard/', views.customer_dashboard_view, name='customer_dashboard'),
    path('partner/dashboard/', views.partner_dashboard_view, name='partner_dashboard'),
    path('partner/pending/', views.partner_pending_view, name='partner_pending'),
    path('super-admin/dashboard/', views.super_admin_dashboard_view, name='super_admin_dashboard'),

    
    path('partner/profile/edit/', views.edit_restaurant_profile, name='edit_restaurant_profile'),
    path('partner/menu/', views.manage_menu_view, name='manage_menu'),
    path('partner/menu/delete/<int:item_id>/', views.delete_menu_item, name='delete_menu_item'),
    path('partner/spaces/', views.manage_spaces_view, name='manage_spaces'),
    path('partner/spaces/delete/<int:space_id>/', views.delete_space, name='delete_space'),
    path('partner/spaces/<str:space_type>/', views.manage_spaces_by_type, name='manage_spaces_by_type'),
    path('partner/delivery/manage/', views.manage_delivery_view, name='manage_delivery'),

    
    path('customer/restaurant/<int:restaurant_id>/', views.customer_restaurant_view, name='customer_restaurant_view'),
    path('customer/restaurant/<int:restaurant_id>/table-booking/', views.customer_table_booking, name='customer_table_booking'),
    path('customer/restaurant/<int:restaurant_id>/room-booking/', views.customer_room_booking, name='customer_room_booking'),
    path('customer/restaurant/<int:restaurant_id>/banquet-booking/', views.customer_banquet_booking, name='customer_banquet_booking'),
    path('customer/restaurant/<int:restaurant_id>/home-delivery/', views.customer_home_delivery, name='customer_home_delivery'),
    path('customer/bookings/', views.customer_bookings_view, name='customer_bookings'),

    
    path('super-admin/delete-restaurant/<int:restaurant_id>/', views.delete_restaurant, name='delete_restaurant'),

    
    path('cancel-table/<int:booking_id>/', views.cancel_table_booking, name='cancel_table_booking'),
    path('cancel-room/<int:booking_id>/', views.cancel_room_booking, name='cancel_room_booking'),
    path('cancel-banquet/<int:booking_id>/', views.cancel_banquet_booking, name='cancel_banquet_booking'),
    path('cancel-delivery/<int:order_id>/', views.cancel_delivery_order, name='cancel_delivery_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
