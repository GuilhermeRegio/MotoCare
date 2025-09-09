from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from typing import Dict, Any
from ..repositories.moto_repository import MotoRepository


class MotoService:
    """Service para lógica de negócio relacionada às motos"""

    @staticmethod
    def criar_moto(request, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Serviço para criar uma nova moto

        Args:
            request: Request object do Django
            form_data: Dados validados do formulário

        Returns:
            Dict com resultado da operação
        """
        try:
            # Criar moto usando o repository
            moto = MotoRepository.create_moto(form_data, request.user)

            # Retornar sucesso
            return {
                'success': True,
                'moto': moto,
                'message': f'Moto "{moto.modelo}" foi criada com sucesso!',
                'redirect_url': f'/motos/{moto.id}/'
            }

        except ValidationError as e:
            return {
                'success': False,
                'errors': e.messages,
                'message': 'Erro de validação nos dados informados.'
            }
        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)],
                'message': 'Erro interno ao criar moto.'
            }

    @staticmethod
    def atualizar_moto(request, moto_id: int, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Serviço para atualizar uma moto existente

        Args:
            request: Request object do Django
            moto_id: ID da moto a ser atualizada
            form_data: Dados validados do formulário

        Returns:
            Dict com resultado da operação
        """
        try:
            # Buscar moto
            moto = MotoRepository.get_by_id_and_user(moto_id, request.user)
            if not moto:
                return {
                    'success': False,
                    'message': 'Moto não encontrada.'
                }

            # Atualizar moto
            moto_atualizada = MotoRepository.update_moto(moto, form_data)

            return {
                'success': True,
                'moto': moto_atualizada,
                'message': f'Moto "{moto_atualizada.modelo}" foi atualizada com sucesso!',
                'redirect_url': f'/motos/{moto_atualizada.id}/'
            }

        except ValidationError as e:
            return {
                'success': False,
                'errors': e.messages,
                'message': 'Erro de validação nos dados informados.'
            }
        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)],
                'message': 'Erro interno ao atualizar moto.'
            }

    @staticmethod
    def excluir_moto(request, moto_id: int) -> Dict[str, Any]:
        """
        Serviço para excluir uma moto

        Args:
            request: Request object do Django
            moto_id: ID da moto a ser excluída

        Returns:
            Dict com resultado da operação
        """
        try:
            # Buscar moto
            moto = MotoRepository.get_by_id_and_user(moto_id, request.user)
            if not moto:
                return {
                    'success': False,
                    'message': 'Moto não encontrada.'
                }

            # Guardar nome para mensagem
            nome_moto = moto.modelo

            # Excluir moto
            MotoRepository.delete_moto(moto)

            return {
                'success': True,
                'message': f'Moto "{nome_moto}" foi excluída com sucesso!',
                'redirect_url': '/motos/'
            }

        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)],
                'message': 'Erro interno ao excluir moto.'
            }

    @staticmethod
    def listar_motos_usuario(request) -> Dict[str, Any]:
        """
        Serviço para listar motos do usuário

        Args:
            request: Request object do Django

        Returns:
            Dict com lista de motos
        """
        try:
            motos = MotoRepository.get_all_by_user(request.user)

            return {
                'success': True,
                'motos': motos,
                'total': motos.count()
            }

        except Exception as e:
            return {
                'success': False,
                'errors': [str(e)],
                'message': 'Erro ao carregar lista de motos.'
            }
