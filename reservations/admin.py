"""
Module that registers Admin configuration for Models:
- Tickets
- PurchasedTickets
"""
from django.contrib import admin
from .models import Tickets, PurchasedTickets


class TicketAdmin(admin.ModelAdmin):
    """ Admin configuration for the Ticket model """

    list_display = (
        'restaurant',
        'name',
        'max_purchase_count',
        'purchase_count',
        'soldout')
    search_fields = ('restaurant__name', 'name', 'code')
    ordering = (
        'restaurant',
        'name',
        'max_purchase_count',
        'purchase_count',
        'soldout')
    list_filter = ('soldout', )
    readonly_fields = ('soldout', 'code')


class PurchasedTicketsAdmin(admin.ModelAdmin):
    """ Admin Configuration of purchased tickets """

    list_display = ('id', 'guest_name', 'ticket')
    search_fields = ('guest_name', 'ticket')
    ordering = ('id', 'guest_name', 'ticket')


admin.site.register(Tickets, TicketAdmin)
admin.site.register(PurchasedTickets, PurchasedTicketsAdmin)
