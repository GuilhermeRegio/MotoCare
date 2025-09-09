"""
API Views for Manutencoes app.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Manutencao
from .serializers import ManutencaoSerializer


class ManutencaoViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Manutencao operations.
    """
    serializer_class = ManutencaoSerializer
    permission_classes = [AllowAny]  # Temporário para desenvolvimento
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return active maintenances.
        """
        return Manutencao.objects.filter(ativo=True).order_by('-data_manutencao')
    
    def perform_create(self, serializer):
        """
        Set creator when saving.
        """
        serializer.save(criado_por=self.request.user)
    
    @action(detail=False, methods=['get'])
    def por_moto(self, request):
        """
        List maintenances by motorcycle.
        """
        moto_id = request.query_params.get('moto_id')
        if not moto_id:
            return Response({
                'success': False,
                'message': 'moto_id parameter is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        manutencoes = self.get_queryset().filter(moto_id=moto_id)
        serializer = self.get_serializer(manutencoes, many=True)
        
        return Response({
            'success': True,
            'data': serializer.data
        })
    
    @action(detail=False, methods=['get'])
    def estatisticas(self, request):
        """
        Return maintenance statistics.
        """
        queryset = self.get_queryset()
        
        total_manutencoes = queryset.count()
        total_gastos = sum(m.valor_total or 0 for m in queryset)
        
        # Statistics by type
        tipos = {}
        for manutencao in queryset:
            tipo = manutencao.tipo_servico
            if tipo not in tipos:
                tipos[tipo] = {'quantidade': 0, 'valor_total': 0}
            tipos[tipo]['quantidade'] += 1
            tipos[tipo]['valor_total'] += manutencao.valor_total or 0
        
        return Response({
            'success': True,
            'data': {
                'total_manutencoes': total_manutencoes,
                'total_gastos': total_gastos,
                'estatisticas_por_tipo': tipos
            }
        })
