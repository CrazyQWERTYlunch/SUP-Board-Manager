from django.db import models
from catalog.models import Route

class Event(models.Model):

    route = models.ForeignKey(to=Route, on_delete=models.CASCADE, verbose_name='Маршрут')
    # name = models.CharField(max_length=255,null=True,blank=True)
    total_seats = models.PositiveSmallIntegerField(verbose_name='Количество мест')
    remaining_seats = models.PositiveIntegerField(verbose_name='Осталось мест')
    # date = models.DateField(verbose_name='Дата') # Возможно стоит объединить со стартом 
    start = models.DateTimeField(null=True, blank=True, verbose_name='Начало')
    end = models.DateTimeField(null=True, blank=True, verbose_name='Конец')
    status = models.CharField(max_length=50, default='Предстоит', verbose_name='Статус события')
    
    class Meta:  
        db_table = 'tblevents'
        verbose_name = 'Прогулка'
        verbose_name_plural = 'Прогулки'