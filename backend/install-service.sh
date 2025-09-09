#!/bin/bash

# Script de instalação do serviço MotoCare
# Deve ser executado como root ou com sudo

set -e  # Parar em caso de erro

echo "🚀 Instalando serviço MotoCare..."

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script deve ser executado como root (sudo)."
    echo "📝 Uso: sudo ./install-service.sh"
    exit 1
fi

PROJECT_DIR="/home/gfoliveira/Projetos/MotoCare"
SERVICE_FILE="$PROJECT_DIR/motocare.service"
SYSTEMD_DIR="/etc/systemd/system"

# Verificar se os arquivos existem
if [ ! -f "$PROJECT_DIR/motocare-service.sh" ]; then
    echo "❌ Arquivo motocare-service.sh não encontrado."
    exit 1
fi

if [ ! -f "$SERVICE_FILE" ]; then
    echo "❌ Arquivo motocare.service não encontrado."
    exit 1
fi

# Copiar arquivo de serviço para o systemd
echo "📋 Copiando arquivo de serviço..."
cp "$SERVICE_FILE" "$SYSTEMD_DIR/"

# Recarregar configurações do systemd
echo "🔄 Recarregando systemd..."
systemctl daemon-reload

# Habilitar o serviço para iniciar automaticamente
echo "⚙️  Habilitando serviço..."
systemctl enable motocare

# Iniciar o serviço
echo "▶️  Iniciando serviço..."
systemctl start motocare

# Verificar status
echo "📊 Verificando status..."
sleep 3
systemctl status motocare --no-pager

echo ""
echo "✅ Serviço MotoCare instalado com sucesso!"
echo ""
echo "📋 Comandos úteis:"
echo "  sudo systemctl status motocare     # Ver status"
echo "  sudo systemctl stop motocare       # Parar serviço"
echo "  sudo systemctl start motocare      # Iniciar serviço"
echo "  sudo systemctl restart motocare    # Reiniciar serviço"
echo "  sudo systemctl disable motocare    # Desabilitar auto-início"
echo "  sudo systemctl enable motocare     # Habilitar auto-início"
echo ""
echo "📄 Logs do serviço:"
echo "  sudo journalctl -u motocare -f     # Seguir logs em tempo real"
echo "  sudo journalctl -u motocare        # Ver logs históricos"
echo ""
echo "🌐 A aplicação estará disponível em: http://localhost:8000"
