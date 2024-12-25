from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating', 'review')  # Поля для отображения
    list_filter = ('rating',)  # Фильтр по рейтингу
    search_fields = ('user__username', 'product__name', 'review')  # Поиск по пользователю и товару
