from datetime import timedelta, date
from django.db import models
from django.utils import timezone
from catalog.models import Route, Category

class Event(models.Model):
    """
    Модель для представления событий.

    Представляет информацию о проводимых мероприятиях, их статусе, категории, маршруте, цене, доступных местах и времени начала и конца.
    """
    STATUS_CHOICES = (
        ('Предстоит', 'Предстоит'),
        ('Идёт', 'Идёт'),
        ('Завершен', 'Завершен'),
        ('Отменен', 'Отменен'),
    )
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, default=None, verbose_name='Категория')
    route = models.ForeignKey(to=Route, on_delete=models.CASCADE,default=None, verbose_name='Маршрут')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Предстоит', verbose_name='Статус события')
    price = models.DecimalField(default=0.00, max_digits=6, decimal_places=2, verbose_name='Цена')
    total_seats = models.PositiveSmallIntegerField(verbose_name='Всего мест', default=0)
    remaining_seats = models.PositiveIntegerField(verbose_name='Осталось мест', default=0) 
    start = models.DateTimeField(null=True, blank=True, verbose_name='Начало прогулки')
    end = models.DateTimeField(null=True, blank=True, verbose_name='Конец прогулки')
    
    class Meta:  
        db_table = 'tblevents'
        verbose_name = 'Прогулка'
        verbose_name_plural = 'Прогулки'

    def save(self, *args, **kwargs) -> None:
        """
        Метод сохранения события.

        Перед сохранением события убеждаемся, что поля start и end содержат информацию о часовом поясе.
        """
        if self.start is not None and timezone.is_naive(self.start):
            self.start = timezone.make_aware(self.start, timezone.get_current_timezone())
        if self.end is not None and timezone.is_naive(self.end):
            self.end = timezone.make_aware(self.end, timezone.get_current_timezone())
        super().save(*args, **kwargs)


    def __str__(self) -> str:
        """
        Возвращает строковое представление события.

        Returns:
            str: Строковое представление события.
        """
        return f'{self.route.name}: {self.start}'


class EventManager(models.Manager):
    def get_queryset(self, weeks: int = 2) -> models.QuerySet:
        """
        Метод для получения ближайших событий.

        :param weeks: количество недель для фильтрации событий (по умолчанию 2 недели)
        """
        start_date: date = timezone.now().date()
        end_date: date = start_date + timedelta(weeks=weeks)
        return super().get_queryset().filter(start__range=(start_date, end_date))


class EventProxy(Event):

    objects: EventManager = EventManager()

    class Meta:
        proxy: bool = True