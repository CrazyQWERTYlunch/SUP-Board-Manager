from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from .models import Route, Category

class RouteViewTest(TestCase):
    def test_get_routes(self):

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )


        uploaded = SimpleUploadedFile('test_image.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='django', description='asdasd')
        route_1 = Route.objects.create(name='Route 1', 
                                       category=category,
                                       image=uploaded,
                                       slug='route-1',
                                       complexity=4.00,
                                       duration=2,
                                       distance=2,
                                       price=1500.00)
        route_2 = Route.objects.create(name='Route 2', 
                                       category=category,
                                       image=uploaded,
                                       slug='route-2',
                                       complexity=3.00,
                                       duration=4,
                                       distance=7,
                                       price=2500.00)
        
        response = self.client.get(reverse('catalog:routes'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['routes'].count(), 2)
        self.assertEqual(list(response.context['routes']), [route_1, route_2])
        # self.assertContains(response, route_1)
        # self.assertContains(response, route_2)



class RouteDetailViewTest(TestCase):
    def test_get_product_by_slug(self):
        # Create a product
        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
            b'\x01\x0a\x00\x01\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02'
            b'\x02\x4c\x01\x00\x3b'
        )
        uploaded = SimpleUploadedFile(
            'small.gif', small_gif, content_type='image/gif')
        category = Category.objects.create(name='Category 1', description='asdasd') 
        route = Route.objects.create(name='Route 1', 
                                       category=category,
                                       image=uploaded,
                                       slug='route-1',
                                       complexity=4.00,
                                       duration=2,
                                       distance=2,
                                       price=1500.00)
        # Make a request to the product detail view with the product's slug
        response = self.client.get(
            reverse('catalog:route', kwargs={'slug': 'route-1'}))

        # Check that the response is a success
        self.assertEqual(response.status_code, 200)

        # Check that the product is in the response context
        self.assertEqual(response.context['route'], route)
        self.assertEqual(response.context['route'].slug, route.slug)