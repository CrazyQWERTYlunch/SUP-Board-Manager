from django.db import models
from schedule.models import Event



# Здесь возможно стоит задуматься о переработке модели эвента, если добавлять сертификаты на какую-то более общую
class BaseOrder(models.Model):
    STATUS = (
        'Ждет подтверждения',
        'Подтвержден',
        'Выполнен',
        'Отменен'
              )
    # product = models.ForeignKey(to=Route, verbose_name='Имя')
    fullname = models.CharField(max_length=150, verbose_name='Имя')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')
    email = models.EmailField(verbose_name='Адрес почты')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')
    payment_by_card = models.BooleanField(default=False, verbose_name='Оплата картой')
    is_paid = models.BooleanField(default=False, verbose_name='Оплачено')
    status = models.CharField(max_length=18, default='В обработке', verbose_name='Статус заказа') # Связать со статусом
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания заказа')
    update_timestamp = models.DateTimeField(auto_now=True, verbose_name='Дата изменения заказа')


    def total_price(self):
        pass
    

    def __str__(self):
        return f'Заказ № {self.pk} | Покупатель {self.name}: {self.phone_number}'
    



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
    