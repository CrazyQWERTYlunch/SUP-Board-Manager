from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils import timezone
from .forms import CreateOrderForm, validate_phone_number_format
from order.models import EventOrder
from catalog.models import Category, Route
from schedule.models import Event, EventProxy


class OrderFormsTestCase(TestCase):
    """
    Тесты форм приложения order.
    """

    def setUp(self):
        """
        Создает объекты Category, Route и EventProxy для связи с заказом.
        """
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.route = Route.objects.create(
            category=self.category,
            name='Test Route',
            slug='test-route',
            complexity=3,
            duration=120,
            distance='10 km'
        )
        self.event = EventProxy.objects.create(
            category=self.category,
            route=self.route,
            start=timezone.now(),
            end=timezone.now() + timedelta(hours=2),
            price=10.00,
            total_seats=50,
            remaining_seats=50
        )

    def test_validate_phone_number_format_valid(self):
        """
        Проверка валидации формата номера телефона с верным форматом.
        """
        valid_phone_numbers = ['123-456-78-90', '987-654-32-10']
        for phone_number in valid_phone_numbers:
            try:
                validate_phone_number_format(phone_number)
            except ValidationError:
                self.fail(f'Валидный номер телефона {phone_number} не прошел валидацию.')

    def test_validate_phone_number_format_invalid(self):
        """
        Проверка валидации формата номера телефона с неверным форматом.
        """
        invalid_phone_numbers = ['123-456', '12-34-56-789', '1234567890']
        for phone_number in invalid_phone_numbers:
            with self.assertRaises(ValidationError):
                validate_phone_number_format(phone_number)

    def test_create_order_form_clean_quantity(self):
        """
        Проверка очистки поля quantity формы CreateOrderForm.
        """
        form = CreateOrderForm(data={'quantity': 0})
        self.assertFalse(form.is_valid())
        self.assertIn('quantity', form.errors)

    def test_create_order_form_clean_payment_by_card(self):
        """
        Проверка очистки поля payment_by_card формы CreateOrderForm.
        """
        form = CreateOrderForm(data={'payment_by_card': '2'})
        self.assertFalse(form.is_valid())
        self.assertIn('payment_by_card', form.errors)

    def test_create_order_form_clean_phone_number(self):
        """
        Проверка очистки поля phone_number формы CreateOrderForm.
        """
        valid_phone_number = '123-456-78-90'
        form = CreateOrderForm(data={
            'event': self.event,
            'fullname': 'Test User',
            'email': 'test@example.com',
            'quantity': 1,
            'payment_by_card': '0',
            'phone_number': valid_phone_number
        })
        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['phone_number'], valid_phone_number)

    def test_create_order_form_clean_phone_number_invalid(self):
        """
        Проверка очистки поля phone_number формы CreateOrderForm на невалидные данные.
        """
        invalid_phone_number = '123-456'
        form = CreateOrderForm(data={'phone_number': invalid_phone_number})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)


class OrderModelsTestCase(TestCase):
    """
    Тесты моделей приложения order.
    """

    def setUp(self):
        """
        Создает объекты Category, Route и EventProxy для связи с заказом.
        """
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.route = Route.objects.create(
            category=self.category,
            name='Test Route',
            slug='test-route',
            complexity=3,
            duration=120,
            distance='10 km'
        )
        self.event = EventProxy.objects.create(
            category=self.category,
            route=self.route,
            start=timezone.now(),
            end=timezone.now() + timedelta(hours=2),
            price=10.00,
            total_seats=50,
            remaining_seats=50
        )

    def test_event_order_total_price(self):
        """
        Проверка вычисления общей стоимости заказа в модели EventOrder.
        """
        order = EventOrder.objects.create(event=self.event, fullname='Test User', phone_number='123-456-78-90', email='test@example.com', quantity=3, payment_by_card=False)
        self.assertEqual(order.total_price(), 30.00)

    def test_event_order_total_price_with_multiple_quantity(self):
        """
        Проверка вычисления общей стоимости заказа в модели EventOrder с несколькими товарами.
        """
        order = EventOrder.objects.create(event=self.event, fullname='Test User', phone_number='123-456-78-90', email='test@example.com', quantity=5, payment_by_card=False)
        self.assertEqual(order.total_price(), 50.00)

    def test_event_order_total_price_with_payment_by_card(self):
        """
        Проверка вычисления общей стоимости заказа в модели EventOrder при оплате картой.
        """
        order = EventOrder.objects.create(event=self.event, fullname='Test User', phone_number='123-456-78-90', email='test@example.com', quantity=2, payment_by_card=True)
        self.assertEqual(order.total_price(), 20.00)


class OrderViewsTestCase(TestCase):
    """
    Тесты представлений приложения order.
    """

    def setUp(self):
        """
        Создает объекты Category, Route и EventProxy для связи с заказом.
        """
        self.category = Category.objects.create(name='Test Category', slug='test-category')
        self.route = Route.objects.create(
            category=self.category,
            name='Test Route',
            slug='test-route',
            complexity=3,
            duration=120,
            distance='10 km'
        )
        self.event = EventProxy.objects.create(
            category=self.category,
            route=self.route,
            start=timezone.now() + timedelta(hours=1),
            end=timezone.now() + timedelta(hours=3),
            price=10.00,
            total_seats=50,
            remaining_seats=50
        )

    def test_create_order_view(self):
        """
        Проверка отображения формы оформления заказа для указанного мероприятия.
        """
        client = Client()
        response = client.get(reverse('order:create_order', kwargs={'event_id': self.event.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order/create_order.html')

    def test_create_order_post_success(self):
        """
        Проверка успешного создания заказа после отправки формы.
        """
        client = Client()
        url = reverse('order:create_order', kwargs={'event_id': self.event.id})
        data = {
            'event': self.event.id,
            'fullname': 'Test User',
            'phone_number': '123-456-78-90',
            'email': 'test@example.com',
            'quantity': 2,
            'payment_by_card': '0'
        }
        response = client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(EventOrder.objects.filter(fullname='Test User', phone_number='123-456-78-90', email='test@example.com', quantity=2, payment_by_card=False).exists())

    def test_create_order_post_invalid_data(self):
        """
        Проверка обработки неверных данных при отправке формы.
        """
        client = Client()
        url = reverse('order:create_order', kwargs={'event_id': self.event.id})
        data = {}
        response = client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(EventOrder.objects.exists())