from django.shortcuts import render, redirect, HttpResponseRedirect
from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages
from order.models import EventOrder
from schedule.models import Event
from order.forms import CreateOrderForm
from django.urls import reverse

# Create your views here.
def create_order(request, event_id=None):
    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    event=Event.objects.filter(id=event_id).first()
                    if event.remaining_seats < form.cleaned_data['quantity']:
                        raise ValidationError(f'На прогулке осталось {event.remaining_seats} мест')
                    
                    order = EventOrder.objects.create(
                        event=event,
                        fullname=form.cleaned_data['fullname'],
                        phone_number=form.cleaned_data['phone_number'],
                        email=form.cleaned_data['email'],
                        quantity=form.cleaned_data['quantity'],
                        payment_by_card=form.cleaned_data['payment_by_card'],
                    ) 

                    event.remaining_seats -= order.quantity
                    event.save()

                    messages.success(request, 'Заказ оформлен!')
                    return redirect('main:index')
            except ValidationError as e:
                messages.warning(request, e) # Исправить, чтобы высвечивалось и пользователю
                return redirect('schedule:index')                     
       
    form = CreateOrderForm()

    context = {
        'title': 'Оформление заказа',
        'form': form,
        'event': Event.objects.filter(id=event_id).first()

    }

    return render(request, 'order/create_order.html', context=context)
