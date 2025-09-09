from django.db import models
from django.db.models import Q
from typing import Optional, List
from ..models import Moto


class MotoRepository:
    """Repository para operações de banco de dados da entidade Moto"""

    @staticmethod
    def get_all_by_user(user) -> models.QuerySet:
        """Retorna todas as motos do usuário"""
        return Moto.objects.filter(criado_por=user)

    @staticmethod
    def get_by_id_and_user(moto_id: int, user) -> Optional[Moto]:
        """Retorna uma moto específica do usuário"""
        try:
            return Moto.objects.get(id=moto_id, criado_por=user)
        except Moto.DoesNotExist:
            return None

    @staticmethod
    def create_moto(data: dict, user) -> Moto:
        """Cria uma nova moto"""
        moto = Moto(**data)
        moto.criado_por = user
        moto.save()
        return moto

    @staticmethod
    def update_moto(moto: Moto, data: dict) -> Moto:
        """Atualiza uma moto existente"""
        for field, value in data.items():
            if hasattr(moto, field):
                setattr(moto, field, value)
        moto.save()
        return moto

    @staticmethod
    def delete_moto(moto: Moto) -> None:
        """Exclui uma moto"""
        moto.delete()

    @staticmethod
    def get_active_motos_by_user(user) -> models.QuerySet:
        """Retorna apenas motos ativas do usuário"""
        return Moto.objects.filter(criado_por=user, ativo=True)

    @staticmethod
    def search_motos_by_user(user, search_term: str) -> models.QuerySet:
        """Busca motos por termo de pesquisa"""
        return Moto.objects.filter(
            criado_por=user
        ).filter(
            Q(modelo__icontains=search_term) |
            Q(marca__icontains=search_term) |
            Q(placa__icontains=search_term)
        )
