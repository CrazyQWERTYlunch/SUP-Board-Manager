from django.urls import path
from schedule import views

app_name = 'schedule'

urlpatterns = [
    path('search/', views.index, name='search'),
    path('', views.index, name='index'),
    path('<slug:category_slug>/', views.index, name='index'),

]