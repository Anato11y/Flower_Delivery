from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('catalog/', views.catalog, name='catalog'),  # Добавлен маршрут каталога
]
