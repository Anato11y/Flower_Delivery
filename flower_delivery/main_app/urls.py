from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('catalog/', views.catalog, name='catalog'),  # Добавлен маршрут каталога
    path('logout/', LogoutView.as_view(), name='logout'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('login/', LoginView.as_view(template_name='main_app/login.html'), name='login'),
]
