from django.db import models
from django.utils.text import slugify
import random
import string
from django.urls import reverse


def rand_slug():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(3))

class Category(models.Model):
    """
    Модель представляет собой категорию услуги.

    Атрибуты модели:
        name (CharField): Название категории.
        slug (SlugField): URL-адрес категории, создается автоматически на основе названия.
        description (TextField): Описание услуги.
        image (ImageField): Изображение категории.
    """
    name = models.CharField(max_length=150, unique=True, verbose_name='Название') # db_index=True, - возможно стоит добавить
    slug = models.SlugField(max_length=150, unique=True, verbose_name='URL') # editable=True
    description = models.TextField(blank=True, null=True, verbose_name='Описание услуги')
    image = models.ImageField(upload_to='category_images', blank=True, null=True, verbose_name='Изображение')
    
    class Meta:
        unique_together = ('slug', )
        db_table = 'category'
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        """
        Возвращает строковое представление категории.

        Returns:
            str: Строковое представление категории.
        """
        return self.name
    
    def save(self, *args, **kwargs):
        """Переопределение метода для автоматической записи слага при создании не из админки"""
        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

    
class Route(models.Model):
    """
    Модель существующих маршрутов.

    Attributes:
        category (Category): Категория маршрута.
        name (str): Название маршрута.
        slug (str): URL-адрес маршрута, создается автоматически на основе названия.
        description (str): Описание маршрута.
        complexity (float): Сложность маршрута (значение от 0 до 10).
        duration (int): Продолжительность маршрута в минутах.
        distance (str): Протяженность маршрута.
        image (str): Изображение маршрута.
        price (float): Цена маршрута.
    """
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='Категория') # Может быть лучше будет SET_DEFAULT?
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание маршрута')
    complexity = models.DecimalField(default=5.00, max_digits=3, decimal_places=2, verbose_name="Сложность" ) # Возможно переделать, чтобы не проводить доп.действий
    duration = models.PositiveSmallIntegerField(verbose_name='Продолжительность')
    distance = models.CharField(max_length=50, verbose_name='Протяженность')
    image = models.ImageField(upload_to='route_images', blank=True, null=True, verbose_name='Изображение')
    price = models.DecimalField(default=0.00, max_digits=6, decimal_places=2, verbose_name='Цена маршрута')
    
    class Meta:
        db_table = 'route'
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ('id', )
    
    
    def __str__(self)-> str:
        """
        Возвращает строковое представление маршрута.

        Returns:
            str: Строковое представление маршрута.
        """
        return f'{self.name} - {self.price}'
    
    def get_absolute_url(self) -> str:
        """
        Получает абсолютный URL для маршрута.

        Returns:
            str: Абсолютный URL для маршрута.
        """
        return reverse("catalog:route", kwargs={"slug": self.slug})
    