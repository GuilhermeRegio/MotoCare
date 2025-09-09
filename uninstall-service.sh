#!/bin/bash

# Script de desinstalação do serviço MotoCare
# Deve ser executado como root ou com sudo

set -e  # Parar em caso de erro

echo "🛑 Desinstalando serviço MotoCare..."

# Verificar se está rodando como root
if [ "$EUID" -ne 0 ]; then
    echo "❌ Este script deve ser executado como root (sudo)."
    echo "📝 Uso: sudo ./uninstall-service.sh"
    exit 1
fi

SERVICE_NAME="motocare"
SYSTEMD_DIR="/etc/systemd/system"
SERVICE_FILE="$SYSTEMD_DIR/$SERVICE_NAME.service"

# Parar o serviço se estiver rodando
echo "🛑 Parando serviço..."
systemctl stop "$SERVICE_NAME" 2>/dev/null || true

# Desabilitar o serviço
echo "⚙️  Desabilitando serviço..."
systemctl disable "$SERVICE_NAME" 2>/dev/null || true

# Remover arquivo de serviço
if [ -f "$SERVICE_FILE" ]; then
    echo "🗑️  Removendo arquivo de serviço..."
    rm "$SERVICE_FILE"
fi

# Recarregar configurações do systemd
echo "🔄 Recarregando systemd..."
systemctl daemon-reload

# Remover arquivos de log e PID se existirem
PROJECT_DIR="/home/gfoliveira/Projetos/MotoCare"
rm -f "$PROJECT_DIR/motocare.log" "$PROJECT_DIR/motocare.pid" "$PROJECT_DIR/server.log" "$PROJECT_DIR/server.pid"

echo ""
echo "✅ Serviço MotoCare desinstalado com sucesso!"
echo ""
echo "💡 Para reinstalar:"
echo "  sudo ./install-service.sh"
