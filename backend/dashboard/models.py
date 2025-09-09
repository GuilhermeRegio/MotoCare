from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from motos.models import Moto


class Metrica(models.Model):
    """Métricas gerais do sistema"""

    # Tipo de métrica
    TIPO_CHOICES = [
        ('financeiro', 'Financeiro'),
        ('manutencao', 'Manutenção'),
        ('desempenho', 'Desempenho'),
        ('seguranca', 'Segurança'),
        ('consumo', 'Consumo'),
    ]
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES)

    # Identificador único
    chave = models.CharField('Chave', max_length=100, unique=True)
    nome = models.CharField('Nome', max_length=200)
    descricao = models.TextField('Descrição', blank=True, null=True)

    # Unidade de medida
    unidade = models.CharField('Unidade', max_length=20, blank=True, null=True)

    # Controle
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Métrica'
        verbose_name_plural = 'Métricas'
        ordering = ['tipo', 'nome']

    def __str__(self):
        return f"{self.nome} ({self.unidade or 'N/A'})"


class ValorMetrica(models.Model):
    """Valores das métricas ao longo do tempo"""

    metrica = models.ForeignKey(Metrica, on_delete=models.CASCADE, related_name='valores')
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, related_name='metricas', blank=True, null=True)

    # Valor
    valor = models.DecimalField('Valor', max_digits=15, decimal_places=4)
    valor_texto = models.CharField('Valor Texto', max_length=100, blank=True, null=True)

    # Período
    data_referencia = models.DateField('Data de Referência')
    periodo = models.CharField('Período', max_length=20,
                              choices=[('diario', 'Diário'), ('semanal', 'Semanal'), ('mensal', 'Mensal'), ('anual', 'Anual')],
                              default='mensal')

    # Contexto adicional
    contexto = models.JSONField('Contexto', blank=True, null=True)

    # Metadados
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Valor de Métrica'
        verbose_name_plural = 'Valores de Métricas'
        ordering = ['-data_referencia', '-criado_em']
        unique_together = ['metrica', 'moto', 'data_referencia', 'periodo']

    def __str__(self):
        return f"{self.metrica} - {self.valor} ({self.data_referencia})"


class Dashboard(models.Model):
    """Configurações personalizadas do dashboard"""

    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dashboard')
    moto_principal = models.ForeignKey(Moto, on_delete=models.SET_NULL, null=True, blank=True, related_name='dashboard_principal')

    # Configurações de exibição
    metricas_favoritas = models.JSONField('Métricas Favoritas', blank=True, null=True)
    widgets_visiveis = models.JSONField('Widgets Visíveis', blank=True, null=True)

    # Período padrão
    periodo_padrao = models.CharField('Período Padrão', max_length=20,
                                     choices=[('7d', '7 dias'), ('30d', '30 dias'), ('90d', '90 dias'), ('1y', '1 ano')],
                                     default='30d')

    # Tema e layout
    tema = models.CharField('Tema', max_length=20,
                           choices=[('claro', 'Claro'), ('escuro', 'Escuro'), ('auto', 'Automático')],
                           default='auto')
    layout = models.CharField('Layout', max_length=20,
                             choices=[('grid', 'Grid'), ('lista', 'Lista'), ('compacto', 'Compacto')],
                             default='grid')

    # Notificações
    notificacoes_ativas = models.BooleanField('Notificações Ativas', default=True)
    email_alertas = models.BooleanField('Alertas por Email', default=False)

    # Metadados
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Dashboard'
        verbose_name_plural = 'Dashboards'
        ordering = ['-atualizado_em']

    def __str__(self):
        return f"Dashboard de {self.usuario}"


class Alerta(models.Model):
    """Alertas e notificações do sistema"""

    # Destinatário
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alertas')
    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, related_name='alertas', blank=True, null=True)

    # Tipo de alerta
    TIPO_CHOICES = [
        ('manutencao', 'Manutenção'),
        ('seguranca', 'Segurança'),
        ('desempenho', 'Desempenho'),
        ('financeiro', 'Financeiro'),
        ('sistema', 'Sistema'),
    ]
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES)

    # Severidade
    SEVERIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]
    severidade = models.CharField('Severidade', max_length=20, choices=SEVERIDADE_CHOICES, default='media')

    # Conteúdo
    titulo = models.CharField('Título', max_length=200)
    mensagem = models.TextField('Mensagem')
    descricao = models.TextField('Descrição', blank=True, null=True)

    # Status
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('lido', 'Lido'),
        ('resolvido', 'Resolvido'),
        ('ignorado', 'Ignorado'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='ativo')

    # Ação recomendada
    acao_recomendada = models.TextField('Ação Recomendada', blank=True, null=True)
    link_acao = models.URLField('Link para Ação', blank=True, null=True)

    # Datas
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    lido_em = models.DateTimeField('Lido em', blank=True, null=True)
    resolvido_em = models.DateTimeField('Resolvido em', blank=True, null=True)

    # Controle de recorrência
    recorrente = models.BooleanField('Recorrente', default=False)
    intervalo_recorrencia = models.PositiveIntegerField('Intervalo de Recorrência (dias)', blank=True, null=True)

    class Meta:
        verbose_name = 'Alerta'
        verbose_name_plural = 'Alertas'
        ordering = ['-severidade', '-criado_em']

    def __str__(self):
        return f"{self.tipo.upper()} - {self.titulo}"

    @property
    def ativo(self):
        """Verifica se o alerta ainda está ativo"""
        return self.status in ['ativo', 'lido']


class Relatorio(models.Model):
    """Relatórios gerados pelo sistema"""

    # Autor
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='relatorios')

    # Tipo de relatório
    TIPO_CHOICES = [
        ('manutencao', 'Manutenção'),
        ('financeiro', 'Financeiro'),
        ('desempenho', 'Desempenho'),
        ('analise', 'Análise'),
        ('completo', 'Completo'),
    ]
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES)

    # Período
    data_inicio = models.DateField('Data de Início')
    data_fim = models.DateField('Data de Fim')

    # Filtros aplicados
    filtros = models.JSONField('Filtros Aplicados', blank=True, null=True)

    # Conteúdo
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição', blank=True, null=True)

    # Arquivo gerado
    arquivo_pdf = models.FileField('Arquivo PDF', upload_to='relatorios/', blank=True, null=True)
    arquivo_excel = models.FileField('Arquivo Excel', upload_to='relatorios/', blank=True, null=True)

    # Status
    STATUS_CHOICES = [
        ('gerando', 'Gerando'),
        ('concluido', 'Concluído'),
        ('erro', 'Erro'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='gerando')

    # Estatísticas
    total_registros = models.PositiveIntegerField('Total de Registros', blank=True, null=True)
    tempo_geracao = models.DurationField('Tempo de Geração', blank=True, null=True)

    # Metadados
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    concluido_em = models.DateTimeField('Concluído em', blank=True, null=True)

    class Meta:
        verbose_name = 'Relatório'
        verbose_name_plural = 'Relatórios'
        ordering = ['-criado_em']

    def __str__(self):
        return f"{self.tipo.upper()} - {self.titulo}"

    @property
    def periodo_dias(self):
        """Retorna o período do relatório em dias"""
        if self.data_inicio and self.data_fim:
            return (self.data_fim - self.data_inicio).days
        return None
