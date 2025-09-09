#!/bin/bash

# Script de inicialização para o serviço MotoCare
# Este script é usado pelo systemd para iniciar o servidor Django

# Configurações
PROJECT_DIR="/home/gfoliveira/Projetos/MotoCare"
VENV_DIR="$PROJECT_DIR/venv"
LOG_FILE="$PROJECT_DIR/motocare.log"
PID_FILE="$PROJECT_DIR/motocare.pid"

# Função de log
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Verificar se estamos no diretório correto
cd "$PROJECT_DIR" || {
    log "ERRO: Não foi possível acessar o diretório do projeto: $PROJECT_DIR"
    exit 1
}

# Verificar se o manage.py existe
if [ ! -f "manage.py" ]; then
    log "ERRO: Arquivo manage.py não encontrado em $PROJECT_DIR"
    exit 1
fi

# Verificar se o virtualenv existe
if [ ! -d "$VENV_DIR" ]; then
    log "ERRO: Ambiente virtual não encontrado em $VENV_DIR"
    exit 1
fi

# Ativar o ambiente virtual
source "$VENV_DIR/bin/activate" || {
    log "ERRO: Falha ao ativar ambiente virtual"
    exit 1
}

# Verificar se o Django está instalado
if ! python -c "import django" 2>/dev/null; then
    log "ERRO: Django não está instalado no ambiente virtual"
    exit 1
fi

# Configurar Django settings
export DJANGO_SETTINGS_MODULE="moto_maintenance.settings"

# Executar migrações se necessário
log "Verificando migrações..."
python manage.py migrate --check > /dev/null 2>&1
if [ $? -ne 0 ]; then
    log "Executando migrações..."
    python manage.py migrate >> "$LOG_FILE" 2>&1
fi

# Coletar arquivos estáticos
log "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput >> "$LOG_FILE" 2>&1

# Iniciar o servidor
log "Iniciando servidor Django..."
python manage.py runserver 0.0.0.0:8000 >> "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# Salvar o PID
echo $SERVER_PID > "$PID_FILE"
log "Servidor iniciado com PID: $SERVER_PID"

# Aguardar um pouco para verificar se o servidor iniciou corretamente
sleep 3
if kill -0 $SERVER_PID 2>/dev/null; then
    log "Servidor iniciado com sucesso"
else
    log "ERRO: Servidor falhou ao iniciar"
    exit 1
fi

# Manter o script rodando para o systemd
wait $SERVER_PID
