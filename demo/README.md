---
title: Visão Computacional Segurança do Trabalho
emoji: 🦺
colorFrom: yellow
colorTo: orange
sdk: gradio
sdk_version: 6.27.0
app_file: app.py
pinned: false
---

# Detecção de EPIs + Segmentação de Pessoas

Demo interativa do sistema de visão computacional para segurança do
trabalho (detecção de EPIs em canteiro de obra + segmentação de pessoas).

Projeto da disciplina de pós-graduação Visão Computacional e Reconhecimento
de Padrões. Código completo, relatório técnico, notebooks e dataset:
ver repositório do projeto.

**Modelos:**
- Detector: YOLOv8n, fine-tuning para 10 classes de EPI (capacete, colete,
  máscara — presente/ausente — pessoa, cone, máquina, veículo).
- Segmentador: YOLOv8n-seg, fine-tuning para a classe `person` (silhueta
  completa).

Duas abas:
- **Imagem** — envie uma foto, resultado instantâneo com os dois modelos
  lado a lado.
- **Vídeo** — envie um vídeo, escolha detector ou segmentador, e receba o
  vídeo anotado quadro a quadro (leva alguns minutos, dependendo da
  duração e se há GPU disponível na sessão).

## Como rodar

Esta pasta contém o app pronto (`app.py`), mas os pesos (`detection_best.pt`,
`segmentation_best.pt`) não são versionados no repositório — copie-os de
`models/detection/.../weights/best.pt` e `models/segmentation/.../weights/best.pt`
para dentro desta pasta antes de rodar.

```bash
pip install -r requirements.txt
python app.py
```

**Publicação:** originalmente planejado como Hugging Face Space, mas a
hospedagem de Spaces com Gradio/Docker passou a exigir assinatura **PRO**
mesmo no tier gratuito de CPU (mudança de política identificada em
setembro/2026). Alternativa gratuita: rodar este mesmo código no Google
Colab com `demo.launch(share=True)`, que gera um link público temporário
(~72h) sem custo.
