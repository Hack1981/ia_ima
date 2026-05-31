import torch
import time
from fastapi import FastAPI, Query
from fastapi.responses import Response, HTMLResponse
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler

# =========================
# APP
# =========================
app = FastAPI()

# =========================
# MODELO
# =========================
model_id = "Lykon/dreamshaper-8"

pipe = StableDiffusionPipeline.from_pretrained(
    model_id,
    torch_dtype=torch.float16,
    safety_checker=None
)

pipe = pipe.to("cuda")

pipe.enable_attention_slicing()
pipe.enable_vae_slicing()

pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(
    pipe.scheduler.config
)

# =========================
# IA GENERATION
# =========================
def gerar(prompt: str):
    negative_prompt = (
        "low quality, blurry, watermark, bad anatomy, deformed, ugly, extra fingers"
    )

    start = time.time()

    with torch.autocast("cuda"):
        image = pipe(
            prompt,
            num_inference_steps=50,
            guidance_scale=8.0,
            height=768,
            width=768,
            negative_prompt=negative_prompt
        ).images[0]

    end = time.time()

    import io
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return buffer.read(), round(end - start, 2)


# =========================
# API ROUTE
# =========================
@app.get("/ia_img")
def ia_img(prompt: str = Query(...)):
    img_bytes, tempo = gerar(prompt)

    # ⚠️ melhor prática: metadata no header
    headers = {
        "X-Generation-Time": str(tempo)
    }

    return Response(content=img_bytes, media_type="image/png", headers=headers)


# =========================
# FRONTEND CHAT
# =========================
@app.get("/", response_class=HTMLResponse)
def home():
    return """
<!DOCTYPE html>
<html lang="pt-br">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IA Image Studio</title>

<style>
    :root {
        --bg-color: #0f172a;
        --chat-bg: #1e293b;
        --accent: #38bdf8;
        --text: #f1f5f9;
    }

    body {
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: var(--bg-color);
        color: var(--text);
        display: flex;
        flex-direction: column;
        height: 100vh;
    }

    .header {
        padding: 20px;
        background: #0f172a;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        border-bottom: 1px solid #334155;
    }

    .chat {
        flex: 1;
        overflow-y: auto;
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .msg {
        background: var(--chat-bg);
        padding: 15px;
        border-radius: 12px;
        border-left: 4px solid var(--accent);
        animation: fadeIn 0.3s ease;
    }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; } }

    img {
        max-width: 100%;
        border-radius: 8px;
        margin-top: 10px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
    }

    .input-bar {
        padding: 20px;
        background: #0f172a;
        display: flex;
        gap: 10px;
        border-top: 1px solid #334155;
    }

    input {
        flex: 1;
        padding: 12px;
        border: 1px solid #334155;
        border-radius: 8px;
        background: #1e293b;
        color: white;
    }

    button {
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        font-weight: bold;
        transition: 0.2s;
    }

    .btn-send { background: var(--accent); color: #000; }
    .btn-send:hover { opacity: 0.9; }
    .btn-clear { background: #ef4444; color: white; }
</style>
</head>

<body>

<div class="header">✨ IA Image Studio</div>

<div class="chat" id="chat"></div>

<div class="input-bar">
    <input id="prompt" placeholder="Descreva a imagem que deseja gerar..." />
    <button class="btn-send" onclick="send()">Gerar</button>
    <button class="btn-clear" onclick="clearChat()">Limpar</button>
</div>

<script>
async function send() {
    let input = document.getElementById("prompt");
    let chat = document.getElementById("chat");
    let prompt = input.value;

    if (!prompt) return;

    // Criar elemento de mensagem
    let msg = document.createElement("div");
    msg.className = "msg";
    msg.innerHTML = "⏳ Gerando: <i>" + prompt + "</i>...";
    chat.appendChild(msg);
    input.value = "";
    chat.scrollTop = chat.scrollHeight;

    try {
        let startTime = Date.now();
        let res = await fetch("/ia_img?prompt=" + encodeURIComponent(prompt));
        let blob = await res.blob();
        let url = URL.createObjectURL(blob);
        let time = ((Date.now() - startTime) / 1000).toFixed(2);

        msg.innerHTML = `
            <div><b>Prompt:</b> ${prompt}</div>
            <div style="font-size: 12px; color: #94a3b8; margin-bottom: 5px;">Tempo: ${time}s</div>
            <img src="${url}" />
        `;
    } catch (e) {
        msg.innerHTML = "❌ Erro ao gerar imagem.";
    }
    chat.scrollTop = chat.scrollHeight;
}

function clearChat() {
    document.getElementById("chat").innerHTML = "";
}
</script>

</body>
</html>
"""

# =========================
# START SERVER (UVICORN)
# =========================
import uvicorn

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8888,
        log_level="info"
    )
