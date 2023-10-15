from django.contrib import admin
from .models import *

class TicketAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'name', 'maxPurchaseCount', 'purchaseCount', 'soldout' )
    search_fields = ( 'restaurant__name', 'name', 'code')
    ordering = ('restaurant', 'name', 'maxPurchaseCount', 'purchaseCount', 'soldout' )
    list_filter = ( 'soldout' )
    readonly_fields = ( 'soldout','code' )

class PurchasedTicketsAdmin(admin.ModelAdmin):
    list_display = ('id', 'guestName', 'ticket')
    search_fields = ( 'guestName', 'ticket')
    ordering = ('id','guestName', 'ticket')

admin.site.register(Tickets, TicketAdmin)
admin.site.register(PurchasedTickets, PurchasedTicketsAdmin)