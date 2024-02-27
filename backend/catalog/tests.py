"""
Модуль тестирования для приложения catalog.

Этот модуль содержит тесты для моделей, представлений и шаблонов в приложении catalog.
"""

from django.test import TestCase, Client
from .models import Category, Route
from django.urls import reverse
from django.template.loader import render_to_string

class CatalogModelsTestCase(TestCase):
    """
    Тесты для моделей приложения catalog.
    """

    def setUp(self):
        """
        Настройка тестов.

        Создает категорию для использования в тестах.
        """
        self.category = Category.objects.create(name='Test Category', slug='test-category')

    def test_category_creation(self):
        """
        Проверка создания категории.

        Создает категорию и проверяет корректность ее атрибутов.
        """
        category = Category.objects.get(slug='test-category')
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.slug, 'test-category')
        self.assertEqual(str(category), 'Test Category')

    def test_route_creation(self):
        """
        Проверка создания маршрута.

        Создает маршрут и проверяет корректность его атрибутов.
        """
        route = Route.objects.create(category=self.category, name='Test Route', slug='test-route', complexity=3, duration=120, distance='10 km')
        self.assertEqual(route.name, 'Test Route')
        self.assertEqual(route.slug, 'test-route')
        self.assertEqual(route.category, self.category)
        self.assertEqual(route.complexity, 3)
        self.assertEqual(route.duration, 120)
        self.assertEqual(route.distance, '10 km')
        self.assertEqual(str(route), 'Test Route - 0.0')


class CatalogViewsTestCase(TestCase):
    """
    Тесты для представлений приложения catalog.
    """
    def setUp(self):
        """
        Настройка тестов.

        Создает клиента для выполнения HTTP-запросов и создает объекты для тестирования представлений.
        """
        self.client = Client()
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.route = Route.objects.create(category=self.category, name='Test Route', slug='test-route', complexity=3, duration=120, distance='10 km')

    def test_routes_view(self):
        """
        Проверка представления списка маршрутов.

        Выполняет GET-запрос к представлению и проверяет корректность HTTP-ответа и использованного шаблона.
        """
        response = self.client.get(reverse('catalog:routes'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/routes.html')

    def test_route_detail_view(self):
        """
        Проверка представления деталей маршрута.

        Выполняет GET-запрос к представлению деталей маршрута и проверяет корректность HTTP-ответа и использованного шаблона.
        """
        response = self.client.get(reverse('catalog:route', kwargs={'slug': self.route.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/route_detail.html')
    
    def test_routes_view_with_filter(self):
        """
        Проверка фильтрации маршрутов в представлении списка маршрутов.

        Выполняет GET-запрос с фильтром к представлению списка маршрутов и проверяет корректность HTTP-ответа и использованного шаблона, а также соответствие отфильтрованных маршрутов выбранной категории.
        """
        response = self.client.get(reverse('catalog:routes'), {'category': self.category.id})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/routes.html')
        # Дополнительная проверка: убедимся, что отфильтрованные маршруты принадлежат выбранной категории
        filtered_routes = response.context['routes']
        for route in filtered_routes:
            self.assertEqual(route.category, self.category)

    def test_routes_view_with_search(self):
        """
        Проверка поиска маршрутов в представлении списка маршрутов.

        Выполняет GET-запрос с поиском к представлению списка маршрутов и проверяет корректность HTTP-ответа и использованного шаблона, а также наличие всех маршрутов в результате поиска.
        """
        response = self.client.get(reverse('catalog:routes'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/routes.html')
        # Дополнительная проверка: убедимся, что все маршруты возвращаются в результате поиска
        searched_routes = response.context['routes']
        self.assertIn(self.route, searched_routes)

    def test_route_detail_view_not_found(self):
        """
        Проверка отображения 404 ошибки при запросе несуществующего маршрута.

        Выполняет GET-запрос к представлению деталей несуществующего маршрута и проверяет корректность HTTP-ответа.
        """
        response = self.client.get(reverse('catalog:route', kwargs={'slug': 'non-existent-slug'}))
        self.assertEqual(response.status_code, 404)

class CatalogTemplateTestCase(TestCase):
    """
    Тесты для шаблонов приложения catalog.
    """
    def test_routes_template_exists(self):
        """
        Проверка существования шаблона routes.html.

        Загружает шаблон routes.html и проверяет, что он не является пустым.
        """
        rendered = render_to_string('catalog/routes.html')
        self.assertNotEqual(rendered, '')
