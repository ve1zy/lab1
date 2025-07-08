from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, logout, check_auth

urlpatterns = [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', logout),
    path('check-auth/', check_auth, name='check_auth'),
]