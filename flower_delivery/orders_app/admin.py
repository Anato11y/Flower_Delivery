from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'order_date')  # Поля для отображения
    list_filter = ('status', 'order_date')  # Фильтры по полям
    search_fields = ('user__username',)  # Поиск по имени пользователя
