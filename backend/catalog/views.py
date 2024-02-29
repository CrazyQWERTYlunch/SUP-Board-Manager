"""
Модуль catalog предоставляет представления (views) для отображения маршрутов SUP.
"""

from django.shortcuts import render, get_object_or_404
from .models import Route
from schedule.models import EventProxy
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseServerError, Http404
from typing import Dict, Any


SUP_ROUTES_TITLE = 'SUP-Маршруты'


def apply_filters_to_routes(routes, category_id: int, complexity: str, duration: str, price: str, search_query: str):
    """
    Применяет фильтры к набору маршрутов.

    Args:
        routes: QuerySet маршрутов для фильтрации.
        category_id (int): ID категории для фильтрации.
        complexity (str): Сложность для фильтрации.
        duration (str): Продолжительность для фильтрации.
        price (str): Цена для фильтрации.
        search_query (str): Запрос для поиска маршрутов.

    Returns:
        QuerySet: Отфильтрованный QuerySet маршрутов.
    """
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
    return routes


def get_filtered_routes(request: HttpRequest) -> 'QuerySet[Route]':
    """
    Получает отфильтрованный набор маршрутов на основе параметров запроса.

    Args:
        request (HttpRequest): Запрос HTTP.

    Returns:
        QuerySet[Route]: Отфильтрованный набор маршрутов.
    """
    category_id = request.GET.get('category')
    complexity = request.GET.get('complexity')
    duration = request.GET.get('duration')
    price = request.GET.get('price')
    search_query = request.GET.get('search')
    routes = Route.objects.all()
    return apply_filters_to_routes(routes, category_id, complexity, duration, price, search_query)


def routes_view(request: HttpRequest) -> HttpResponse:
    """
    Представление для отображения списка маршрутов.

    Args:
        request (HttpRequest): HTTP запрос.

    Returns:
        HttpResponse: Ответ HTTP с отображением списка маршрутов.
    """
    try:
        routes = get_filtered_routes(request)
        context = {
            'title': SUP_ROUTES_TITLE,
            'routes': routes,
        }
        return render(request, 'catalog/routes.html', context=context)
    except Exception as e:
        return handle_exception(request, e)


def get_route_details(slug: str) -> Dict[str, Any]:
    """
    Получает информацию о маршруте и ближайших событиях для него.

    Args:
        slug (str): Строка, используемая для идентификации маршрута.

    Returns:
        Dict[str, Any]: Информация о маршруте и событиях.
    """
    route = get_object_or_404(Route, slug=slug)
    events_for_route = EventProxy.objects.filter(route=route, remaining_seats__gt=0).order_by('start')[:5] 
    return {
        'route': route,
        'events_for_route': events_for_route
    }


def route_detail_view(request: HttpRequest, slug: str) -> HttpResponse:
    """
    Представление для отображения деталей конкретного маршрута.

    Args:
        request (HttpRequest): HTTP запрос.
        slug (str): Строка, используемая для идентификации маршрута.

    Returns:
        HttpResponse: Ответ HTTP с отображением деталей маршрута.
    """
    try:
        context = {
            'title': 'Детали маршрута',
            **get_route_details(slug)
        }
        return render(request, 'catalog/route_detail.html', context=context)
    except Http404:
        return HttpResponseNotFound('Маршрут не найден')
    except Exception as e:
        return handle_exception(request, e)


def handle_exception(request: HttpRequest, exception: Exception) -> HttpResponse:
    """
    Обрабатывает исключение, возникшее при выполнении запроса.

    Args:
        request (HttpRequest): HTTP запрос.
        exception (Exception): Возникшее исключение.

    Returns:
        HttpResponse: Ответ HTTP с описанием ошибки.
    """
    return HttpResponseServerError('Произошла ошибка на сервере')

