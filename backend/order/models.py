from django.db import models
from schedule.models import Event


class BaseOrder(models.Model):
    """
    Абстрактная базовая модель заказа.

    Attributes:
        fullname (str): Имя заказчика.
        phone_number (str): Номер телефона заказчика.
        email (str): Адрес электронной почты заказчика.
        quantity (int): Количество заказанных товаров или услуг.
        payment_by_card (bool): Флаг оплаты картой.
        is_paid (bool): Флаг оплаченного заказа.
        status (str): Статус заказа (выбираемый из заданных вариантов).
        created_timestamp (datetime): Дата и время создания заказа.
        update_timestamp (datetime): Дата и время последнего обновления заказа.
    """

    STATUS = (
        ('Ждет подтверждения', 'Ждет подтверждения'),
        ('Подтвержден', 'Подтвержден'),
        ('Выполнен', 'Выполнен'),
        ('Отменен', 'Отменен'),
    )

    fullname = models.CharField(max_length=150, verbose_name='Имя')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Адрес почты')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')
    payment_by_card = models.BooleanField(default=False, verbose_name='Оплата картой')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=18, choices=STATUS, default='Ждет подтверждения', verbose_name='Статус заказа')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    update_timestamp = models.DateTimeField(auto_now=True, verbose_name='Дата изменения заказа')

    class Meta:
        abstract = True

    def total_price(self):
        """
        Вычисляет общую стоимость заказа.

        Returns:
            float: Общая стоимость заказа.
        """
        pass

    def __str__(self):
        return f'Заказ № {self.pk} | Покупатель {self.fullname}: {self.phone_number}'


class EventOrder(BaseOrder):
    """
    Модель заказа для конкретного события.

    Attributes:
        event (Event): Связанное событие (прогулка).
    """

    event = models.ForeignKey(to=Event, on_delete=models.CASCADE, verbose_name='Прогулка')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ\Прогулки'
        verbose_name_plural = 'Заказы\Прогулки'

    def total_price(self):
        """
        Вычисляет общую стоимость заказа на основе стоимости события и его количества.

        Returns:
            float: Общая стоимость заказа.
        """
        return round(self.event.price * self.quantity, 2)

    def __str__(self):
        return f'Прогулка : {self.event.route.name} | {self.event.start} |  Заказ № {self.pk}'