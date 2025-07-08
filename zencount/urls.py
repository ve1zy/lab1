from django.contrib import admin  # Импорт для работы с админкой Django
from django.urls import path, include
from django.views.generic.base import RedirectView  # Импорт для редиректа

urlpatterns = [
    path('admin/', admin.site.urls),  # Маршрут для админки Django
    path('', RedirectView.as_view(url='/login/')),  # Редирект с корневого пути на /login/
    path('', include('api_auth.urls')),  # Включение маршрутов из приложения api_auth
]