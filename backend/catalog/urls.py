from django.urls import path
from catalog import views

app_name = 'catalog'

urlpatterns = [
    path('', views.routes_view, name='routes'),
    path('<slug:slug>/', views.route_detail_view, name='route'),
]
