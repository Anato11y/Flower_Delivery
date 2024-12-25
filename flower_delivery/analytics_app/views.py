from django.shortcuts import render
from orders_app.models import Order
from django.db.models import Sum

def analytics(request):
    total_orders = Order.objects.count()
    total_revenue = Order.objects.aggregate(Sum('products__price'))['products__price__sum']
    return render(request, 'analytics_app/analytics.html', {'total_orders': total_orders, 'total_revenue': total_revenue})
