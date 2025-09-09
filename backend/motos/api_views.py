from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from .models import Moto, PerfilMoto, Rota
from .serializers import MotoSerializer, MotoDetailSerializer, PerfilMotoSerializer, RotaSerializer


class MotoViewSet(viewsets.ModelViewSet):
    """ViewSet para operações CRUD de Motos"""
    
    serializer_class = MotoSerializer
    permission_classes = [AllowAny]  # Temporário para desenvolvimento
    
    def get_queryset(self):
        """Retorna motos ativas"""
        return Moto.objects.filter(ativo=True).order_by('-criado_em')
    
    def get_serializer_class(self):
        """Usa serializer detalhado para retrieve"""
        if self.action == 'retrieve':
            return MotoDetailSerializer
        return MotoSerializer
    
    def perform_create(self, serializer):
        """Define o usuário criador ao salvar"""
        serializer.save(criado_por=self.request.user)
    
    @action(detail=True, methods=['post'])
    def criar_perfil(self, request, pk=None):
        """Cria um perfil para a moto"""
        moto = self.get_object()
        
        if hasattr(moto, 'perfil'):
            return Response({
                'success': False,
                'message': 'Esta moto já possui um perfil'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = PerfilMotoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(moto=moto)
            return Response({
                'success': True,
                'message': 'Perfil criado com sucesso',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Dados inválidos',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['put', 'patch'])
    def atualizar_perfil(self, request, pk=None):
        """Atualiza o perfil da moto"""
        moto = self.get_object()
        
        if not hasattr(moto, 'perfil'):
            return Response({
                'success': False,
                'message': 'Esta moto não possui um perfil'
            }, status=status.HTTP_404_NOT_FOUND)
        
        partial = request.method == 'PATCH'
        serializer = PerfilMotoSerializer(moto.perfil, data=request.data, partial=partial)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Perfil atualizado com sucesso',
                'data': serializer.data
            })
        
        return Response({
            'success': False,
            'message': 'Dados inválidos',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def adicionar_rota(self, request, pk=None):
        """Adiciona uma rota à moto"""
        moto = self.get_object()
        
        data = request.data.copy()
        data['moto'] = moto.id
        
        serializer = RotaSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'message': 'Rota adicionada com sucesso',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'success': False,
            'message': 'Dados inválidos',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'])
    def rotas(self, request, pk=None):
        """Lista todas as rotas da moto"""
        moto = self.get_object()
        rotas = moto.rotas.filter(ativo=True)
        serializer = RotaSerializer(rotas, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=True, methods=['post'])
    def atualizar_km(self, request, pk=None):
        """Atualiza a quilometragem da moto"""
        moto = self.get_object()
        novo_km = request.data.get('km_atual')
        
        if not novo_km:
            return Response({
                'success': False,
                'message': 'Campo km_atual é obrigatório'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            novo_km = int(novo_km)
            if novo_km < moto.km_atual:
                return Response({
                    'success': False,
                    'message': 'A nova quilometragem não pode ser menor que a atual'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            moto.km_atual = novo_km
            moto.save()
            
            return Response({
                'success': True,
                'message': 'Quilometragem atualizada com sucesso',
                'data': {
                    'km_atual': moto.km_atual,
                    'km_total_percorridos': moto.km_total_percorridos
                }
            })
            
        except (ValueError, TypeError):
            return Response({
                'success': False,
                'message': 'Quilometragem deve ser um número válido'
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """Retorna estatísticas gerais das motos"""
        motos = self.get_queryset()
        
        total_motos = motos.count()
        km_total = sum(moto.km_total_percorridos for moto in motos)
        
        # Estatísticas por marca
        marcas = {}
        for moto in motos:
            marca = moto.marca
            if marca not in marcas:
                marcas[marca] = {'quantidade': 0, 'km_total': 0}
            marcas[marca]['quantidade'] += 1
            marcas[marca]['km_total'] += moto.km_total_percorridos
        
        return Response({
            'success': True,
            'data': {
                'total_motos': total_motos,
                'km_total_percorridos': km_total,
                'estatisticas_por_marca': marcas
            }
        })


class RotaViewSet(viewsets.ModelViewSet):
    """ViewSet para operações CRUD de Rotas"""
    
    serializer_class = RotaSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna apenas rotas ativas"""
        return Rota.objects.filter(ativo=True).order_by('-data_registro')
    
    @action(detail=True, methods=['post'])
    def desativar(self, request, pk=None):
        """Desativa uma rota"""
        rota = self.get_object()
        rota.ativo = False
        rota.save()
        
        return Response({
            'success': True,
            'message': 'Rota desativada com sucesso'
        })


class PerfilMotoViewSet(viewsets.ModelViewSet):
    """ViewSet para operações CRUD de Perfis de Moto"""
    
    serializer_class = PerfilMotoSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Retorna todos os perfis"""
        return PerfilMoto.objects.all().order_by('-atualizado_em')
