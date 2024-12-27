from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Order, OrderItem
from main_app.models import Product, CartItem
from bot.handlers import order_notification
import json


def create_order(user, delivery_address):
    cart_items = CartItem.objects.filter(user=user)
    if not cart_items.exists():
        return None, 'Корзина пуста'

    order = Order.objects.create(user=user, delivery_address=delivery_address, status='Pending')

    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price
        )
        cart_item.delete()

    return order, None


@login_required
def checkout(request):
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address', '').strip()
        if not delivery_address:
            return JsonResponse({'success': False, 'error': 'Адрес доставки обязателен'}, status=400)

        # Создание заказа
        order, error = create_order(request.user, delivery_address)
        if error:
            return JsonResponse({'success': False, 'error': error}, status=400)

        # Уведомление боту
        order_notification(order.id)

        return JsonResponse({'success': True, 'message': 'Заказ успешно оформлен'})

    # Показ корзины
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.quantity * item.product.price for item in cart_items)

    for item in cart_items:
        item.total = item.quantity * item.product.price

    return render(request, 'orders_app/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders_app/order_history.html', {'orders': orders})


@login_required
def manage_orders(request):
    orders = Order.objects.all()
    return render(request, 'orders_app/manage_orders.html', {'orders': orders})


@csrf_exempt
@login_required
def update_cart_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('id')
            quantity = int(data.get('quantity', 1))

            # Логирование
            print(f"Update request received: ID={item_id}, Quantity={quantity}")

            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            cart_item.quantity = quantity
            cart_item.save()

            total_price = sum(item.quantity * item.product.price for item in CartItem.objects.filter(user=request.user))
            item_total = cart_item.quantity * cart_item.product.price

            return JsonResponse({'success': True, 'total_price': total_price, 'item_total': item_total})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Товар не найден'}, status=404)
        except Exception as e:
            print(f"Error in update_cart_item: {e}")  # Лог ошибки
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Неверный запрос'}, status=400)


@csrf_exempt
@login_required
def delete_cart_item(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('id')

            # Проверяем, существует ли товар в корзине
            cart_item = CartItem.objects.get(id=item_id, user=request.user)
            cart_item.delete()

            # Пересчитываем общую сумму корзины
            total_price = sum(
                float(item.quantity * item.product.price) for item in CartItem.objects.filter(user=request.user)
            )

            return JsonResponse({'success': True, 'total_price': total_price})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Товар не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Неверный запрос'}, status=400)


@login_required
def place_order(request):
    if request.method == 'POST':
        delivery_address = request.POST.get('delivery_address', '').strip()
        if not delivery_address:
            return JsonResponse({'success': False, 'error': 'Адрес доставки обязателен'}, status=400)

        cart_items = CartItem.objects.filter(user=request.user)
        if not cart_items.exists():
            return JsonResponse({'success': False, 'error': 'Корзина пуста'}, status=400)

        # Создаем заказ
        order = Order.objects.create(user=request.user, delivery_address=delivery_address, status='Pending')

        for cart_item in cart_items:
            # Проверка на экземпляр Product
            if isinstance(cart_item.product, Product):
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,  # Здесь передается экземпляр модели Product
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )
            else:
                return JsonResponse({'success': False, 'error': 'Некорректный продукт в корзине'}, status=400)

            cart_item.delete()  # Удаляем товар из корзины

        # Уведомление боту
        order_notification(order.id)

        return JsonResponse({'success': True, 'message': 'Заказ успешно оформлен'})

    return JsonResponse({'success': False, 'error': 'Неверный запрос'}, status=400)