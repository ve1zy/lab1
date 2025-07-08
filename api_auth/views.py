from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

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
				secure=True,  # Измените на False для локальной разработки
				samesite='None',
				path='/'
			)
            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                samesite='None',
                path='/'
            )
            return res
        except Exception as e:
            print(f"Error: {e}")  # Вывод ошибки в консоль
            return Response({"success": False})

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            access_token = tokens['access']

            res = Response({'refreshed': True})
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # Установите True, если используете HTTPS
                samesite='Lax',
                path='/'
            )
            return res
        except Exception as e:
            print(e)
            return Response({'refreshed': False}, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    try:
        res = Response({'success': True})
        res.delete_cookie('access_token', path='/', samesite='Lax')
        res.delete_cookie('refresh_token', path='/', samesite='Lax')
        return res
    except Exception as e:
        print(e)
        return Response({'success': False}, status=400)