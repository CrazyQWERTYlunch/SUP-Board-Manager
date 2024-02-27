from typing import Any, Dict
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.forms import ValidationError
from django.contrib import messages
from django.http import Http404
from django.utils import timezone

from order.models import EventOrder
from schedule.models import EventProxy
from order.forms import CreateOrderForm


def create_order(request, event_id: int = None) -> Any:
    """
    Отображает форму оформления заказа для указанного мероприятия.

    Args:
        request (HttpRequest): Объект HttpRequest, представляющий запрос.
        event_id (int, optional): ID мероприятия. По умолчанию None.

    Returns:
        HttpResponse: Возвращает отрендеренный шаблон или ответ перенаправления.

    Raises:
        Http404: Если мероприятие уже началось.

    """
    event = get_object_or_404(EventProxy, id=event_id)

    if event.start < timezone.now():
        raise Http404("Это мероприятие уже прошло и больше недоступно для заказа.")

    form = CreateOrderForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        try:
            with transaction.atomic():
                create_order_instance(event, form.cleaned_data)
                messages.success(request, 'Ваш заказ оформлен успешно!')
                return redirect('main:index')
        except ValidationError as e:
            messages.warning(request, e)

    context: Dict[str, Any] = {'title': 'Оформление заказа', 'form': form, 'event': event}
    return render(request, 'order/create_order.html', context=context)


def create_order_instance(event: EventProxy, cleaned_data: Dict[str, Any]) -> None:
    """
    Создает экземпляр EventOrder на основе предоставленных данных.

    Args:
        event (EventProxy): Мероприятие, для которого создается заказ.
        cleaned_data (Dict[str, Any]): Очищенные данные формы.

    Raises:
        ValidationError: Если для мероприятия недостаточно свободных мест.

    """
    if event.remaining_seats < cleaned_data['quantity']:
        raise ValidationError(f'На прогулке осталось {event.remaining_seats} мест.')

    order = EventOrder.objects.create(
        event=event,
        fullname=cleaned_data['fullname'],
        phone_number=cleaned_data['phone_number'],
        email=cleaned_data['email'],
        quantity=cleaned_data['quantity'],
        payment_by_card=cleaned_data['payment_by_card'],
    )

    event.remaining_seats -= order.quantity
    event.save()
