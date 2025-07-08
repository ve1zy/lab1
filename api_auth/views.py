# views.py

from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)

            # Создаем HTTP-only cookie
            response = Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

            response.set_cookie(
                key='auth_token',
                value=str(refresh.access_token),
                httponly=True,
                secure=False,  # Установите True, если используете HTTPS
                samesite='Lax',
                max_age=3600,  # Время жизни токена в секундах
            )
            return response
        else:
            return Response({'detail': 'Неверный логин или пароль'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request, *args, **kwargs):
        response = Response({'detail': 'Вы успешно вышли'}, status=status.HTTP_200_OK)
        response.delete_cookie('auth_token')  # Удаляем куки
        return response