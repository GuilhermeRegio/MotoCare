from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Moto, PerfilMoto, Rota
from .forms import MotoForm, PerfilMotoForm, RotaForm
from .controllers.moto_controller import MotoController


# Reutilizando as views antigas para manter compatibilidade
@login_required
def lista_motos(request):
    """Lista todas as motos do usuário"""
    return MotoController.index(request)


@login_required
def detalhe_moto(request, moto_id):
    """Detalhes de uma moto específica"""
    return MotoController.show(request, moto_id)


@login_required
def criar_moto(request):
    """Criar uma nova moto"""
    return MotoController.create(request)


@login_required
def editar_moto(request, moto_id):
    """Editar uma moto existente"""
    return MotoController.edit(request, moto_id)


@login_required
@require_POST
def excluir_moto(request, moto_id):
    """Excluir uma moto"""
    return MotoController.destroy(request, moto_id)


# API Views usando controllers
@login_required
def api_motos(request):
    """API para listar motos"""
    return MotoController.api_index(request)


@login_required
def perfil_moto(request, moto_id):
    """Gerenciar perfil da moto"""
    moto = get_object_or_404(Moto, id=moto_id, criado_por=request.user)
    perfil, created = PerfilMoto.objects.get_or_create(moto=moto)

    if request.method == 'POST':
        form = PerfilMotoForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('motos:perfil', moto_id=moto.id)
    else:
        form = PerfilMotoForm(instance=perfil)

    return render(request, 'motos/perfil.html', {
        'form': form,
        'moto': moto,
        'perfil': perfil
    })


@login_required
def rotas_moto(request, moto_id):
    """Gerenciar rotas da moto"""
    moto = get_object_or_404(Moto, id=moto_id, criado_por=request.user)
    rotas = moto.rotas.filter(ativo=True)

    if request.method == 'POST':
        form = RotaForm(request.POST)
        if form.is_valid():
            rota = form.save(commit=False)
            rota.moto = moto
            rota.save()
            messages.success(request, 'Rota criada com sucesso!')
            return redirect('motos:rotas', moto_id=moto.id)
    else:
        form = RotaForm()

    return render(request, 'motos/rotas.html', {
        'form': form,
        'moto': moto,
        'rotas': rotas
    })


@login_required
def api_moto_detalhes(request, moto_id):
    """API para detalhes da moto"""
    moto = get_object_or_404(Moto, id=moto_id, criado_por=request.user)

    data = {
        'id': moto.id,
        'modelo': moto.modelo,
        'marca': moto.marca,
        'ano': moto.ano,
        'km_atual': moto.km_atual,
        'km_compra': moto.km_compra,
        'cor': moto.cor,
        'placa': moto.placa,
        'chassi': moto.chassi,
        'renavam': moto.renavam,
        'data_compra': moto.data_compra.isoformat() if moto.data_compra else None,
        'data_fabricacao': moto.data_fabricacao.isoformat() if moto.data_fabricacao else None,
        'cilindrada': moto.cilindrada,
        'tipo_motor': moto.tipo_motor,
        'tipo_transmissao': moto.tipo_transmissao,
        'tipo_combustivel': moto.tipo_combustivel,
        'ativo': moto.ativo,
        'observacoes': moto.observacoes,
        'km_total_percorridos': moto.km_total_percorridos,
        'idade_anos': moto.idade_anos,
    }

    return JsonResponse(data)


@login_required
def api_atualizar_km(request, moto_id):
    """API para atualizar quilometragem"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    moto = get_object_or_404(Moto, id=moto_id, criado_por=request.user)

    try:
        novo_km = int(request.POST.get('km_atual'))
        if novo_km < moto.km_atual:
            return JsonResponse({'error': 'Novo KM não pode ser menor que o atual'}, status=400)

        moto.km_atual = novo_km
        moto.save()

        return JsonResponse({
            'success': True,
            'km_atual': moto.km_atual,
            'km_total_percorridos': moto.km_total_percorridos
        })

    except (ValueError, TypeError):
        return JsonResponse({'error': 'Valor de KM inválido'}, status=400)
