# from django.shortcuts import render, get_list_or_404
# from datetime import datetime 
# from .models import EventProxy
# from django.db.models import Q
# from .models import EventProxy
# from django.db.models import Q

# def index(request, category_slug=None):
#     # category_slug = request.GET.get('category_slug')
#     # Получаем параметры фильтрации из GET-запроса
#     # day = request.GET.get('day')
#     # time = request.GET.get('time')

#     # # Фильтрация событий по выбранному дню
#     # if day:
#     #     events = EventProxy.objects.filter(start__date=day)
#     # else:
#     #     events = EventProxy.objects.all()

#     # # Фильтрация событий по выбранному времени
#     # category_slug = request.GET.get('category_slug')
#     # Получаем параметры фильтрации из GET-запроса
#     # day = request.GET.get('day')
#     # time = request.GET.get('time')

#     # # Фильтрация событий по выбранному дню
#     # if day:
#     #     events = EventProxy.objects.filter(start__date=day)
#     # else:
#     #     events = EventProxy.objects.all()

#     # # Фильтрация событий по выбранному времени
#     # if time:
#     #     events = events.filter(start__time=time)

#     # Если выбрана категория, фильтруем события по этой категории
#     # if category_slug == 'all' or category_slug is None:
#     #     events = EventProxy.objects.all()
#     # else:
#     #     events = EventProxy.objects.filter(category__slug=category_slug)

#     if category_slug == 'all' or category_slug is None:
#         events = EventProxy.objects.all().select_related('category')
#     else:
#         events = EventProxy.objects.filter(category__slug=category_slug).select_related('category')



#     # Сортировка событий по времени начала
#     events = events.order_by('start')

#     context = {
#         'title': 'Расписание',
#         'events': events,
#         'slug_url': category_slug,
#     }
#     return render(request, 'shedule/demo.html', context=context)
# from django.shortcuts import render
# from .models import EventProxy
# from datetime import time




from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.db.models.query import QuerySet
from .models import EventProxy


def index(request) -> HttpResponse:
    """
    Отображает страницу с расписанием событий.

    Parameters:
        request (HttpRequest): HTTP-запрос.

    Returns:
        HttpResponse: HTTP-ответ с HTML-содержимым страницы расписания.

    Raises:
        ValidationError: Если параметры запроса недопустимы.
        Exception: Если произошла неизвестная ошибка.

    """
    try:
        category_slug = request.GET.get('category')
        time_start = request.GET.get('time_start')
        time_end = request.GET.get('time_end')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')

        events = get_filtered_events(category_slug, time_start, time_end, min_price, max_price)

        context = {
            'title': 'Расписание',
            'events': events,
            'category_slug': category_slug,
            'time_start': time_start,
            'time_end': time_end,
            'min_price': min_price,
            'max_price': max_price,
        }
        return render(request, 'shedule/demo.html', context=context)
    except Exception as e:
        error_message = "Произошла ошибка: {}".format(str(e))
        return HttpResponseServerError(error_message)


def get_filtered_events(category_slug: str, time_start: str, time_end: str, min_price: str, max_price: str) -> QuerySet[EventProxy]:
    """
    Фильтрует события на основе предоставленных параметров.

    Parameters:
        category_slug (str): Слаг категории для фильтрации.
        time_start (str): Время начала для фильтрации.
        time_end (str): Время окончания для фильтрации.
        min_price (str): Минимальная цена для фильтрации.
        max_price (str): Максимальная цена для фильтрации.

    Returns:
        QuerySet[EventProxy]: Отфильтрованный набор данных событий.

    """
    events = EventProxy.objects.all().select_related('category')

    if category_slug and category_slug != 'all':
        events = events.filter(category__slug=category_slug)

    if time_start and time_end:
        events = filter_events_by_time(events, time_start, time_end)

    if min_price:
        events = events.filter(route__price__gte=min_price)
    if max_price:
        events = events.filter(route__price__lte=max_price)

    return events.order_by('start')


def filter_events_by_time(events: QuerySet[EventProxy], time_start: str, time_end: str) -> QuerySet[EventProxy]:
    """
    Фильтрует события по времени.

    Parameters:
        events (QuerySet[EventProxy]): Набор данных событий для фильтрации.
        time_start (str): Начальное время интервала для фильтрации.
        time_end (str): Конечное время интервала для фильтрации.

    Returns:
        QuerySet[EventProxy]: Отфильтрованный набор данных событий по времени.

    """
    if time_start and time_end is not None:
        if time_end < time_start:
            events = events.filter(start__time__gte=time_start) | events.filter(start__time__lte=time_end)
        else:
            events = events.filter(start__time__gte=time_start, start__time__lte=time_end)
    return events