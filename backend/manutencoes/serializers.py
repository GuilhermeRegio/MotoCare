"""
Serializers for Manutencoes app.
"""
from rest_framework import serializers
from .models import Manutencao


class ManutencaoSerializer(serializers.ModelSerializer):
    """
    Serializer for Manutencao model.
    """
    
    class Meta:
        model = Manutencao
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']
    
    def to_representation(self, instance):
        """
        Customize object representation.
        """
        data = super().to_representation(instance)
        
        # Format dates
        if instance.data_manutencao:
            data['data_manutencao_formatada'] = instance.data_manutencao.strftime('%d/%m/%Y')
        
        # Add motorcycle info
        if instance.moto:
            data['moto_info'] = {
                'id': instance.moto.id,
                'modelo': instance.moto.modelo,
                'marca': instance.moto.marca,
                'placa': instance.moto.placa,
            }
        
        return data
