from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from typing import Dict, Any
from ..models import Moto
from ..forms import MotoForm
from ..requests.moto_request import CriarMotoRequest, AtualizarMotoRequest
from ..services.moto_service import MotoService


class MotoController:
    """Controller para operações relacionadas às motos"""

    @staticmethod
    @login_required
    def index(request):
        """Lista todas as motos do usuário"""
        resultado = MotoService.listar_motos_usuario(request)

        if resultado['success']:
            return render(request, 'motos/lista.html', {
                'motos': resultado['motos']
            })
        else:
            messages.error(request, resultado['message'])
            return render(request, 'motos/lista.html', {
                'motos': []
            })

    @staticmethod
    @login_required
    def show(request, moto_id: int):
        """Exibe detalhes de uma moto específica"""
        moto = get_object_or_404(Moto, id=moto_id, criado_por=request.user)

        return render(request, 'motos/detalhe.html', {
            'moto': moto
        })

    @staticmethod
    @login_required
    def create(request):
        """Exibe formulário de criação de moto"""
        if request.method == 'POST':
            return MotoController._store(request)

        form = MotoForm()
        return render(request, 'motos/form.html', {
            'form': form,
            'titulo': 'Nova Moto'
        })

    @staticmethod
    def _store(request) -> Any:
        """Processa criação de nova moto"""
        print(f"🚀 _store chamado! POST data: {request.POST}")
        
        # Criar request object
        moto_request = CriarMotoRequest(request.POST.dict())
        print(f"🔍 Request criado: {moto_request.data}")

        # Validar request
        is_valid = moto_request.is_valid()
        print(f"✅ Validação: {is_valid}")
        print(f"🔧 Errors: {moto_request.errors}")
        print(f"🧹 Cleaned data: {moto_request.cleaned_data}")
        
        if not is_valid:
            print("❌ Request inválido, retornando ao formulário")
            # Adicionar erros às messages
            for field, errors in moto_request.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            # Retornar ao formulário com erros
            form = MotoForm(request.POST)
            return render(request, 'motos/form.html', {
                'form': form,
                'titulo': 'Nova Moto'
            })

        print("✅ Request válido, chamando service")
        # Chamar service para criar moto
        resultado = MotoService.criar_moto(request, moto_request.cleaned_data)
        print(f"🎯 Resultado do service: {resultado}")

        if resultado['success']:
            messages.success(request, resultado['message'])
            return redirect(resultado['redirect_url'])
        else:
            print("❌ Service retornou erro")
            # Adicionar erros do service
            for error in resultado.get('errors', []):
                messages.error(request, error)

            form = MotoForm(request.POST)
            return render(request, 'motos/form.html', {
                'form': form,
                'titulo': 'Nova Moto'
            })

    @staticmethod
    @login_required
    def edit(request, moto_id: int):
        """Exibe formulário de edição de moto"""
        moto = get_object_or_404(Moto, id=moto_id, criado_por=request.user)

        if request.method == 'POST':
            return MotoController._update(request, moto_id)

        form = MotoForm(instance=moto)
        return render(request, 'motos/form.html', {
            'form': form,
            'titulo': 'Editar Moto',
            'moto': moto
        })

    @staticmethod
    def _update(request, moto_id: int) -> Any:
        """Processa atualização de moto"""
        # Criar request object
        moto_request = AtualizarMotoRequest(request.POST.dict())

        # Validar request
        if not moto_request.is_valid():
            # Adicionar erros às messages
            for field, errors in moto_request.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

            # Retornar ao formulário com erros
            moto = get_object_or_404(Moto, id=moto_id, criado_por=request.user)
            form = MotoForm(request.POST, instance=moto)
            return render(request, 'motos/form.html', {
                'form': form,
                'titulo': 'Editar Moto',
                'moto': moto
            })

        # Chamar service para atualizar moto
        resultado = MotoService.atualizar_moto(request, moto_id, moto_request.cleaned_data)

        if resultado['success']:
            messages.success(request, resultado['message'])
            return redirect(resultado['redirect_url'])
        else:
            # Adicionar erros do service
            for error in resultado.get('errors', []):
                messages.error(request, error)

            moto = get_object_or_404(Moto, id=moto_id, criado_por=request.user)
            form = MotoForm(request.POST, instance=moto)
            return render(request, 'motos/form.html', {
                'form': form,
                'titulo': 'Editar Moto',
                'moto': moto
            })

    @staticmethod
    @login_required
    @require_POST
    def destroy(request, moto_id: int):
        """Exclui uma moto"""
        resultado = MotoService.excluir_moto(request, moto_id)

        if resultado['success']:
            messages.success(request, resultado['message'])
        else:
            messages.error(request, resultado['message'])

        return redirect('/motos/')

    @staticmethod
    @login_required
    def api_index(request):
        """API para listar motos"""
        resultado = MotoService.listar_motos_usuario(request)

        if resultado['success']:
            motos_data = list(resultado['motos'].values(
                'id', 'modelo', 'marca', 'ano', 'km_atual', 'placa'
            ))
            return JsonResponse({'motos': motos_data})
        else:
            return JsonResponse({'error': resultado['message']}, status=400)
