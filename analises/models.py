from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from motos.models import Moto


class AnaliseTecnica(models.Model):
    """Análise técnica da motocicleta"""

    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, related_name='analises_tecnicas')

    # Tipo de análise
    TIPO_CHOICES = [
        ('visual', 'Visual'),
        ('diagnostico', 'Diagnóstico'),
        ('desempenho', 'Desempenho'),
        ('seguranca', 'Segurança'),
        ('completa', 'Completa'),
    ]
    tipo = models.CharField('Tipo de Análise', max_length=20, choices=TIPO_CHOICES, default='completa')

    # Status
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_andamento', 'Em Andamento'),
        ('concluida', 'Concluída'),
        ('cancelada', 'Cancelada'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')

    # Informações básicas
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição', blank=True, null=True)

    # Dados da análise
    dados_analise = models.JSONField('Dados da Análise', blank=True, null=True)

    # Resultados
    resumo = models.TextField('Resumo', blank=True, null=True)
    recomendacoes = models.TextField('Recomendações', blank=True, null=True)

    # Pontuação
    pontuacao_geral = models.DecimalField('Pontuação Geral', max_digits=4, decimal_places=2, blank=True, null=True,
                                        validators=[MinValueValidator(0), MaxValueValidator(10)])

    # Datas
    data_solicitacao = models.DateTimeField('Data da Solicitação', auto_now_add=True)
    data_inicio = models.DateTimeField('Data de Início', blank=True, null=True)
    data_conclusao = models.DateTimeField('Data de Conclusão', blank=True, null=True)

    # Responsável
    responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='analises_responsavel')

    # Observações
    observacoes = models.TextField('Observações', blank=True, null=True)

    # Metadados
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Análise Técnica'
        verbose_name_plural = 'Análises Técnicas'
        ordering = ['-data_solicitacao']

    def __str__(self):
        return f"{self.tipo} - {self.moto} ({self.get_status_display()})"

    @property
    def duracao(self):
        """Retorna a duração da análise em horas"""
        if self.data_inicio and self.data_conclusao:
            return (self.data_conclusao - self.data_inicio).total_seconds() / 3600
        return None

    @property
    def concluida_recentemente(self):
        """Verifica se a análise foi concluída recentemente (últimas 24h)"""
        from datetime import datetime, timedelta
        if self.data_conclusao:
            return (datetime.now() - self.data_conclusao.replace(tzinfo=None)) <= timedelta(hours=24)
        return False


