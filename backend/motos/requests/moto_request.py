from django import forms
from django.core.exceptions import ValidationError
from typing import Dict, Any


class CriarMotoRequest:
    """Request para criação de moto com validações específicas"""

    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.cleaned_data = {}
        self.errors = {}

    def is_valid(self) -> bool:
        """Valida os dados da request"""
        try:
            self._validate_required_fields()
            self._validate_modelo()
            self._validate_marca()
            self._validate_ano()
            self._validate_km_atual()
            self._validate_placa()
            self._validate_chassi()
            self._validate_renavam()

            return len(self.errors) == 0

        except Exception as e:
            self.errors['__all__'] = [f'Erro interno de validação: {str(e)}']
            return False

    def _validate_required_fields(self):
        """Valida campos obrigatórios"""
        required_fields = ['modelo', 'marca', 'ano', 'km_atual']

        for field in required_fields:
            if not self.data.get(field):
                self.errors[field] = ['Este campo é obrigatório.']
            else:
                self.cleaned_data[field] = self.data[field].strip()

    def _validate_modelo(self):
        """Valida o campo modelo"""
        if 'modelo' in self.data and self.data['modelo']:
            modelo = self.data['modelo'].strip()
            if len(modelo) < 2:
                self.errors['modelo'] = ['Modelo deve ter pelo menos 2 caracteres.']
            elif len(modelo) > 100:
                self.errors['modelo'] = ['Modelo deve ter no máximo 100 caracteres.']
            else:
                self.cleaned_data['modelo'] = modelo

    def _validate_marca(self):
        """Valida o campo marca"""
        if 'marca' in self.data and self.data['marca']:
            marca = self.data['marca'].strip()
            if len(marca) < 2:
                self.errors['marca'] = ['Marca deve ter pelo menos 2 caracteres.']
            elif len(marca) > 100:
                self.errors['marca'] = ['Marca deve ter no máximo 100 caracteres.']
            else:
                self.cleaned_data['marca'] = marca

    def _validate_ano(self):
        """Valida o campo ano"""
        if 'ano' in self.data and self.data['ano']:
            try:
                ano = int(self.data['ano'])
                if ano < 1900:
                    self.errors['ano'] = ['Ano deve ser maior ou igual a 1900.']
                elif ano > 2030:
                    self.errors['ano'] = ['Ano deve ser menor ou igual a 2030.']
                else:
                    self.cleaned_data['ano'] = ano
            except (ValueError, TypeError):
                self.errors['ano'] = ['Ano deve ser um número válido.']

    def _validate_km_atual(self):
        """Valida o campo km_atual"""
        if 'km_atual' in self.data and self.data['km_atual'] is not None:
            try:
                km = int(self.data['km_atual'])
                if km < 0:
                    self.errors['km_atual'] = ['Quilometragem não pode ser negativa.']
                else:
                    self.cleaned_data['km_atual'] = km
            except (ValueError, TypeError):
                self.errors['km_atual'] = ['Quilometragem deve ser um número válido.']

    def _validate_placa(self):
        """Valida o campo placa"""
        if 'placa' in self.data and self.data['placa']:
            placa = self.data['placa'].strip().upper()
            # Formatos aceitos: AAA-1234 ou AAA1A23
            import re
            if not re.match(r'^[A-Z]{3}-?\d{4}$|^[A-Z]{3}\d[A-Z]\d{2}$', placa):
                self.errors['placa'] = ['Formato de placa inválido. Use AAA-1234 ou AAA1A23.']
            else:
                self.cleaned_data['placa'] = placa

    def _validate_chassi(self):
        """Valida o campo chassi"""
        if 'chassi' in self.data and self.data['chassi']:
            chassi = self.data['chassi'].strip().upper()
            if len(chassi) != 17:
                self.errors['chassi'] = ['Chassi deve ter exatamente 17 caracteres.']
            else:
                self.cleaned_data['chassi'] = chassi

    def _validate_renavam(self):
        """Valida o campo renavam"""
        if 'renavam' in self.data and self.data['renavam']:
            renavam = self.data['renavam'].strip()
            if not renavam.isdigit() or len(renavam) != 11:
                self.errors['renavam'] = ['RENAVAM deve ter exatamente 11 dígitos.']
            else:
                self.cleaned_data['renavam'] = renavam


class AtualizarMotoRequest(CriarMotoRequest):
    """Request para atualização de moto (permite campos opcionais)"""

    def _validate_required_fields(self):
        """Para atualização, campos obrigatórios são opcionais"""
        # Copia todos os campos não vazios
        for field, value in self.data.items():
            if value is not None and value != '':
                if isinstance(value, str):
                    self.cleaned_data[field] = value.strip()
                else:
                    self.cleaned_data[field] = value
