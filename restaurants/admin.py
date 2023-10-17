"""
Module that registers Admin configuration for Models:
- Restaurant
"""
from django.contrib import admin
from .models import Restaurant


class RestaurantAdmin(admin.ModelAdmin):
    """ Admin configuration for Restaurant's Model """
    list_display = ('id', 'name', 'owner')
    search_fields = ('name',)
    ordering = ('id', 'name', 'owner')
    list_filter = ('owner',)


admin.site.register(Restaurant, RestaurantAdmin)
