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

    Пример использования:
        Создание объекта категории:
        >>> from catalog.models import Category
        >>> cat = Category.objects.create(name='Название категории', description='Описание категории')

        Получение всех категорий:
        >>> categories = Category.objects.all()
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
        return self.name
    
    def save(self, *args, **kwargs):
        """Переопределение метода для автоматической записи слага при создании не из админки"""
        if not self.slug:
            self.slug = slugify(rand_slug() + '-pickBetter' + self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("catalog:category", kwargs={"category_slug": self.slug})
    
class Route(models.Model):
    """
    Модель существующих маршрутов
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
    # status = 

    class Meta:
        db_table = 'route'
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'
        ordering = ('id', )
    
    
    def __str__(self):
        return f'{self.name} - {self.price}'
    
    def get_absolute_url(self):
        return reverse("catalog:route", kwargs={"slug": self.slug})
    

    # Прокси и менеджер модели
    # Возможно их стоит добавлять в эвентовые события

# class RouteManager(models.Manager):
#     def get_queryset(self) -> models.QuerySet:
#         return super(ProductManager, self).get_queryset().filter(status=True)

# class RouteProxy(Route):

#     # Переопределили метод
#     objects = ProductManager()

#     class Meta:
#         proxy = True