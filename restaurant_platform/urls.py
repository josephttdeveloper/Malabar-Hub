from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from restaurants import views

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
    
    # Unified space routing mapping to manage_spaces_view
    path('partner/spaces/<str:space_type>/', views.manage_spaces_view, name='manage_spaces_by_type'),
    path('partner/spaces/', views.manage_spaces_view, name='manage_spaces'),
    path('partner/spaces/delete/<int:space_id>/', views.delete_space, name='delete_space'),
    
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
    path('super-admin/login/', views.super_admin_login_view, name='super_admin_login'),
    path('partner/revenue-report/', views.partner_revenue_report_view, name='partner_revenue_report'),
    path('partner/delivery/toggle-pause/', views.toggle_pause_orders, name='toggle_pause_orders'),
    path('partner/delivery/item/toggle/<int:item_id>/', views.toggle_menu_item, name='toggle_menu_item'),
    path('partner/delivery/orders/', views.partner_delivery_orders_view, name='partner_delivery_orders'), 
    path('partner/bookings/', views.partner_bookings_view, name='partner_bookings'),
    path('partner/settings/', views.partner_settings_view, name='partner_settings'),
    path('partner/bookings/confirm/<int:booking_id>/', views.confirm_partner_booking, name='confirm_partner_booking'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)