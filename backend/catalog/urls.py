from django.urls import path
from .views import routes_view, route_detail_view, category_list

app_name = 'catalog'

urlpatterns = [
    path('', routes_view, name='routes'),
    path('<slug:slug>/', route_detail_view, name='route'),
    path('search/<slug:slug>/', category_list, name='category_list'),
]
