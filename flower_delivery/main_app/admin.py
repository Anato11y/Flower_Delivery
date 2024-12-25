from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')  # Поля для отображения в списке
    search_fields = ('name', 'description')  # Поиск по полям
