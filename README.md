# Sistema de Manutenção de Motocicletas

Um sistema web completo para gerenciamento de manutenções de motocicletas, desenvolvido com Django.

## 🚀 Funcionalidades

- **Gerenciamento de Motos**: Cadastro completo de motocicletas com informações técnicas
- **Perfil de Uso**: Configuração detalhada do perfil de uso de cada moto
- **Manutenções**: Registro e acompanhamento de manutenções realizadas
- **Análises Inteligentes**: Sistema de diagnóstico e recomendações
- **Dashboard**: Visão geral com métricas e estatísticas
- **Relatórios**: Geração de relatórios detalhados
- **API REST**: Interface para integração com outros sistemas

## 🛠️ Tecnologias Utilizadas

- **Backend**: Django 5.2.6
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Banco de Dados**: SQLite (desenvolvimento) / PostgreSQL (produção)
- **API**: Django REST Framework
- **Autenticação**: Sistema de autenticação do Django
- **Deploy**: Configurado para produção

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Git

## 🚀 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd moto-maintenance
```

### 2. Crie e ative o ambiente virtual
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

### 5. Execute as migrações
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Crie um superusuário
```bash
python manage.py createsuperuser
```

### 7. Execute o servidor

#### Opção 1: Comando manual (tradicional)
```bash
source venv/bin/activate
python manage.py runserver
```

#### Opção 2: Script automático (recomendado) ⭐
```bash
./start.sh
```

#### Opção 3: Servidor em background (desenvolvimento)
```bash
./start_bg.sh  # Inicia em background
./stop.sh      # Para o servidor
```

Acesse: http://localhost:8000

## ⚡ Scripts de Inicialização Rápida

Para facilitar o desenvolvimento, foram criados scripts automatizados:

### `start.sh` - Inicialização Interativa
- Ativa automaticamente o ambiente virtual
- Verifica e executa migrações se necessário
- Coleta arquivos estáticos
- Inicia o servidor em primeiro plano
- **Uso**: `./start.sh`

### `start_bg.sh` - Inicialização em Background
- Inicia o servidor em background
- Salva logs em `server.log`
- Salva PID em `server.pid`
- **Uso**: `./start_bg.sh`

### `stop.sh` - Parar Servidor
- Para o servidor iniciado em background
- Remove arquivos temporários
- **Uso**: `./stop.sh`

### Benefícios dos Scripts:
- ✅ Não precisa ativar venv manualmente
- ✅ Verificações automáticas de dependências
- ✅ Migrações executadas automaticamente
- ✅ Arquivos estáticos coletados
- ✅ Logs organizados
- ✅ Fácil controle de processos

## 🔧 Instalação como Serviço do Sistema

Para transformar o MotoCare em um serviço do sistema que inicia automaticamente:

### Instalação Automática (Recomendado)
```bash
sudo ./install-service.sh
```

### Instalação Manual
```bash
# 1. Copiar arquivo de serviço
sudo cp motocare.service /etc/systemd/system/

# 2. Recarregar systemd
sudo systemctl daemon-reload

# 3. Habilitar serviço
sudo systemctl enable motocare

# 4. Iniciar serviço
sudo systemctl start motocare
```

### Gerenciamento do Serviço
```bash
# Verificar status
sudo systemctl status motocare

# Parar serviço
sudo systemctl stop motocare

# Iniciar serviço
sudo systemctl start motocare

# Reiniciar serviço
sudo systemctl restart motocare

# Ver logs em tempo real
sudo journalctl -u motocare -f

# Ver logs históricos
sudo journalctl -u motocare
```

### Desinstalação do Serviço
```bash
sudo ./uninstall-service.sh
```

### Benefícios do Serviço:
- 🚀 **Inicialização automática** na inicialização do sistema
- 🔄 **Reinicialização automática** em caso de falha
- 📊 **Logs centralizados** no journald
- 🎛️ **Gerenciamento profissional** com systemctl
- 🔒 **Execução segura** com usuário dedicado
- 📈 **Monitoramento de recursos** e limites configurados

## 🔍 Solução de Problemas

### Problemas Comuns do Serviço

#### 1. Serviço não inicia
```bash
# Verificar status detalhado
sudo systemctl status motocare -l

# Verificar logs
sudo journalctl -u motocare -n 50

# Verificar se a porta está livre
sudo netstat -tlnp | grep :8000
```

#### 2. Erro de permissões
```bash
# Verificar permissões dos arquivos
ls -la /home/gfoliveira/Projetos/MotoCare/

# Corrigir permissões se necessário
sudo chown -R gfoliveira:gfoliveira /home/gfoliveira/Projetos/MotoCare/
```

#### 3. Ambiente virtual não encontrado
```bash
# Verificar se o venv existe
ls -la /home/gfoliveira/Projetos/MotoCare/venv/

# Recriar venv se necessário
cd /home/gfoliveira/Projetos/MotoCare
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### 4. Porta já em uso
```bash
# Verificar qual processo está usando a porta
sudo lsof -i :8000

# Matar processo se necessário
sudo kill -9 <PID>

# Ou alterar a porta no arquivo motocare.conf
```

#### 5. Problemas de rede
```bash
# Verificar se o serviço está ouvindo
sudo netstat -tlnp | grep python

# Testar conectividade local
curl http://localhost:8000

# Verificar firewall
sudo ufw status
```

