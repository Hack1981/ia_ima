#!/bin/bash

echo "🧹 Limpando versões antigas..."
pip uninstall -y torch torchvision torchaudio

echo "📦 Instalando PyTorch CUDA 12.4..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

echo "📦 Instalando dependências..."
pip install diffusers transformers accelerate fastapi uvicorn

echo "🌐 Baixando cloudflared..."
wget -O cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64

chmod +x cloudflared

echo "✅ Instalação concluída"
