from django.shortcuts import render

from .models import Event

def index(request, category_slug=None):

    if category_slug == 'all':
        events = Event.objects.all()





    all_events = Event.objects.all()
    context = {
        'title': 'Расписание',
        'events': all_events,
    }
    return render(request,'shedule/demo.html', context=context)