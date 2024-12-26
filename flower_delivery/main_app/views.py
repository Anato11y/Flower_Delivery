from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Product
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Product

def index(request):
    products = Product.objects.all()
    return render(request, 'main_app/index.html', {'products': products})

    # Разбиваем на группы по 5
    def chunk(items, chunk_size):
        return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)]

    products_chunks = chunk(products, 5)

    return render(request, 'main_app/index.html', {'products_chunks': products_chunks})

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