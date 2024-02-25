from django.shortcuts import render, get_object_or_404

from .models import Route
from schedule.models import EventProxy
from django.utils import timezone

def routes_view(request):
    # try:
    # Получаем значения параметров фильтрации из запроса
    category_id = request.GET.get('category')
    complexity = request.GET.get('complexity')
    duration = request.GET.get('duration')
    price = request.GET.get('price')
    search_query = request.GET.get('search')

    routes = Route.objects.all()
    # Формируем фильтры для запроса
    if category_id:
        routes = routes.filter(category_id=category_id)

    if complexity:
        routes = routes.filter(complexity=complexity)

    if duration:
        routes = routes.filter(duration=duration)

    if price:
        if price == '1':
            routes = routes.filter(price__lte=1000)
        elif price == '2':
            routes = routes.filter(price__gte=1000, price__lte=5000)
        elif price == '3':
            routes = routes.filter(price__gte=5000)

    if search_query:
        routes = routes.filter(name__icontains=search_query)

    context = {
        'title': 'SUP-Маршруты',
        'routes': routes,
    }
    
    return render(request, 'catalog/routes.html', context=context)
    # except ObjectDoesNotExist:
    #     return HttpResponseNotFound('Страница не найдена')
    # except Exception as e:
    #     return HttpResponseServerError(f'Произошла ошибка: {str(e)}')


def route_detail_view(request, slug=False):
    """Представление отдельного маршрута"""
    
    route = get_object_or_404(Route, slug=slug)
    
    # Покажи ближайшие 5 событий с этим маршрутом на которые остались места  (срезом ограничиваем количество) 
    events_for_route = EventProxy.objects.filter(route=route, remaining_seats__gt=0).order_by('start')[:5] 
    
    context = {
        'title': route.name,
        'route': route,
        'events_for_route': events_for_route
    }

    return render(request, 'catalog/route_detail.html', context=context)
