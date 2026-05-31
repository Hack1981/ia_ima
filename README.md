# ✨ IA Image Studio

Sistema de geração de imagens com IA usando **Stable Diffusion + FastAPI + Interface Web interativa**.

---

## 🚀 Visão geral

Este projeto cria uma API + interface web onde você pode:

* Gerar imagens a partir de prompts de texto
* Usar Stable Diffusion (DreamShaper 8)
* Acompanhar tempo de geração
* Interagir via chat estilo “estúdio de imagens”

---

## 🧠 Tecnologias usadas

* 🧪 Python
* ⚡ FastAPI
* 🤖 Diffusers (Stable Diffusion)
* 🧠 PyTorch (CUDA)
* 🎨 DreamShaper-8
* 🌐 HTML + JS (frontend embutido)
* 🚀 Uvicorn

---

## 📦 Instalação (Google Colab / Notebook)

### 1️⃣ Clonar o projeto

```bash
!git clone https://github.com/Hack1981/ia_ima.git
%cd ia_ima
```

---

### 2️⃣ Instalar dependências

```bash
!bash instalador.sh
```

---

### 3️⃣ Iniciar o servidor

```bash
!bash start.sh
```

---

## 🌐 Como funciona

Após iniciar o servidor:

* Acesse:

```
http://localhost:8888
```

ou no Colab via túnel (se configurado)

---

## 🧪 Endpoint da API

### 🎨 Gerar imagem

```
GET /ia_img?prompt=seu_texto_aqui
```

### Exemplo:

```
/ia_img?prompt=um dragão cyberpunk voando na cidade futurista
```

### Resposta:

* Imagem PNG gerada pela IA
* Header com tempo de geração:

```
X-Generation-Time: 3.42
```

---

## 🖥️ Interface Web

A interface inclui:

* 💬 Chat estilo IA
* ⏳ Status de geração em tempo real
* 🖼️ Renderização automática da imagem
* 🧹 Botão para limpar conversa
* 🎨 Tema escuro moderno

---

## ⚙️ Código principal

O servidor usa:

* Modelo: `Lykon/dreamshaper-8`
* Scheduler: `EulerAncestralDiscreteScheduler`
* Otimizações:

  * `enable_attention_slicing()`
  * `enable_vae_slicing()`
  * `torch.float16 (CUDA)`

---

## 📡 FastAPI Server

O servidor roda em:

```python
uvicorn.run(app, host="0.0.0.0", port=8888)
```

---

## 🧩 Estrutura do projeto

```
ia_ima/
│
├── instalador.sh
├── start.sh
├── main.py (FastAPI + IA)
└── README.md
```

---

## ⚡ Exemplo de uso

Prompt:

```
um castelo flutuando no céu com luzes neon e nuvens douradas
```

Resultado:

🖼️ Imagem gerada em poucos segundos com IA

---

## 📌 Observações

* Requer GPU (CUDA recomendado)
* Ideal para Colab ou servidores com GPU
* Modelos podem demorar na primeira execução

---

## 🧠 Autor

Projeto experimental de geração de imagens com IA.
