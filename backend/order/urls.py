from django.urls import path
from order import views

app_name = 'order'

urlpatterns = [
    path('create_order/<int:event_id>/', views.create_order, name='create_order'),
]
