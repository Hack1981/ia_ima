# ✨ IA Image Studio

Sistema de geração de imagens com IA usando **Stable Diffusion + FastAPI + Interface Web interativa**.

---

## 🚀 Visão geral

Este projeto cria uma API + interface web onde você pode:

* Gerar imagens a partir de prompts de texto
* Usar Stable Diffusion (DreamShaper 8)
* Acompanhar tempo de geração
* Acessar via link público (Cloudflare Tunnel)

---

## 🧠 Tecnologias usadas

* 🧪 Python
* ⚡ FastAPI
* 🤖 Diffusers (Stable Diffusion)
* 🧠 PyTorch (CUDA)
* 🎨 DreamShaper-8
* 🌐 HTML + JS (frontend embutido)
* 🚀 Uvicorn
* ☁️ Cloudflare Tunnel

---

## 📦 Instalação (Google Colab / Linux)

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

### 3️⃣ Iniciar o projeto

```bash
!bash start.sh
```

---

## 🌐 Como funciona

Após rodar o projeto:

* API local: `http://localhost:8888`
* Cloudflare gera automaticamente um link público
* Logs do servidor aparecem em tempo real

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

* 💬 Chat estilo IA
* 🖼️ Geração de imagens em tempo real
* ⏳ Feedback de geração
* 🧹 Botão de limpar chat
* 🎨 Interface moderna em tema escuro

---

## ⚙️ Modelo IA

* Modelo: `Lykon/dreamshaper-8`
* Scheduler: `EulerAncestralDiscreteScheduler`
* Otimizações:

  * attention slicing
  * vae slicing
  * float16 CUDA

---

## 📡 Execução do servidor

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
├── main.py
└── README.md
```

---

## ⚡ Fluxo de uso

1. Clona o repositório
2. Executa `instalador.sh`
3. Executa `start.sh`
4. Acessa o link gerado pelo Cloudflare

---

## 📌 Observações

* Requer GPU (CUDA recomendado)
* Primeira execução pode demorar
* Link do Cloudflare é temporário

---

## 🧠 Autor

Projeto experimental de geração de imagens com IA.
