from django.contrib import admin

from order.models import EventOrder


from datetime import datetime

@admin.register(EventOrder)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'event_id',
        'display_route',
        'fullname',
        'display_date',
        'status',
        'total_price',
        'is_paid',
        'update_timestamp',
        'total_price',
    )

    list_filter = ('status', 'is_paid', 'fullname')


    def display_date(self, obj):
        return obj.event.start.strftime('%d%h%m')
    

    def display_route(self, obj):
        return str(obj.event.route.name)
    