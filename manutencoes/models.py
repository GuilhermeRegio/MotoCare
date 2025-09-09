from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from motos.models import Moto


class TipoManutencao(models.Model):
    """Tipos de manutenção disponíveis"""

    nome = models.CharField('Nome', max_length=100, unique=True)
    descricao = models.TextField('Descrição', blank=True, null=True)
    categoria = models.CharField('Categoria', max_length=50,
                                choices=[('preventiva', 'Preventiva'), ('corretiva', 'Corretiva'), ('melhoria', 'Melhoria')])
    intervalo_km = models.PositiveIntegerField('Intervalo (km)', blank=True, null=True)
    intervalo_meses = models.PositiveIntegerField('Intervalo (meses)', blank=True, null=True)

    # Controle
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Tipo de Manutenção'
        verbose_name_plural = 'Tipos de Manutenção'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class ItemManutencao(models.Model):
    """Itens específicos de manutenção"""

    tipo = models.ForeignKey(TipoManutencao, on_delete=models.CASCADE, related_name='itens')
    nome = models.CharField('Nome do Item', max_length=100)
    descricao = models.TextField('Descrição', blank=True, null=True)

    # Especificações
    marca_recomendada = models.CharField('Marca Recomendada', max_length=50, blank=True, null=True)
    modelo_recomendada = models.CharField('Modelo Recomendado', max_length=100, blank=True, null=True)
    quantidade_padrao = models.DecimalField('Quantidade Padrão', max_digits=8, decimal_places=2, blank=True, null=True)
    unidade_medida = models.CharField('Unidade de Medida', max_length=20, blank=True, null=True)

    # Custos
    valor_estimado = models.DecimalField('Valor Estimado (R$)', max_digits=10, decimal_places=2, blank=True, null=True)

    # Controle
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Item de Manutenção'
        verbose_name_plural = 'Itens de Manutenção'
        ordering = ['tipo', 'nome']
        unique_together = ['tipo', 'nome']

    def __str__(self):
        return f"{self.tipo} - {self.nome}"


class Manutencao(models.Model):
    """Registro de manutenções realizadas ou planejadas"""

    # Relacionamentos
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, related_name='manutencoes')
    tipo = models.ForeignKey(TipoManutencao, on_delete=models.CASCADE, related_name='manutencoes')

    # Status
    STATUS_CHOICES = [
        ('planejada', 'Planejada'),
        ('comprada', 'Itens Comprados'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='planejada')

    # Informações básicas
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição', blank=True, null=True)

    # Quilometragem
    km_atual = models.PositiveIntegerField('Km Atual na Manutenção')
    km_proxima = models.PositiveIntegerField('Km para Próxima Manutenção', blank=True, null=True)

    # Datas
    data_planejada = models.DateField('Data Planejada', blank=True, null=True)
    data_inicio = models.DateTimeField('Data de Início', blank=True, null=True)
    data_conclusao = models.DateTimeField('Data de Conclusão', blank=True, null=True)

    # Localização
    local_manutencao = models.CharField('Local da Manutenção', max_length=100, blank=True, null=True)
    responsavel = models.CharField('Responsável', max_length=100, blank=True, null=True)

    # Custos
    valor_estimado = models.DecimalField('Valor Estimado (R$)', max_digits=10, decimal_places=2, blank=True, null=True)
    valor_real = models.DecimalField('Valor Real (R$)', max_digits=10, decimal_places=2, blank=True, null=True)

    # Observações
    observacoes = models.TextField('Observações', blank=True, null=True)

    # Metadados
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='manutencoes_criadas')

    class Meta:
        verbose_name = 'Manutenção'
        verbose_name_plural = 'Manutenções'
        ordering = ['-data_planejada', '-criado_em']

    def __str__(self):
        return f"{self.tipo} - {self.moto} ({self.get_status_display()})"

    @property
    def duracao(self):
        """Retorna a duração da manutenção em dias"""
        if self.data_inicio and self.data_conclusao:
            return (self.data_conclusao - self.data_inicio).days
        return None

    @property
    def atrasada(self):
        """Verifica se a manutenção está atrasada"""
        from datetime import date
        if self.data_planejada and self.status in ['planejada', 'comprada']:
            return date.today() > self.data_planejada
        return False

    @property
    def km_faltantes(self):
        """Retorna quantos km faltam para a próxima manutenção"""
        if self.km_proxima and self.moto.km_atual < self.km_proxima:
            return self.km_proxima - self.moto.km_atual
        return 0


class ItemManutencaoRealizada(models.Model):
    """Itens específicos utilizados em uma manutenção"""

    manutencao = models.ForeignKey(Manutencao, on_delete=models.CASCADE, related_name='itens_utilizados')
    item = models.ForeignKey(ItemManutencao, on_delete=models.CASCADE, related_name='utilizacoes')

    # Quantidades e valores
    quantidade_utilizada = models.DecimalField('Quantidade Utilizada', max_digits=8, decimal_places=2)
    valor_unitario = models.DecimalField('Valor Unitário (R$)', max_digits=10, decimal_places=2)
    valor_total = models.DecimalField('Valor Total (R$)', max_digits=10, decimal_places=2)

    # Informações específicas
    marca_utilizada = models.CharField('Marca Utilizada', max_length=50, blank=True, null=True)
    modelo_utilizado = models.CharField('Modelo Utilizado', max_length=100, blank=True, null=True)
    fornecedor = models.CharField('Fornecedor', max_length=100, blank=True, null=True)

    # Documentação
    nota_fiscal = models.FileField('Nota Fiscal', upload_to='notas_fiscais/', blank=True, null=True)

    # Observações
    observacoes = models.TextField('Observações', blank=True, null=True)

    class Meta:
        verbose_name = 'Item Utilizado'
        verbose_name_plural = 'Itens Utilizados'
        ordering = ['item__nome']

    def __str__(self):
        return f"{self.item} - {self.manutencao}"

    def save(self, *args, **kwargs):
        """Calcula o valor total automaticamente"""
        self.valor_total = self.quantidade_utilizada * self.valor_unitario
        super().save(*args, **kwargs)


class HistoricoManutencao(models.Model):
    """Histórico detalhado das manutenções realizadas"""

    manutencao = models.OneToOneField(Manutencao, on_delete=models.CASCADE, related_name='historico')

    # Informações técnicas
    sintomas = models.TextField('Sintomas Relatados', blank=True, null=True)
    diagnostico = models.TextField('Diagnóstico', blank=True, null=True)
    procedimentos_realizados = models.TextField('Procedimentos Realizados', blank=True, null=True)

    # Avaliação
    satisfacao = models.PositiveIntegerField('Satisfação (1-5)', blank=True, null=True,
                                           validators=[MinValueValidator(1), MaxValueValidator(5)])
    recomendacao = models.TextField('Recomendação', blank=True, null=True)

    # Fotos e documentos
    fotos_antes = models.ImageField('Fotos Antes', upload_to='manutencao/fotos_antes/', blank=True, null=True)
    fotos_depois = models.ImageField('Fotos Depois', upload_to='manutencao/fotos_depois/', blank=True, null=True)
    relatorio_tecnico = models.FileField('Relatório Técnico', upload_to='manutencao/relatorios/', blank=True, null=True)

    # Metadados
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Histórico de Manutenção'
        verbose_name_plural = 'Históricos de Manutenção'
        ordering = ['-criado_em']

    def __str__(self):
        return f"Histórico - {self.manutencao}"
