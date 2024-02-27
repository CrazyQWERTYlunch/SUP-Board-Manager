from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from .models import Event
from catalog.models import Category, Route
from datetime import timedelta


class ScheduleModelsTestCase(TestCase):
    """
    Тесты моделей приложения расписания.
    """

    def setUp(self):
        """
        Настройка тестовых данных перед каждым тестом.
        """
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.route = Route.objects.create(category=self.category, name='Test Route', slug='test-route', complexity=3, duration=120, distance='10 km')
        self.start = timezone.now()
        self.event = Event.objects.create(category=self.category, route=self.route, status='Предстоит', price=0.00, total_seats=100, remaining_seats=100, start=self.start, end=self.start + timedelta(hours=2))

    def test_event_creation(self):
        """
        Тест создания события.
        """
        self.assertEqual(self.event.status, 'Предстоит')
        self.assertEqual(self.event.price, 0.00)
        self.assertEqual(self.event.total_seats, 100)
        self.assertEqual(self.event.remaining_seats, 100)
        self.assertEqual(
            str(self.event),
            f'Test Route: {self.start}'
        )


class ScheduleViewsTestCase(TestCase):
    """
    Тесты представлений приложения расписания.
    """

    def setUp(self):
        """
        Настройка тестовых данных перед каждым тестом.
        """
        self.client = Client()
        self.category = Category.objects.create(
            name='Test Category', slug='test-category')
        self.category2 = Category.objects.create(
            name='Test Category 2', slug='test-category-2')
        self.route = Route.objects.create(
            category=self.category,
            name='Test Route',
            slug='test-route',
            complexity=3,
            duration=120,
            distance='10 km'
        )
        self.route2 = Route.objects.create(
            category=self.category2,
            name='Test Route 2',
            slug='test-route-2',
            complexity=3,
            duration=120,
            distance='10 km'
        )

        self.start_time = timezone.now() + timedelta(hours=1)
        self.end_time = self.start_time + timedelta(hours=2)
        self.event = Event.objects.create(
            category=self.category, route=self.route,
            start=self.start_time, end=self.end_time
        )
        self.event2 = Event.objects.create(
            category=self.category2, route=self.route2,
            start=self.start_time, end=self.end_time
        )

    def test_index_view(self):
        """
        Тест представления index.
        """
        response = self.client.get(reverse('schedule:index'))
        self.assertEqual(response.status_code, 200)

    def test_filtered_events(self):
        """
        Тест фильтрации событий по категории.
        """
        response = self.client.get(reverse('schedule:index'), {'category': 'test-category'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('events', response.context)
        filtered_events = response.context['events']
        for event in filtered_events:
            self.assertEqual(event.category, self.category)
            self.assertEqual(event.route, self.route)

    def test_time_filtering(self):
        """
        Тест фильтрации событий по времени.
        """
        response = self.client.get(reverse('schedule:index'), {'time_start': self.start_time.strftime('%H:%M'), 'time_end': self.end_time.strftime('%H:%M')})
        self.assertEqual(response.status_code, 200)
        self.assertIn('events', response.context)
        filtered_events = response.context['events']
        for event in filtered_events:
            self.assertTrue(self.start_time <= event.start <= self.end_time)

    def test_category_and_time_filtering(self):
        """
        Тест фильтрации событий по категории и времени.
        """
        response = self.client.get(reverse('schedule:index'), {'category': 'test-category', 'time_start': self.start_time.strftime('%H:%M'), 'time_end': self.end_time.strftime('%H:%M')})
        self.assertEqual(response.status_code, 200)
        self.assertIn('events', response.context)
        filtered_events = response.context['events']
        for event in filtered_events:
            self.assertEqual(event.category, self.category)
            self.assertTrue(self.start_time <= event.start <= self.end_time)

    def test_multiple_parameters_filtering(self):
        """
        Тест фильтрации событий по нескольким параметрам.
        """
        response = self.client.get(reverse('schedule:index'), {'category': 'test-category', 'time_start': '00:00', 'time_end': '23:59'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('events', response.context)
        filtered_events = response.context['events']
        for event in filtered_events:
            self.assertEqual(event.category, self.category)
            self.assertTrue(event.start.time() >= timezone.datetime.strptime('00:00', '%H:%M').time())
            self.assertTrue(event.end.time() <= timezone.datetime.strptime('23:59', '%H:%M').time())

