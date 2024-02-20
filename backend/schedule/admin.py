from django.contrib import admin

from .models import Event 


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['route_display', 'date', 'start', 'end', 'remaining_seats', 'total_seats', 'status']
    list_filter = ['date', 'status']


    def route_display(self, obj):
        return str(obj.route.name)