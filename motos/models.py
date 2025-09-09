from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Moto(models.Model):
    """Modelo principal para motocicletas"""

    # Escolhas para marca
    MARCAS_CHOICES = [
        ('Bajaj', 'Bajaj'),
        ('BMW', 'BMW'),
        ('Dafra', 'Dafra'),
        ('Ducati', 'Ducati'),
        ('Harley-Davidson', 'Harley-Davidson'),
        ('Honda', 'Honda'),
        ('Husqvarna', 'Husqvarna'),
        ('Kawasaki', 'Kawasaki'),
        ('KTM', 'KTM'),
        ('Royal Enfield', 'Royal Enfield'),
        ('Shineray', 'Shineray'),
        ('Suzuki', 'Suzuki'),
        ('Triumph', 'Triumph'),
        ('Yamaha', 'Yamaha'),
        ('Outras', 'Outras'),
    ]

    # Escolhas para tipo de motor
    TIPO_MOTOR_CHOICES = [
        ('2 tempos', '2 Tempos'),
        ('4 tempos', '4 Tempos'),
        ('Elétrico', 'Elétrico'),
    ]

    # Escolhas para transmissão
    TIPO_TRANSMISSAO_CHOICES = [
        ('Manual', 'Manual'),
        ('Automática', 'Automática'),
        ('CVT', 'CVT (Variação Contínua)'),
        ('Semi-automática', 'Semi-automática'),
    ]

    # Escolhas para combustível
    TIPO_COMBUSTIVEL_CHOICES = [
        ('Gasolina', 'Gasolina'),
        ('Etanol', 'Etanol'),
        ('Flex', 'Flex (Gasolina/Etanol)'),
        ('Elétrico', 'Elétrico'),
        ('Diesel', 'Diesel'),
    ]

    # Escolhas para cores
    COR_CHOICES = [
        ('Preto', 'Preto'),
        ('Branco', 'Branco'),
        ('Prata', 'Prata'),
        ('Azul', 'Azul'),
        ('Vermelho', 'Vermelho'),
        ('Verde', 'Verde'),
        ('Amarelo', 'Amarelo'),
        ('Laranja', 'Laranja'),
        ('Cinza', 'Cinza'),
        ('Dourado', 'Dourado'),
        ('Roxo', 'Roxo'),
        ('Rosa', 'Rosa'),
        ('Outras', 'Outras'),
    ]

    # Escolhas para cilindrada
    CILINDRADA_CHOICES = [
        (50, '50cc'),
        (100, '100cc'),
        (110, '110cc'),
        (125, '125cc'),
        (150, '150cc'),
        (160, '160cc'),
        (200, '200cc'),
        (250, '250cc'),
        (300, '300cc'),
        (400, '400cc'),
        (500, '500cc'),
        (600, '600cc'),
        (650, '650cc'),
        (750, '750cc'),
        (800, '800cc'),
        (900, '900cc'),
        (1000, '1000cc'),
        (1200, '1200cc'),
        (1300, '1300cc'),
        (1500, '1500cc'),
        (1800, '1800cc'),
    ]

    # Informações básicas
    modelo = models.CharField('Modelo', max_length=100, default='Dafra Cruisym 300')
    marca = models.CharField('Marca', max_length=50, choices=MARCAS_CHOICES, default='Dafra')
    ano_inicio = models.PositiveIntegerField('Ano Início', default=2024, validators=[MinValueValidator(1900), MaxValueValidator(2030)])
    ano_fim = models.PositiveIntegerField('Ano Fim', blank=True, null=True, validators=[MinValueValidator(1900), MaxValueValidator(2030)])
    cor = models.CharField('Cor', max_length=50, choices=COR_CHOICES, blank=True, null=True)

    # Quilometragem
    km_atual = models.PositiveIntegerField('Km Atual', default=0)
    km_compra = models.PositiveIntegerField('Km na Compra', default=0)

    # Informações técnicas
    cilindrada = models.PositiveIntegerField('Cilindrada (cc)', choices=CILINDRADA_CHOICES, default=300)
    tipo_motor = models.CharField('Tipo de Motor', max_length=50, choices=TIPO_MOTOR_CHOICES, default='4 tempos')
    tipo_transmissao = models.CharField('Transmissão', max_length=50, choices=TIPO_TRANSMISSAO_CHOICES, default='Manual')
    tipo_combustivel = models.CharField('Combustível', max_length=20, choices=TIPO_COMBUSTIVEL_CHOICES, default='Gasolina')

    # Documentação
    placa = models.CharField('Placa', max_length=10, blank=True, null=True)
    chassi = models.CharField('Chassi', max_length=50, blank=True, null=True)
    renavam = models.CharField('Renavam', max_length=20, blank=True, null=True)

    # Datas importantes
    data_compra = models.DateField('Data da Compra', blank=True, null=True)
    data_fabricacao = models.DateField('Data de Fabricação', blank=True, null=True)

    # Imagens e documentos
    imagem_principal = models.ImageField('Imagem Principal', upload_to='motos/', blank=True, null=True)
    documento_compra = models.FileField('Documento de Compra', upload_to='documentos/', blank=True, null=True)

    # Controle
    ativo = models.BooleanField('Ativo', default=True)
    observacoes = models.TextField('Observações', blank=True, null=True)

    # Metadados
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)
    criado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='motos_criadas')

    class Meta:
        verbose_name = 'Moto'
        verbose_name_plural = 'Motos'
        ordering = ['-criado_em']

    def __str__(self):
        if self.ano_fim:
            return f"{self.marca} {self.modelo} ({self.ano_inicio}/{self.ano_fim})"
        return f"{self.marca} {self.modelo} ({self.ano_inicio})"

    @property
    def km_total_percorridos(self):
        """Retorna o total de km percorridos desde a compra"""
        return self.km_atual - self.km_compra

    @property
    def idade_anos(self):
        """Retorna a idade da moto em anos"""
        from datetime import date
        if self.data_fabricacao:
            return date.today().year - self.data_fabricacao.year
        return date.today().year - self.ano_inicio

    @property
    def ano_display(self):
        """Retorna a formatação do ano para exibição"""
        if self.ano_fim:
            return f"{self.ano_inicio}/{self.ano_fim}"
        return str(self.ano_inicio)


