#!/bin/bash

# Script para parar o servidor Django em background

echo "🛑 Parando servidor MotoCare..."

if [ -f "server.pid" ]; then
    PID=$(cat server.pid)
    if kill -0 $PID 2>/dev/null; then
        kill $PID
        echo "✅ Servidor parado (PID: $PID)"
        rm -f server.pid
    else
        echo "⚠️  Servidor não estava rodando"
        rm -f server.pid
    fi
else
    echo "🔍 Procurando processos do servidor..."
    # Tentar encontrar e matar processos do runserver
    PIDS=$(pgrep -f "manage.py runserver")
    if [ ! -z "$PIDS" ]; then
        echo "$PIDS" | xargs kill
        echo "✅ Servidores encontrados e parados"
    else
        echo "ℹ️  Nenhum servidor encontrado rodando"
    fi
fi

echo "✅ Concluído"
