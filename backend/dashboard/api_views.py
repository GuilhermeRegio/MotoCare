"""
API Views for Dashboard app.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from motos.models import Moto
from manutencoes.models import Manutencao
from datetime import datetime, timedelta
from django.db.models import Count, Sum


class DashboardAPIView(APIView):
    """
    API view for dashboard statistics.
    """
    permission_classes = [AllowAny]  # Temporário para desenvolvimento
    
    def get(self, request):
        """
        Return dashboard statistics.
        """
        try:
            # Basic statistics
            total_motos = Moto.objects.filter(ativo=True).count()
            total_manutencoes = Manutencao.objects.count()
            
            # Recent maintenances (last 30 days)
            data_limite = datetime.now() - timedelta(days=30)
            manutencoes_recentes = Manutencao.objects.filter(
                criado_em__gte=data_limite
            ).count()
            
            # Total spending
            total_gastos = Manutencao.objects.aggregate(
                total=Sum('valor_real')
            )['total'] or 0
            
            # Main motorcycle (most recent)
            moto_principal = None
            if total_motos > 0:
                moto = Moto.objects.filter(ativo=True).order_by('-criado_em').first()
                if moto:
                    moto_principal = {
                        'id': moto.id,
                        'modelo': moto.modelo,
                        'marca': moto.marca,
                        'ano_display': moto.ano_display,
                        'placa': moto.placa,
                        'km_atual': moto.km_atual,
                        'km_total_percorridos': moto.km_total_percorridos,
                        'imagem_url': moto.imagem_principal.url if moto.imagem_principal else None,
                    }
            
            # Statistics by brand
            marcas_stats = Moto.objects.filter(ativo=True).values('marca').annotate(
                quantidade=Count('id')
            ).order_by('-quantidade')[:5]
            
            # Monthly maintenance statistics
            manutencoes_mensais = []
            for i in range(6):  # Last 6 months
                data_inicio = datetime.now().replace(day=1) - timedelta(days=30*i)
                data_fim = data_inicio.replace(day=28) + timedelta(days=4)
                
                count = Manutencao.objects.filter(
                    ativo=True,
                    data_manutencao__gte=data_inicio,
                    data_manutencao__lt=data_fim
                ).count()
                
                manutencoes_mensais.append({
                    'mes': data_inicio.strftime('%m/%Y'),
                    'quantidade': count
                })
            
            return Response({
                'success': True,
                'data': {
                    'total_motos': total_motos,
                    'total_manutencoes': total_manutencoes,
                    'manutencoes_recentes': manutencoes_recentes,
                    'total_gastos': float(total_gastos),
                    'moto_principal': moto_principal,
                    'marcas_stats': list(marcas_stats),
                    'manutencoes_mensais': manutencoes_mensais,
                    'metricas': {
                        'total_manutencoes': total_manutencoes,
                        'total_gasto': float(total_gastos),
                        'media_km': int(sum(m.km_atual for m in Moto.objects.filter(ativo=True)) / max(1, total_motos))
                    }
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'success': False,
                'message': f'Erro ao buscar dados do dashboard: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
