from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views import View
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import json


@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                return JsonResponse({
                    'success': False,
                    'message': 'Username e password são obrigatórios'
                }, status=400)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return JsonResponse({
                    'success': True,
                    'message': 'Login realizado com sucesso',
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
                    'success': False,
                    'message': 'Credenciais inválidas'
                }, status=401)
                
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Dados JSON inválidos'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Erro interno: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutAPIView(View):
    def post(self, request):
        logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Logout realizado com sucesso'
        })


class UserAPIView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse({
                'authenticated': True,
                'user': {
                    'id': request.user.id,
                    'username': request.user.username,
                    'email': request.user.email,
                    'first_name': request.user.first_name,
                    'last_name': request.user.last_name,
                }
            })
        else:
            return JsonResponse({
                'authenticated': False,
                'user': None
            })


@api_view(['GET'])
@permission_classes([AllowAny])
def csrf_token_view(request):
    """Retorna o token CSRF para o frontend React"""
    token = get_token(request)
    return Response({'csrfToken': token})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_stats_view(request):
    """Retorna estatísticas para o dashboard"""
    from motos.models import Moto
    from manutencoes.models import Manutencao
    from datetime import datetime, timedelta
    
    try:
        # Estatísticas básicas
        total_motos = Moto.objects.count()
        total_manutencoes = Manutencao.objects.count()
        
        # Manutenções dos últimos 30 dias
        data_limite = datetime.now() - timedelta(days=30)
        manutencoes_recentes = Manutencao.objects.filter(
            data_manutencao__gte=data_limite
        ).count()
        
        # Motos que precisam de manutenção (exemplo: km > 10000)
        motos_manutencao = Moto.objects.filter(quilometragem__gt=10000).count()
        
        return Response({
            'success': True,
            'data': {
                'totalMotos': total_motos,
                'totalManutencoes': total_manutencoes,
                'manutencoesRecentes': manutencoes_recentes,
                'motosManutencao': motos_manutencao,
            }
        })
    except Exception as e:
        return Response({
            'success': False,
            'message': f'Erro ao buscar estatísticas: {str(e)}'
        }, status=500)
