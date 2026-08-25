from django.contrib import admin
from restaurants.models import Restaurant
from django.utils.html import format_html
from django.urls import reverse

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'owner_name', 'email', 'phone_number', 'is_verified', 'created_at')
    list_filter = ('is_verified',)
    search_fields = ('business_name', 'owner_name', 'email', 'phone_number')
    actions = ['approve_restaurants']
    
    
    change_form_template = 'admin/restaurants/restaurant/change_form.html'

    @admin.action(description='Approve selected restaurant partner accounts')
    def approve_restaurants(self, request, queryset):
        queryset.update(is_verified=True)
