from django.db import models
from catalog.models import Route, Category
from datetime import datetime

class Event(models.Model):
    STATUS = (
        'Предстоит',
        'Идёт',
        'Завершена',
    )
    category = models.ForeignKey(to=Category, default='SUP-прогулка', on_delete=models.CASCADE, verbose_name='Категория')
    route = models.ForeignKey(to=Route, on_delete=models.CASCADE, verbose_name='Маршрут') # limit_choices_to={"category": category} может стоит как-то добавить и ограничить
    price = models.DecimalField(default=0.00, max_digits=6, decimal_places=2, verbose_name='Цена') # ЧТо-то придумать
    total_seats = models.PositiveSmallIntegerField(verbose_name='Всего мест')
    remaining_seats = models.PositiveIntegerField(verbose_name='Осталось мест') 
    start = models.DateTimeField(null=True, blank=True, verbose_name='Начало прогулки')
    end = models.DateTimeField(null=True, blank=True, verbose_name='Конец прогулки')
    status = models.CharField(max_length=10, default='Предстоит', verbose_name='Статус события')
    
    class Meta:  
        db_table = 'tblevents'
        verbose_name = 'Прогулка'
        verbose_name_plural = 'Прогулки'



# class EventManager(models.Manager):
#     def get_queryset(self) -> models.QuerySet:
#         return super().get_queryset().filter(start__gt=datetime.now())
# # 
# class EventProxy(Event):

#     objects = EventManager()

#     class Meta:
#         proxy = True