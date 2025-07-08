from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import UserRegistrationSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']
            refresh_token = tokens['refresh']
            
            res = Response()
            res.data = {"success": True}
            res.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=False,  # Установите True для HTTPS
                samesite='Lax',  # Или 'None' для кросс-доменных запросов
                path='/'
            )
            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=False,  # Установите True для HTTPS
                samesite='Lax',  # Или 'None' для кросс-доменных запросов
                path='/'
            )
            return res
        except Exception as e:
            print(f"Error during login: {e}")
            return Response({"success": False})

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']
            
            res = Response()
            res.data = {'refreshed': True}
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # Установите True для HTTPS
                samesite='Lax',  # Или 'None' для кросс-доменных запросов
                path='/'
            )
            return res
        except Exception as e:
            print(f"Error during token refresh: {e}")
            return Response({'refreshed': False})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        res = Response()
        res.data = {'success': True}
        res.delete_cookie('access_token', path='/', samesite='Lax')
        res.delete_cookie('refresh_token', path='/', samesite='Lax')
        return res
    except Exception as e:
        print(f"Error during logout: {e}")
        return Response({'success': False})