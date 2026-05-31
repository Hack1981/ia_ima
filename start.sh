#!/bin/bash

echo "🚀 Iniciando IA Image Studio..."

# inicia API com nohup
nohup python3 main.py > app.log 2>&1 &

echo "⏳ Subindo Cloudflare Tunnel..."

# inicia tunnel com nohup
nohup ./cloudflared tunnel --url http://localhost:8888 > cloudflared.log 2>&1 &

sleep 6

echo ""
echo "🔗 URL pública (Cloudflare):"
grep -o "https://.*trycloudflare.com" cloudflared.log | head -n 1

echo ""
echo "📡 Logs do tunnel:"
tail -f cloudflared.log
