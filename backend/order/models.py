from django.db import models
from schedule.models import Event



class BaseOrder(models.Model):
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
        pass
    

    def __str__(self):
        return f'Заказ № {self.pk} | Покупатель {self.fullname}: {self.phone_number}'
    



class EventOrder(BaseOrder):
    event = models.ForeignKey(to=Event, on_delete=models.CASCADE, verbose_name='Прогулка')

    class Meta:
        db_table = 'order'
        verbose_name = 'Заказ\Прогулки'
        verbose_name_plural = 'Заказы\Прогулки'


    def total_price(self):
        return round(self.event.route.price * self.quantity, 2)

    def __str__(self):
        return f'Прогулка : {self.event.route.name} | {self.event.start} |  Заказ № {self.pk}'    