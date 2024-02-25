from django.shortcuts import render, redirect,get_object_or_404
from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages

from order.models import EventOrder
from schedule.models import EventProxy
from order.forms import CreateOrderForm


def create_order(request, event_id=None):
    event = get_object_or_404(EventProxy, id=event_id)

    if request.method == 'POST':
        form = CreateOrderForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    # event=Event.objects.filter(id=event_id).first()
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
                context = {
                    'title': 'Оформление заказа',
                    'form': form,
                    'event': event,
                }

                return render(request, 'order/create_order.html', context=context)
       
    form = CreateOrderForm()

    context = {
        'title': 'Оформление заказа',
        'form': form,
        'event': event,
    }

    return render(request, 'order/create_order.html', context=context)
