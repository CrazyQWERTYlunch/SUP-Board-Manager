from django.shortcuts import render, get_object_or_404

from .models import Category, Route
from schedule.models import EventProxy



def routes_view(request):
    # Стоит добавить фильтр

    routes = Route.objects.all() # Возможно стоит перекрутить на показ с категориями

    context = {
        'title': 'SUP-Маршруты',
        'routes': routes,
    }
    
    return render(request, 'catalog/routes.html', context=context)


def route_detail_view(request, slug=False):
    """Представление отдельного маршрута"""
    route = get_object_or_404(Route, slug=slug)
    data = EventProxy.objects.filter(route=route)

    context = {
        'title': route.name,
        'route': route,
        'data': data
    }

    return render(request, 'catalog/route_detail.html', context=context)


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    routes = Route.objects.select_related('category').filter(category=category)
    context = {
        'category': category,
        'routes': routes,
    }
    return render(request, 'catalog/category_list.html', context=context)