class Diagnostico(models.Model):
    """Diagnósticos identificados na análise"""

    analise = models.ForeignKey(AnaliseTecnica, on_delete=models.CASCADE, related_name='diagnosticos')

    # Tipo de diagnóstico
    TIPO_CHOICES = [
        ('informacao', 'Informação'),
        ('aviso', 'Aviso'),
        ('alerta', 'Alerta'),
        ('critico', 'Crítico'),
    ]
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='informacao')

    # Sistema/componente afetado
    sistema = models.CharField('Sistema/Componente', max_length=100)
    componente = models.CharField('Componente Específico', max_length=100, blank=True, null=True)

    # Descrição
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição')
    causa_provavel = models.TextField('Causa Provável', blank=True, null=True)

    # Severidade e urgência
    severidade = models.PositiveIntegerField('Severidade (1-5)', default=1,
                                           validators=[MinValueValidator(1), MaxValueValidator(5)])
    urgencia = models.CharField('Urgência', max_length=20,
                               choices=[('baixa', 'Baixa'), ('media', 'Média'), ('alta', 'Alta'), ('critica', 'Crítica')],
                               default='baixa')

    # Status
    STATUS_CHOICES = [
        ('identificado', 'Identificado'),
        ('em_analise', 'Em Análise'),
        ('resolvido', 'Resolvido'),
        ('monitorando', 'Monitorando'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='identificado')

    # Solução recomendada
    solucao_recomendada = models.TextField('Solução Recomendada', blank=True, null=True)
    custo_estimado = models.DecimalField('Custo Estimado (R$)', max_digits=10, decimal_places=2, blank=True, null=True)

    # Prazo para resolução
    prazo_dias = models.PositiveIntegerField('Prazo para Resolução (dias)', blank=True, null=True)

    # Observações
    observacoes = models.TextField('Observações', blank=True, null=True)

    # Metadados
    identificado_em = models.DateTimeField('Identificado em', auto_now_add=True)
    resolvido_em = models.DateTimeField('Resolvido em', blank=True, null=True)

    class Meta:
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'
        ordering = ['-severidade', '-identificado_em']

    def __str__(self):
        return f"{self.tipo.upper()} - {self.titulo}"

    @property
    def prazo_expirado(self):
        """Verifica se o prazo para resolução expirou"""
        from datetime import datetime, timedelta
        if self.prazo_dias and self.status != 'resolvido':
            return (datetime.now() - self.identificado_em.replace(tzinfo=None)) > timedelta(days=self.prazo_dias)
        return False


class AnaliseVisual(models.Model):
    """Análise visual da motocicleta"""

    analise = models.OneToOneField(AnaliseTecnica, on_delete=models.CASCADE, related_name='analise_visual')

    # Imagem analisada
    imagem_original = models.ImageField('Imagem Original', upload_to='analises/imagens/')

    # Características técnicas da imagem
    formato_imagem = models.CharField('Formato', max_length=10, blank=True, null=True)
    dimensoes = models.JSONField('Dimensões', blank=True, null=True)  # [altura, largura]
    tamanho_bytes = models.PositiveIntegerField('Tamanho (bytes)', blank=True, null=True)

    # Análise de cores
    cores_principais = models.JSONField('Cores Principais', blank=True, null=True)
    paleta_cores = models.JSONField('Paleta de Cores', blank=True, null=True)

    # Análise técnica
    tipo_imagem = models.CharField('Tipo de Imagem', max_length=50, blank=True, null=True)
    qualidade_imagem = models.CharField('Qualidade', max_length=20,
                                      choices=[('baixa', 'Baixa'), ('media', 'Média'), ('alta', 'Alta')],
                                      blank=True, null=True)

    # Brilho e contraste
    nivel_brilho = models.DecimalField('Nível de Brilho', max_digits=5, decimal_places=2, blank=True, null=True)
    nivel_contraste = models.DecimalField('Nível de Contraste', max_digits=5, decimal_places=2, blank=True, null=True)

    # Detecção de objetos
    objetos_detectados = models.JSONField('Objetos Detectados', blank=True, null=True)

    # Resultados da análise
    resumo_analise = models.TextField('Resumo da Análise', blank=True, null=True)
    observacoes_tecnicas = models.TextField('Observações Técnicas', blank=True, null=True)

    # Metadados
    analisada_em = models.DateTimeField('Analisada em', auto_now_add=True)

    class Meta:
        verbose_name = 'Análise Visual'
        verbose_name_plural = 'Análises Visuais'
        ordering = ['-analisada_em']

    def __str__(self):
        return f"Análise Visual - {self.analise}"


class Recomendacao(models.Model):
    """Recomendações geradas pela análise"""

    analise = models.ForeignKey(AnaliseTecnica, on_delete=models.CASCADE, related_name='recomendacoes_geradas')

    # Tipo de recomendação
    TIPO_CHOICES = [
        ('manutencao', 'Manutenção'),
        ('melhoria', 'Melhoria'),
        ('seguranca', 'Segurança'),
        ('desempenho', 'Desempenho'),
        ('economia', 'Economia'),
    ]
    tipo = models.CharField('Tipo', max_length=20, choices=TIPO_CHOICES, default='manutencao')

    # Prioridade
    PRIORIDADE_CHOICES = [
        ('baixa', 'Baixa'),
        ('media', 'Média'),
        ('alta', 'Alta'),
        ('urgente', 'Urgente'),
    ]
    prioridade = models.CharField('Prioridade', max_length=20, choices=PRIORIDADE_CHOICES, default='media')

    # Conteúdo
    titulo = models.CharField('Título', max_length=200)
    descricao = models.TextField('Descrição')
    justificativa = models.TextField('Justificativa', blank=True, null=True)

    # Implementação
    acoes_recomendadas = models.TextField('Ações Recomendadas')
    prazo_implementacao = models.PositiveIntegerField('Prazo de Implementação (dias)', blank=True, null=True)

    # Custos e benefícios
    custo_estimado = models.DecimalField('Custo Estimado (R$)', max_digits=10, decimal_places=2, blank=True, null=True)
    beneficio_esperado = models.TextField('Benefício Esperado', blank=True, null=True)

    # Status
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('em_implementacao', 'Em Implementação'),
        ('implementada', 'Implementada'),
        ('cancelada', 'Cancelada'),
    ]
    status = models.CharField('Status', max_length=20, choices=STATUS_CHOICES, default='pendente')

    # Datas
    criada_em = models.DateTimeField('Criada em', auto_now_add=True)
    implementada_em = models.DateTimeField('Implementada em', blank=True, null=True)

    # Observações
    observacoes = models.TextField('Observações', blank=True, null=True)

    class Meta:
        verbose_name = 'Recomendação'
        verbose_name_plural = 'Recomendações'
        ordering = ['-prioridade', '-criada_em']

    def __str__(self):
        return f"{self.tipo.upper()} - {self.titulo}"

    @property
    def prazo_expirado(self):
        """Verifica se o prazo de implementação expirou"""
        from datetime import datetime, timedelta
        if self.prazo_implementacao and self.status == 'pendente':
            return (datetime.now() - self.criada_em.replace(tzinfo=None)) > timedelta(days=self.prazo_implementacao)
        return False
