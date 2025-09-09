from rest_framework import serializers
from .models import Moto, PerfilMoto, Rota


class MotoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Moto"""
    
    class Meta:
        model = Moto
        fields = [
            'id', 'modelo', 'marca', 'ano_inicio', 'ano_fim', 'cor',
            'km_atual', 'km_compra', 'cilindrada', 'tipo_motor',
            'tipo_transmissao', 'tipo_combustivel', 'placa', 'chassi',
            'renavam', 'data_compra', 'data_fabricacao', 'imagem_principal',
            'documento_compra', 'ativo', 'observacoes', 'criado_em',
            'atualizado_em', 'criado_por'
        ]
        read_only_fields = ['id', 'criado_em', 'atualizado_em', 'criado_por']
    
    def to_representation(self, instance):
        """Customiza a representação do objeto"""
        data = super().to_representation(instance)
        
        # Adiciona propriedades calculadas
        data['km_total_percorridos'] = instance.km_total_percorridos
        data['idade_anos'] = instance.idade_anos
        data['ano_display'] = instance.ano_display
        
        # Formata datas
        if instance.data_compra:
            data['data_compra_formatada'] = instance.data_compra.strftime('%d/%m/%Y')
        if instance.data_fabricacao:
            data['data_fabricacao_formatada'] = instance.data_fabricacao.strftime('%d/%m/%Y')
            
        # URL da imagem
        if instance.imagem_principal:
            data['imagem_url'] = instance.imagem_principal.url
        
        return data


class PerfilMotoSerializer(serializers.ModelSerializer):
    """Serializer para o modelo PerfilMoto"""
    
    class Meta:
        model = PerfilMoto
        fields = '__all__'
        read_only_fields = ['id', 'criado_em', 'atualizado_em']
    
    def to_representation(self, instance):
        """Customiza a representação do objeto"""
        data = super().to_representation(instance)
        
        # Adiciona propriedades calculadas
        data['calibragem_atualizada'] = instance.calibragem_atualizada
        data['calibragem_dianteira_diferenca'] = float(instance.calibragem_dianteira_diferenca)
        data['calibragem_traseira_diferenca'] = float(instance.calibragem_traseira_diferenca)
        
        return data


class RotaSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Rota"""
    
    class Meta:
        model = Rota
        fields = '__all__'
        read_only_fields = ['id', 'data_registro']


class MotoDetailSerializer(MotoSerializer):
    """Serializer detalhado para Moto com perfil e rotas"""
    
    perfil = PerfilMotoSerializer(read_only=True)
    rotas = RotaSerializer(many=True, read_only=True)
    
    class Meta(MotoSerializer.Meta):
        fields = MotoSerializer.Meta.fields + ['perfil', 'rotas']
