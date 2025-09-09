from django import forms
from .models import Moto, PerfilMoto, Rota


class MotoForm(forms.ModelForm):
    """Formulário para Moto"""

    class Meta:
        model = Moto
        fields = [
            'modelo', 'marca', 'ano_inicio', 'ano_fim', 'cor', 'km_atual', 'km_compra',
            'cilindrada', 'tipo_motor', 'tipo_transmissao', 'tipo_combustivel',
            'placa', 'chassi', 'renavam', 'data_compra', 'data_fabricacao',
            'imagem_principal', 'documento_compra', 'observacoes', 'ativo'
        ]
        widgets = {
            'data_compra': forms.DateInput(attrs={'type': 'date'}),
            'data_fabricacao': forms.DateInput(attrs={'type': 'date'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tornar apenas campos essenciais obrigatórios
        self.fields['modelo'].required = True
        self.fields['marca'].required = True
        self.fields['ano_inicio'].required = True
        self.fields['km_atual'].required = True

        # Campos com valores padrão não precisam ser obrigatórios
        self.fields['ano_fim'].required = False
        self.fields['km_compra'].required = False
        self.fields['cilindrada'].required = False
        self.fields['tipo_motor'].required = False
        self.fields['tipo_transmissao'].required = False
        self.fields['tipo_combustivel'].required = False

        # Definir valores iniciais para campos não obrigatórios
        if not self.instance.pk:  # Apenas para novos registros
            self.fields['km_compra'].initial = 0
            self.fields['cilindrada'].initial = 300
            self.fields['tipo_motor'].initial = '4 tempos'
            self.fields['tipo_transmissao'].initial = 'Manual'
            self.fields['tipo_combustivel'].initial = 'Gasolina'

        # Adicionar classes CSS do Bootstrap a todos os campos
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control', 'rows': 3})
            elif isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({'class': 'form-control'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

        # Adicionar placeholders (apenas para campos de texto livre)
        self.fields['modelo'].widget.attrs.update({'placeholder': 'Ex: Cruisym 300'})
        self.fields['ano_inicio'].widget.attrs.update({'placeholder': '2024'})
        self.fields['ano_fim'].widget.attrs.update({'placeholder': 'Ex: 2024 (opcional)'})
        self.fields['placa'].widget.attrs.update({'placeholder': 'Ex: ABC-1234'})
        self.fields['chassi'].widget.attrs.update({'placeholder': 'Número do chassi'})
        self.fields['renavam'].widget.attrs.update({'placeholder': 'Número do Renavam'})
        
        # Adicionar help texts
        self.fields['documento_compra'].help_text = 'Carregue aqui o documento de compra da moto (PDF, JPG, PNG)'


class PerfilMotoForm(forms.ModelForm):
    """Formulário para Perfil da Moto"""

    class Meta:
        model = PerfilMoto
        fields = [
            'peso_condutor', 'altura_condutor', 'capacidade_carga',
            'tipo_pneu', 'tamanho_aro_dianteira', 'tamanho_aro_traseira',
            'estilo_uso', 'frequencia_uso', 'distancia_media_dia', 'velocidade_media',
            'tipo_via_predominante', 'condicoes_via', 'clima_predominante',
            'calibragem_recomendada_dianteira', 'calibragem_recomendada_traseira',
            'calibragem_atual_dianteira', 'calibragem_atual_traseira', 'ultima_calibragem',
            'imagem_perfil', 'documento_perfil', 'observacoes_perfil'
        ]
        widgets = {
            'ultima_calibragem': forms.DateInput(attrs={'type': 'date'}),
            'observacoes_perfil': forms.Textarea(attrs={'rows': 3}),
        }


class RotaForm(forms.ModelForm):
    """Formulário para Rota"""

    class Meta:
        model = Rota
        fields = [
            'nome_rota', 'tipo_via', 'distancia_km', 'tempo_estimado',
            'velocidade_media', 'condicoes_via', 'clima', 'frequencia_semanal',
            'observacoes'
        ]
        widgets = {
            'tempo_estimado': forms.TimeInput(attrs={'type': 'time'}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }
