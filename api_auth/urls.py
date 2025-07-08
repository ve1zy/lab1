# urls.py

from django.contrib import admin
from django.urls import path
from .views import LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]	