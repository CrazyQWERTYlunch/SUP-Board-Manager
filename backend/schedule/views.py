from django.shortcuts import render, get_list_or_404
from datetime import datetime 
from .models import EventProxy
from django.db.models import Q
from .models import EventProxy
from django.db.models import Q

def index(request, category_slug=None):
    # category_slug = request.GET.get('category_slug')
    # Получаем параметры фильтрации из GET-запроса
    # day = request.GET.get('day')
    # time = request.GET.get('time')

    # # Фильтрация событий по выбранному дню
    # if day:
    #     events = EventProxy.objects.filter(start__date=day)
    # else:
    #     events = EventProxy.objects.all()

    # # Фильтрация событий по выбранному времени
    # category_slug = request.GET.get('category_slug')
    # Получаем параметры фильтрации из GET-запроса
    # day = request.GET.get('day')
    # time = request.GET.get('time')

    # # Фильтрация событий по выбранному дню
    # if day:
    #     events = EventProxy.objects.filter(start__date=day)
    # else:
    #     events = EventProxy.objects.all()

    # # Фильтрация событий по выбранному времени
    # if time:
    #     events = events.filter(start__time=time)

    # Если выбрана категория, фильтруем события по этой категории
    # if category_slug == 'all' or category_slug is None:
    #     events = EventProxy.objects.all()
    # else:
    #     events = EventProxy.objects.filter(category__slug=category_slug)

    if category_slug == 'all' or category_slug is None:
        events = EventProxy.objects.all().select_related('category')
    else:
        events = EventProxy.objects.filter(category__slug=category_slug).select_related('category')



    # Сортировка событий по времени начала
    events = events.order_by('start')

    context = {
        'title': 'Расписание',
        'events': events,
        'slug_url': category_slug,
    }
    return render(request, 'shedule/demo.html', context=context)
    return render(request, 'shedule/demo.html', context=context)