class PerfilMoto(models.Model):
    """Perfil de uso e características da motocicleta"""

    # Relacionamento
    moto = models.OneToOneField(Moto, on_delete=models.CASCADE, related_name='perfil')

    # Perfil do condutor
    peso_condutor = models.DecimalField('Peso do Condutor (kg)', max_digits=5, decimal_places=2, default=75.0)
    altura_condutor = models.DecimalField('Altura do Condutor (cm)', max_digits=5, decimal_places=2, blank=True, null=True)

    # Capacidade de carga
    capacidade_carga = models.DecimalField('Capacidade de Carga (kg)', max_digits=5, decimal_places=2, default=180.0)

    # Características técnicas
    tipo_pneu = models.CharField('Tipo de Pneu', max_length=20, default='urbano',
                                choices=[('urbano', 'Urbano'), ('misto', 'Misto'), ('off_road', 'Off-Road')])
    tamanho_aro_dianteira = models.CharField('Aro Dianteiro', max_length=10, default='17"')
    tamanho_aro_traseira = models.CharField('Aro Traseiro', max_length=10, default='17"')

    # Estilo de uso
    estilo_uso = models.CharField('Estilo de Uso', max_length=20, default='urbano',
                                 choices=[('urbano', 'Urbano'), ('estrada', 'Estrada'), ('off_road', 'Off-Road'), ('esportivo', 'Esportivo')])
    frequencia_uso = models.CharField('Frequência de Uso', max_length=20, default='diario',
                                     choices=[('diario', 'Diário'), ('semanal', 'Semanal'), ('quinzenal', 'Quinzenal'), ('mensal', 'Mensal')])

    # Distância e velocidade
    distancia_media_dia = models.DecimalField('Distância Média/Dia (km)', max_digits=6, decimal_places=2, default=25.0)
    velocidade_media = models.DecimalField('Velocidade Média (km/h)', max_digits=5, decimal_places=2, default=35.0)

    # Condições de uso
    tipo_via_predominante = models.CharField('Tipo de Via Predominante', max_length=20, default='cidade',
                                           choices=[('cidade', 'Cidade'), ('estrada', 'Estrada'), ('misto', 'Misto')])
    condicoes_via = models.CharField('Condições da Via', max_length=20, default='regular',
                                    choices=[('excelente', 'Excelente'), ('regular', 'Regular'), ('ruim', 'Ruim')])
    clima_predominante = models.CharField('Clima Predominante', max_length=20, default='seco',
                                         choices=[('seco', 'Seco'), ('umido', 'Úmido'), ('quente', 'Quente'), ('frio', 'Frio')])

    # Calibragem recomendada
    calibragem_recomendada_dianteira = models.DecimalField('Calibragem Recomendada Dianteira (PSI)', max_digits=4, decimal_places=2, default=2.2)
    calibragem_recomendada_traseira = models.DecimalField('Calibragem Recomendada Traseira (PSI)', max_digits=4, decimal_places=2, default=2.0)

    # Calibragem atual
    calibragem_atual_dianteira = models.DecimalField('Calibragem Atual Dianteira (PSI)', max_digits=4, decimal_places=2, default=2.0)
    calibragem_atual_traseira = models.DecimalField('Calibragem Atual Traseira (PSI)', max_digits=4, decimal_places=2, default=2.0)
    ultima_calibragem = models.DateField('Última Calibragem', blank=True, null=True)

    # Imagens e documentos adicionais
    imagem_perfil = models.ImageField('Imagem do Perfil', upload_to='perfis/', blank=True, null=True)
    documento_perfil = models.FileField('Documento do Perfil', upload_to='documentos/', blank=True, null=True)

    # Observações
    observacoes_perfil = models.TextField('Observações do Perfil', blank=True, null=True)

    # Metadados
    criado_em = models.DateTimeField('Criado em', auto_now_add=True)
    atualizado_em = models.DateTimeField('Atualizado em', auto_now=True)

    class Meta:
        verbose_name = 'Perfil da Moto'
        verbose_name_plural = 'Perfis das Motos'
        ordering = ['-atualizado_em']

    def __str__(self):
        return f"Perfil de {self.moto}"

    @property
    def calibragem_atualizada(self):
        """Verifica se a calibragem está atualizada (últimos 30 dias)"""
        from datetime import date, timedelta
        if not self.ultima_calibragem:
            return False
        return (date.today() - self.ultima_calibragem) <= timedelta(days=30)

    @property
    def calibragem_dianteira_diferenca(self):
        """Diferença entre calibragem atual e recomendada (dianteira)"""
        return self.calibragem_atual_dianteira - self.calibragem_recomendada_dianteira

    @property
    def calibragem_traseira_diferenca(self):
        """Diferença entre calibragem atual e recomendada (traseira)"""
        return self.calibragem_atual_traseira - self.calibragem_recomendada_traseira


