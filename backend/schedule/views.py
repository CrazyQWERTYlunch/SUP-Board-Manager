from django.shortcuts import render, get_list_or_404
from datetime import datetime 
from .models import Event

def index(request, category_slug=None):
    # Реализация фильтров
    # Попытаться потом реализовать
    # time = request.Get.get('time', None)

    if category_slug == 'all' or category_slug is None: # пока оставляем этот костылик
        events = Event.objects.all()
    else:
        events = get_list_or_404(Event.objects.filter(category__slug=category_slug))



    # if time:
    #     time = datetime(time)
    #     events = events.filter(start__lt=time)



    # events = Event.objects.all()
    context = {
        'title': 'Расписание',
        'events': events,
        'slug_url': category_slug,
    }
    return render(request,'shedule/demo.html', context=context)