### Comandos Úteis para Debug
```bash
# Ver logs em tempo real
sudo journalctl -u motocare -f

# Ver logs das últimas 24 horas
sudo journalctl -u motocare --since "24 hours ago"

# Reiniciar e ver logs simultaneamente
sudo systemctl restart motocare && sudo journalctl -u motocare -f

# Verificar uso de recursos
sudo systemctl status motocare
ps aux | grep motocare
```

### Arquivos de Log Importantes
- `/var/log/syslog` - Logs do sistema
- `~/Projetos/MotoCare/motocare.log` - Logs específicos da aplicação
- `journalctl -u motocare` - Logs do serviço systemd

## ✅ Verificação e Teste

### Testar se o serviço está funcionando
```bash
# Verificar status
sudo systemctl status motocare

# Testar conectividade
curl http://localhost:8000

# Verificar se está respondendo corretamente
curl -s http://localhost:8000 | head -20
```

### Teste completo da aplicação
```bash
# 1. Verificar se o serviço está ativo
sudo systemctl is-active motocare

# 2. Verificar se a porta está ouvindo
sudo netstat -tlnp | grep :8000

# 3. Testar endpoints principais
curl -s http://localhost:8000/accounts/login/ | grep -i "login"
curl -s http://localhost:8000/static/favicon.ico | wc -c

# 4. Verificar logs por erros
sudo journalctl -u motocare -n 20 | grep -i error
```

### Monitoramento contínuo
```bash
# Monitorar logs em tempo real
sudo journalctl -u motocare -f

# Monitorar recursos usados
watch -n 5 'ps aux | grep motocare && echo "---" && free -h'
```

## 📋 Lista de Arquivos Criados

### Scripts de Inicialização
- `start.sh` - Inicialização interativa
- `start_bg.sh` - Inicialização em background
- `stop.sh` - Parar servidor em background

### Arquivos do Serviço
- `motocare-service.sh` - Script principal do serviço
- `motocare.service` - Arquivo de configuração systemd
- `install-service.sh` - Script de instalação
- `uninstall-service.sh` - Script de desinstalação

### Configurações
- `motocare.conf` - Configurações do serviço
- `motocare.conf.example` - Exemplo de configurações

---

**🎉 Agora você pode gerenciar o MotoCare como um serviço profissional do sistema!**

## 📁 Estrutura do Projeto

```
moto-maintenance/
├── moto_maintenance/          # Configurações principais
│   ├── settings.py           # Configurações do Django
│   ├── urls.py              # URLs principais
│   └── wsgi.py              # Configuração WSGI
├── motos/                    # App de gerenciamento de motos
│   ├── controllers/         # Controladores (lógica de apresentação)
│   ├── repositories/        # Repositórios (acesso a dados)
│   ├── requests/           # Requests (validação de entrada)
│   ├── services/           # Services (lógica de negócio)
│   ├── models.py            # Modelos de dados
│   ├── views.py             # Views e lógica
│   ├── forms.py             # Formulários
│   └── urls.py              # URLs da app
├── manutencoes/             # App de manutenções
├── analises/                 # App de análises
├── dashboard/                # App do dashboard
├── templates/                # Templates HTML
├── static/                   # Arquivos estáticos
├── media/                    # Arquivos de mídia
├── db.sqlite3               # Banco de dados (desenvolvimento)
└── manage.py                # Script de gerenciamento
```

### 🏗️ Arquitetura MVC Organizada

O projeto segue uma arquitetura MVC (Model-View-Controller) organizada com separação clara de responsabilidades:

#### **Controllers** (`controllers/`)
- Controlam o fluxo da aplicação
- Orquestram operações entre Services e Views
- Class-Based Controllers para melhor organização

#### **Services** (`services/`)
- Lógica de negócio centralizada
- Operações complexas e regras de negócio
- Reutilizáveis entre diferentes Controllers

#### **Repositories** (`repositories/`)
- Acesso e manipulação de dados
- Abstração da camada de persistência
- Consultas otimizadas ao banco

#### **Requests** (`requests/`)
- Validação de dados de entrada
- Sanitização e normalização
- Regras de validação personalizadas

### 📋 Benefícios da Arquitetura
- ✅ **Separação de Responsabilidades**
- ✅ **Código Reutilizável**
- ✅ **Fácil Manutenção**
- ✅ **Testabilidade**
- ✅ **Escalabilidade**

## 🔧 Configuração de Produção

### 1. Configurações de Segurança
- Altere `SECRET_KEY` para um valor seguro
- Configure `DEBUG = False`
- Configure `ALLOWED_HOSTS` adequadamente
- Configure HTTPS

### 2. Banco de Dados
Para produção, recomenda-se PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'moto_maintenance',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 3. Servidor Web
Configure um servidor WSGI como Gunicorn:
```bash
pip install gunicorn
gunicorn moto_maintenance.wsgi:application --bind 0.0.0.0:8000
```

## 📊 API Endpoints

### Motos
- `GET /api/motos/` - Lista todas as motos
- `GET /api/motos/{id}/` - Detalhes de uma moto
- `POST /api/motos/{id}/atualizar-km/` - Atualizar quilometragem

### Dashboard
- `GET /api/dashboard/data/` - Dados do dashboard

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte, entre em contato através das issues do GitHub ou envie um email para suporte@motomaintenance.com.

## 🔄 Roadmap

- [ ] Sistema de notificações por email
- [ ] Integração com APIs de concessionárias
- [ ] Aplicativo mobile
- [ ] Análises preditivas com IA
- [ ] Multi-tenant para oficinas

---

**Desenvolvido com ❤️ para apaixonados por motocicletas**
