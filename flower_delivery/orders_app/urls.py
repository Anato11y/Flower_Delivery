from django.urls import path
from . import views
from .views import checkout, order_history, manage_orders, update_cart_item, delete_cart_item

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('order_history/', views.order_history, name='order_history'),
    path('manage_orders/', views.manage_orders, name='manage_orders'),
    path('update_cart_item/', views.update_cart_item, name='update_cart_item'),
    path('delete_cart_item/', views.delete_cart_item, name='delete_cart_item'),
    path('place_order/', views.place_order, name='place_order'),


]

