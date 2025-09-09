#!/bin/bash

# Script para iniciar o servidor Django automaticamente
# MotoCare - Sistema de Manutenção de Motocicletas

echo "🚀 Iniciando MotoCare..."

# Verificar se estamos no diretório correto
if [ ! -f "manage.py" ]; then
    echo "❌ Erro: Arquivo manage.py não encontrado. Execute este script do diretório raiz do projeto."
    exit 1
fi

# Verificar se o virtualenv existe
if [ ! -d "venv" ]; then
    echo "❌ Erro: Ambiente virtual 'venv' não encontrado."
    echo "📝 Execute: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Ativar o ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Verificar se o Django está instalado
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Erro: Django não está instalado no ambiente virtual."
    echo "📝 Execute: pip install -r requirements.txt"
    exit 1
fi

# Executar migrações se necessário
echo "📊 Verificando migrações..."
python manage.py migrate --check > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "🔄 Executando migrações..."
    python manage.py migrate
fi

# Coletar arquivos estáticos
echo "📁 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput > /dev/null 2>&1

# Iniciar o servidor
echo "🌐 Iniciando servidor Django..."
echo "📍 URL: http://localhost:8000"
echo "🛑 Para parar o servidor: Ctrl+C"
echo ""

python manage.py runserver 0.0.0.0:8000
