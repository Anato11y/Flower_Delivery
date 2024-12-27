from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Product, CartItem

def index(request):
    products = Product.objects.all()
    return render(request, 'main_app/index.html', {'products': products})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def catalog(request):
    products = Product.objects.all()
    return render(request, 'main_app/catalog.html', {'products': products})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    # Проверяем, есть ли уже этот товар в корзине
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += quantity
    else:
        cart_item.quantity = quantity
    cart_item.save()

    messages.success(request, f"{product.name} добавлен в корзину ({cart_item.quantity} шт.)!")
    return redirect('catalog')

@csrf_exempt
def update_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = data.get('quantity', 0)

            # Проверяем, существует ли продукт
            product = Product.objects.get(id=product_id)

            if quantity > 0:
                # Добавляем или обновляем товар в корзине
                cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
                cart_item.quantity = quantity
                cart_item.save()
                return JsonResponse({'message': 'Корзина обновлена'})
            else:
                # Удаляем товар из корзины, если количество равно 0
                CartItem.objects.filter(user=request.user, product=product).delete()
                return JsonResponse({'message': 'Товар удалён из корзины'})

        except Product.DoesNotExist:
            return JsonResponse({'error': 'Товар не найден'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Неверный запрос'}, status=400)
