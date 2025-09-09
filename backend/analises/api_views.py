"""
API Views for Analises app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from motos.models import Moto
from manutencoes.models import Manutencao
from datetime import datetime, timedelta
from django.db.models import Count, Sum, Avg
from django.db.models.functions import TruncMonth


class AnaliseViewSet(viewsets.ViewSet):
    """
    ViewSet for analysis operations.
    """
    permission_classes = [AllowAny]  # Temporário para desenvolvimento
    """
    ViewSet for analysis operations.
    """
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def gastos_mensais(self, request):
        """
        Return monthly spending analysis.
        """
        try:
            # Get maintenance expenses by month
            gastos_mensais = Manutencao.objects.filter(
                ativo=True,
                data_manutencao__isnull=False
            ).annotate(
                mes=TruncMonth('data_manutencao')
            ).values('mes').annotate(
                total=Sum('valor_total'),
                quantidade=Count('id')
            ).order_by('mes')
            
            # Format data for charts
            dados_formatados = []
            for item in gastos_mensais:
                dados_formatados.append({
                    'mes': item['mes'].strftime('%m/%Y'),
                    'total_gastos': float(item['total'] or 0),
                    'quantidade_manutencoes': item['quantidade']
                })
            
            return Response({
                'success': True,
                'data': dados_formatados
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Erro ao analisar gastos mensais: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def gastos_por_moto(self, request):
        """
        Return spending analysis by motorcycle.
        """
        try:
            motos_com_gastos = []
            
            for moto in Moto.objects.filter(ativo=True):
                total_gastos = Manutencao.objects.filter(
                    moto=moto,
                    ativo=True
                ).aggregate(total=Sum('valor_total'))['total'] or 0
                
                quantidade_manutencoes = Manutencao.objects.filter(
                    moto=moto,
                    ativo=True
                ).count()
                
                motos_com_gastos.append({
                    'moto_id': moto.id,
                    'moto_nome': f"{moto.marca} {moto.modelo}",
                    'placa': moto.placa,
                    'total_gastos': float(total_gastos),
                    'quantidade_manutencoes': quantidade_manutencoes,
                    'gasto_por_km': float(total_gastos / max(1, moto.km_total_percorridos)) if moto.km_total_percorridos > 0 else 0
                })
            
            # Sort by total spending
            motos_com_gastos.sort(key=lambda x: x['total_gastos'], reverse=True)
            
            return Response({
                'success': True,
                'data': motos_com_gastos
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Erro ao analisar gastos por moto: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def tipos_manutencao(self, request):
        """
        Return analysis by maintenance type.
        """
        try:
            tipos_stats = Manutencao.objects.filter(ativo=True).values(
                'tipo_servico'
            ).annotate(
                quantidade=Count('id'),
                total_gastos=Sum('valor_total'),
                gasto_medio=Avg('valor_total')
            ).order_by('-quantidade')
            
            dados_formatados = []
            for item in tipos_stats:
                dados_formatados.append({
                    'tipo': item['tipo_servico'],
                    'quantidade': item['quantidade'],
                    'total_gastos': float(item['total_gastos'] or 0),
                    'gasto_medio': float(item['gasto_medio'] or 0)
                })
            
            return Response({
                'success': True,
                'data': dados_formatados
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Erro ao analisar tipos de manutenção: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(detail=False, methods=['get'])
    def eficiencia_combustivel(self, request):
        """
        Return fuel efficiency analysis.
        """
        try:
            dados_eficiencia = []
            
            for moto in Moto.objects.filter(ativo=True):
                # This would need more complex logic based on fuel records
                # For now, return basic data
                dados_eficiencia.append({
                    'moto_id': moto.id,
                    'moto_nome': f"{moto.marca} {moto.modelo}",
                    'km_total': moto.km_total_percorridos,
                    'eficiencia_estimada': 30.0  # Placeholder value
                })
            
            return Response({
                'success': True,
                'data': dados_eficiencia
            })
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Erro ao analisar eficiência: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
