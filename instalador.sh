#!/bin/bash

echo "🔍 Verificando instalação do PyTorch..."

PYTORCH_OK=false

if python3 -c "import torch; print(torch.__version__)" 2>/dev/null; then
    TORCH_VERSION=$(python3 -c "import torch; print(torch.__version__)")
    CUDA_VERSION=$(python3 -c "import torch; print(torch.version.cuda)")

    echo "📦 Torch instalado: $TORCH_VERSION (CUDA: $CUDA_VERSION)"

    if [[ "$CUDA_VERSION" == "12.4" ]]; then
        echo "✅ PyTorch já está com CUDA 12.4. Pulando instalação."
        PYTORCH_OK=true
    else
        echo "⚠️ CUDA diferente de 12.4. Reinstalando..."
    fi
else
    echo "⚠️ PyTorch não instalado."
fi

if [ "$PYTORCH_OK" = false ]; then
    echo "🧹 Limpando versões antigas..."
    pip uninstall -y torch torchvision torchaudio

    echo "📦 Instalando PyTorch CUDA 12.4..."
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124
fi

echo "📦 Verificando dependências Python..."

REQS="diffusers transformers accelerate fastapi uvicorn"

for pkg in $REQS; do
    python3 -c "import $pkg" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "⬇️ Instalando $pkg..."
        pip install $pkg
    else
        echo "✅ $pkg já instalado"
    fi
done

echo "🌐 Baixando cloudflared..."

if [ ! -f cloudflared ]; then
    wget -O cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
    chmod +x cloudflared
    echo "✅ cloudflared instalado"
else
    echo "✅ cloudflared já existe"
fi

echo "🎉 Finalizado"
