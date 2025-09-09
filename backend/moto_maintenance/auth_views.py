from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')

            if not username or not password:
                return JsonResponse({
                    'error': 'Username e password são obrigatórios'
                }, status=400)

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                })
            else:
                return JsonResponse({
                    'error': 'Credenciais inválidas'
                }, status=401)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Dados JSON inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': 'Erro interno do servidor'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({'success': True})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request):
    """Retorna dados do usuário autenticado"""
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'date_joined': user.date_joined,
    })


@ensure_csrf_cookie
def csrf_view(request):
    """Endpoint para obter CSRF token"""
    return JsonResponse({
        'csrfToken': get_token(request)
    })


@api_view(['GET'])
def health_check(request):
    """Health check endpoint"""
    return Response({
        'status': 'healthy',
        'message': 'API funcionando corretamente'
    })
