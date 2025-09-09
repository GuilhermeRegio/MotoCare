#!/bin/bash

# Script para iniciar o servidor Django em background
# Útil para desenvolvimento contínuo

echo "🚀 Iniciando MotoCare em background..."

# Verificar se estamos no diretório correto
if [ ! -f "manage.py" ]; then
    echo "❌ Erro: Arquivo manage.py não encontrado."
    exit 1
fi

# Verificar se o virtualenv existe
if [ ! -d "venv" ]; then
    echo "❌ Erro: Ambiente virtual 'venv' não encontrado."
    exit 1
fi

# Ativar o ambiente virtual
source venv/bin/activate

# Verificar se o Django está instalado
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Erro: Django não está instalado."
    exit 1
fi

# Executar migrações se necessário
python manage.py migrate --check > /dev/null 2>&1
if [ $? -ne 0 ]; then
    python manage.py migrate > /dev/null 2>&1
fi

# Coletar arquivos estáticos
python manage.py collectstatic --noinput > /dev/null 2>&1

# Iniciar o servidor em background
echo "🌐 Servidor iniciado em background"
echo "📍 URL: http://localhost:8000"
echo "🛑 Para parar: ./stop.sh ou pkill -f 'manage.py runserver'"

nohup python manage.py runserver 0.0.0.0:8000 > server.log 2>&1 &
echo $! > server.pid

echo "✅ Servidor rodando em background (PID: $(cat server.pid))"
echo "📄 Logs em: server.log"
