#!/bin/bash

clear

echo "===================================="
echo "🚀 Iniciando IA Image Studio"
echo "===================================="
echo ""

# =========================
# INICIA API
# =========================
echo "📦 Iniciando servidor Python..."
nohup python3 main.py > app.log 2>&1 &

sleep 3

# =========================
# INICIA CLOUDFLARE (SILENCIOSO)
# =========================
echo "⏳ Subindo Cloudflare Tunnel..."
nohup ./cloudflared tunnel --url http://localhost:8888 > cloudflared.log 2>&1 &

sleep 6

# =========================
# URL
# =========================
echo ""
echo "🔗 URL pública (Cloudflare):"
echo ""

URL=$(grep -o "https://.*trycloudflare.com" cloudflared.log | head -n 1)

echo "$URL"
echo ""

echo "===================================="
echo "📡 Logs do servidor (main.py):"
echo "===================================="
echo ""

# =========================
# SÓ LOG DO MAIN.PY
# =========================
tail -f app.log
