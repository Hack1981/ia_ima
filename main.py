import torch
import time
from fastapi import FastAPI, Query
from fastapi.responses import Response, HTMLResponse
from diffusers import StableDiffusionPipeline, EulerAncestralDiscreteScheduler
from pathlib import Path
from fastapi.responses import HTMLResponse

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
    with open("index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

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
