from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings  # Импорт настроек Django

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main_app.urls')),
    path('orders/', include('orders_app.urls')),
    path('reviews/', include('reviews_app.urls')),
    path('analytics/', include('analytics_app.urls')),

]

# Обработка медиафайлов
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
