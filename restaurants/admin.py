from django.contrib import admin
from .models import *

class RestauranteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'owner' )
    search_fields = ( 'name', 'owner')
    ordering = ('id', 'name', 'owner' )
    list_filter = ( 'owner')

admin.site.register(Restaurant, RestauranteAdmin)