from django.shortcuts import render, redirect
from .models import Order
from main_app.models import Product
from bot.handlers import order_notification
def checkout(request):
    if request.method == 'POST':
        product_ids = request.POST.getlist('products')
        order = Order.objects.create(user=request.user)
        order.products.add(*Product.objects.filter(id__in=product_ids))
        order.save()

        # Уведомление боту
        order_notification(order.id)
        return redirect('order_history')

    products = Product.objects.all()
    return render(request, 'orders_app/checkout.html', {'products': products})

def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders_app/order_history.html', {'orders': orders})

def manage_orders(request):
    orders = Order.objects.all()
    return render(request, 'orders_app/manage_orders.html', {'orders': orders})
