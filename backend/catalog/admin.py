from django.contrib import admin

from .models import Category, Route

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    ordering = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('name', ),
        } 

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'slug', 'price')
    list_filter = ('complexity', 'duration', 'price')
    ordering = ('category','complexity', 'duration', 'price')

    def get_prepopulated_fields(self, request, obj=None):
        return {
            'slug': ('name', ),
        } 