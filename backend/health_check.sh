#!/bin/bash

# Script de verificação de saúde do projeto MotoCare
# Usage: ./health_check.sh

echo "🔍 MotoCare - Verificação de Saúde do Projeto"
echo "=============================================="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
total_checks=0
passed_checks=0

check_item() {
    total_checks=$((total_checks + 1))
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
        passed_checks=$((passed_checks + 1))
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

echo ""
echo "📋 Verificando estrutura do projeto..."

# Verificar arquivos essenciais
[ -f "manage.py" ]; check_item $? "Arquivo manage.py existe"
[ -f "requirements.txt" ]; check_item $? "Arquivo requirements.txt existe"
[ -f ".gitignore" ]; check_item $? "Arquivo .gitignore existe"
[ -f "README.md" ]; check_item $? "Arquivo README.md existe"
[ -f ".env.example" ]; check_item $? "Arquivo .env.example existe"

# Verificar estrutura de diretórios
[ -d "moto_maintenance" ]; check_item $? "Diretório moto_maintenance existe"
[ -d "motos" ]; check_item $? "Diretório motos existe"
[ -d "templates" ]; check_item $? "Diretório templates existe"
[ -d "static" ]; check_item $? "Diretório static existe"
[ -d "media" ]; check_item $? "Diretório media existe"

echo ""
echo "🐍 Verificando ambiente Python..."

# Verificar ambiente virtual
[ -d "venv" ]; check_item $? "Ambiente virtual existe"

# Verificar se o ambiente virtual está ativo
if [ -n "$VIRTUAL_ENV" ]; then
    check_item 0 "Ambiente virtual está ativo"
else
    check_item 1 "Ambiente virtual não está ativo"
fi

# Verificar Python
python3 --version > /dev/null 2>&1; check_item $? "Python 3 instalado"
which pip > /dev/null 2>&1; check_item $? "Pip instalado"

echo ""
echo "📦 Verificando dependências..."

# Verificar se Django está instalado
python -c "import django" 2>/dev/null; check_item $? "Django importado com sucesso"

# Verificar versão do Django
if python -c "import django" 2>/dev/null; then
    django_version=$(python -c "import django; print(django.get_version())")
    echo -e "${GREEN}📌 Django versão: $django_version${NC}"
fi

echo ""
echo "🗄️ Verificando banco de dados..."

# Verificar se existem migrações pendentes
if [ -f "manage.py" ]; then
    python manage.py showmigrations --plan 2>/dev/null | grep -q "\\[ \\]"
    if [ $? -eq 0 ]; then
        check_item 1 "Existem migrações pendentes"
    else
        check_item 0 "Todas as migrações aplicadas"
    fi
fi

echo ""
echo "🔒 Verificando segurança..."

# Verificar se DEBUG está desabilitado para produção
if [ -f ".env" ]; then
    if grep -q "DEBUG=False" .env; then
        check_item 0 "DEBUG=False configurado"
    else
        check_item 1 "DEBUG deve ser False em produção"
    fi
else
    echo -e "${YELLOW}⚠️ Arquivo .env não encontrado${NC}"
fi

# Verificar se SECRET_KEY não é a padrão
if [ -f ".env" ]; then
    if grep -q "django-insecure" .env; then
        check_item 1 "SECRET_KEY padrão detectada (insegura)"
    else
        check_item 0 "SECRET_KEY personalizada configurada"
    fi
fi

echo ""
echo "🚀 Verificando scripts de deployment..."

[ -f "start.sh" ] && [ -x "start.sh" ]; check_item $? "Script start.sh executável"
[ -f "start_bg.sh" ] && [ -x "start_bg.sh" ]; check_item $? "Script start_bg.sh executável"
[ -f "stop.sh" ] && [ -x "stop.sh" ]; check_item $? "Script stop.sh executável"

echo ""
echo "🧹 Verificando limpeza do projeto..."

# Verificar se não há __pycache__
find . -name "__pycache__" -not -path "./venv/*" | head -1 | grep -q "__pycache__"
if [ $? -eq 0 ]; then
    check_item 1 "Diretórios __pycache__ encontrados (devem ser removidos)"
else
    check_item 0 "Nenhum __pycache__ encontrado"
fi

# Verificar se não há arquivos .pyc
find . -name "*.pyc" -not -path "./venv/*" | head -1 | grep -q ".pyc"
if [ $? -eq 0 ]; then
    check_item 1 "Arquivos .pyc encontrados (devem ser removidos)"
else
    check_item 0 "Nenhum arquivo .pyc encontrado"
fi

# Verificar se não há arquivos de backup
find . -name "*backup*" -o -name "*.bak" | head -1 | grep -q "backup\|\.bak"
if [ $? -eq 0 ]; then
    check_item 1 "Arquivos de backup encontrados (devem ser removidos)"
else
    check_item 0 "Nenhum arquivo de backup encontrado"
fi

echo ""
echo "📊 Relatório Final"
echo "=================="
echo -e "Total de verificações: $total_checks"
echo -e "${GREEN}Passou: $passed_checks${NC}"
echo -e "${RED}Falhou: $((total_checks - passed_checks))${NC}"

if [ $passed_checks -eq $total_checks ]; then
    echo -e "\n${GREEN}🎉 Projeto está pronto para Git!${NC}"
    exit 0
else
    echo -e "\n${YELLOW}⚠️ Alguns itens precisam de atenção antes do Git${NC}"
    exit 1
fi