class Rota(models.Model):
    """Rotas frequentes da motocicleta"""

    moto = models.ForeignKey(Moto, on_delete=models.CASCADE, related_name='rotas')

    # Informações da rota
    nome_rota = models.CharField('Nome da Rota', max_length=100)
    tipo_via = models.CharField('Tipo de Via', max_length=20, default='cidade',
                               choices=[('cidade', 'Cidade'), ('estrada', 'Estrada'), ('misto', 'Misto')])
    distancia_km = models.DecimalField('Distância (km)', max_digits=6, decimal_places=2)
    tempo_estimado = models.DurationField('Tempo Estimado', blank=True, null=True)
    velocidade_media = models.DecimalField('Velocidade Média (km/h)', max_digits=5, decimal_places=2, default=35.0)

    # Condições
    condicoes_via = models.CharField('Condições da Via', max_length=20, default='regular',
                                    choices=[('excelente', 'Excelente'), ('regular', 'Regular'), ('ruim', 'Ruim')])
    clima = models.CharField('Clima', max_length=20, default='seco',
                            choices=[('seco', 'Seco'), ('umido', 'Úmido'), ('quente', 'Quente'), ('frio', 'Frio')])
    frequencia_semanal = models.PositiveIntegerField('Frequência Semanal', default=1, validators=[MinValueValidator(1), MaxValueValidator(7)])

    # Observações
    observacoes = models.TextField('Observações', blank=True, null=True)

    # Metadados
    data_registro = models.DateTimeField('Data de Registro', auto_now_add=True)
    ativo = models.BooleanField('Ativo', default=True)

    class Meta:
        verbose_name = 'Rota'
        verbose_name_plural = 'Rotas'
        ordering = ['-data_registro']
        unique_together = ['moto', 'nome_rota']

    def __str__(self):
        return f"{self.nome_rota} - {self.moto}"
