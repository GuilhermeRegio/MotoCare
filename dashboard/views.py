from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth
from django.utils import timezone
from datetime import datetime, timedelta
from motos.models import Moto
from manutencoes.models import Manutencao, ItemManutencaoRealizada
from analises.models import AnaliseTecnica


@login_required
def dashboard(request):
    """Dashboard principal do usuário"""
    # Buscar moto principal do usuário
    moto_principal = Moto.objects.filter(criado_por=request.user, ativo=True).first()

    context = {
        'moto_principal': moto_principal,
        'total_motos': Moto.objects.filter(criado_por=request.user, ativo=True).count(),
    }

    return render(request, 'dashboard/index.html', context)


@login_required
def api_dashboard_data(request):
    """API para dados do dashboard"""
    # Filtros de data (últimos 12 meses)
    data_inicio = timezone.now() - timedelta(days=365)

    # Dados das motos
    motos = Moto.objects.filter(criado_por=request.user, ativo=True)

    # Dados de manutenções
    manutencoes = Manutencao.objects.filter(
        moto__criado_por=request.user,
        data_conclusao__gte=data_inicio
    )

    # Calcular métricas
    total_gasto = ItemManutencaoRealizada.objects.filter(
        manutencao__moto__criado_por=request.user,
        manutencao__data_conclusao__gte=data_inicio
    ).aggregate(total=Sum('valor_total'))['total'] or 0

    # Gastos por tipo
    gastos_por_tipo = ItemManutencaoRealizada.objects.filter(
        manutencao__moto__criado_por=request.user,
        manutencao__data_conclusao__gte=data_inicio
    ).values('item__tipo__nome').annotate(
        total=Sum('valor_total')
    ).order_by('-total')

    # Gastos por mês
    gastos_por_mes = ItemManutencaoRealizada.objects.filter(
        manutencao__moto__criado_por=request.user,
        manutencao__data_conclusao__gte=data_inicio
    ).annotate(
        mes=TruncMonth('manutencao__data_conclusao')
    ).values('mes').annotate(
        total=Sum('valor_total')
    ).order_by('mes')

    # Próxima manutenção
    proxima_manutencao = Manutencao.objects.filter(
        moto__criado_por=request.user,
        status__in=['planejada', 'comprada'],
        data_planejada__gte=timezone.now().date()
    ).order_by('data_planejada').first()

    # Análises recentes
    analises_recentes = AnaliseTecnica.objects.filter(
        moto__criado_por=request.user
    ).order_by('-data_conclusao')[:5]

    data = {
        'moto_principal': {
            'modelo': motos.first().modelo if motos.exists() else None,
            'km_atual': motos.first().km_atual if motos.exists() else 0,
        } if motos.exists() else None,
        'metricas': {
            'total_motos': motos.count(),
            'total_manutencoes': manutencoes.count(),
            'total_gasto': float(total_gasto),
            'media_km': float(total_gasto / max(motos.first().km_atual, 1)) if motos.exists() else 0,
            'gastos_por_tipo': {item['item__tipo__nome']: float(item['total']) for item in gastos_por_tipo},
            'gastos_por_mes': {item['mes'].strftime('%Y-%m'): float(item['total']) for item in gastos_por_mes},
            'proxima_manutencao': {
                'tipo': proxima_manutencao.tipo.nome if proxima_manutencao else None,
                'data_planejada': proxima_manutencao.data_planejada.isoformat() if proxima_manutencao else None,
                'km_proxima': proxima_manutencao.km_proxima if proxima_manutencao else None,
                'km_restantes': (proxima_manutencao.km_proxima - motos.first().km_atual) if proxima_manutencao and motos.exists() else None,
                'urgencia': 'alta' if proxima_manutencao and (proxima_manutencao.data_planejada - timezone.now().date()).days <= 7 else 'normal'
            } if proxima_manutencao else None,
        },
        'manutencoes': {
            'compradas': list(Manutencao.objects.filter(
                moto__criado_por=request.user,
                status='comprada'
            ).values('id', 'titulo', 'tipo__nome')),
            'instaladas': list(Manutencao.objects.filter(
                moto__criado_por=request.user,
                status='concluida'
            ).values('id', 'titulo', 'tipo__nome')),
            'planejadas': list(Manutencao.objects.filter(
                moto__criado_por=request.user,
                status='planejada'
            ).values('id', 'titulo', 'tipo__nome')),
        },
        'analises_recentes': [{
            'id': analise.id,
            'tipo': analise.tipo,
            'titulo': analise.titulo,
            'status': analise.status,
            'data_conclusao': analise.data_conclusao.isoformat() if analise.data_conclusao else None,
        } for analise in analises_recentes],
    }

    return JsonResponse(data)


@login_required
def relatorios(request):
    """Página de relatórios"""
    return render(request, 'dashboard/relatorios.html')


@login_required
def configuracoes(request):
    """Página de configurações"""
    return render(request, 'dashboard/configuracoes.html')
