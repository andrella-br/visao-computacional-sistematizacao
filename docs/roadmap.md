# Roadmap do projeto

Este documento traduz as 5 fases descritas em `Sistematizacao_Instruções.md`
em um plano rastreável. Cada fase (2 a 5) deve ser proposta como uma mudança
OpenSpec separada (`openspec new change "<nome-da-fase>"`) **somente depois**
que a Fase 1 estiver concluída e o cenário/dataset estiverem definidos. Não
crie especificações de treino, dataset ou modelo antes disso.

## Fase 1 — Definição e dados ✅ Concluída

**Status:** cenário e dataset definidos — ver
[`docs/proposta-fase1.md`](proposta-fase1.md) e
[`../reports/eda-fase1.md`](../reports/eda-fase1.md).

- **Cenário:** Segurança do Trabalho (EPIs + segmentação de pessoas).
- **Dataset de detecção:** Construction Site Safety (Roboflow/Kaggle, CC BY
  4.0), subconjunto de 350 imagens, 10 classes.
- **Dataset de segmentação:** subconjunto do COCO 2017 (`person`), 300
  imagens com máscaras.
- **Splits:** 70/20/10, seed=42, reprodutíveis via `src/data/make_splits.py`.

**Objetivo original:** formar o grupo, escolher o cenário e o dataset, e entender os
dados antes de treinar qualquer modelo.

**Atividades:**
- Formar o grupo (1 a 5 integrantes) e definir responsabilidades.
- Escolher o cenário (Segurança do Trabalho, Agronegócio, Cidades
  Inteligentes, Varejo, ou cenário livre aprovado pelo professor).
- Definir a fonte do dataset (≥300 imagens anotadas): público (Roboflow
  Universe, Kaggle, subconjunto do COCO, com fonte citada) ou anotado pelo
  grupo (CVAT, Label Studio ou Roboflow).
- Fazer a análise exploratória (EDA): quantidade de imagens por classe,
  resolução, condições de luz, desbalanceamento.

**Entregáveis:** proposta de 1 página (problema, classes-alvo, fonte dos
dados, ferramenta de anotação).

**Critério do barema:** "1. Problema e dataset" — 10% (clareza do cenário,
qualidade e origem dos dados, EDA e splits corretos).

## Fase 2 — Baseline de detecção ✅ Concluída

**Status:** YOLOv8n treinado (fine-tuning), 30 épocas, CPU — ver
[`../reports/deteccao-fase2.md`](../reports/deteccao-fase2.md).

- **Resultado:** mAP@0.5 = 0.490, mAP@0.5:0.95 = 0.278, precisão = 0.608,
  recall = 0.464 (conjunto de validação).
- **Melhor classe:** `machinery` (mAP@0.5=0.714); **pior classe:**
  `NO-Mask` (mAP@0.5=0.195), refletindo o desbalanceamento identificado na EDA.
- **Pesos e curvas:** `models/detection/css_yolov8n_baseline/`.

**Objetivo original:** treinar um primeiro detector funcional no domínio escolhido.

**Atividades:**
- Preparar os dados no formato YOLO ou COCO, com splits fixos e seed
  definida.
- Fazer o fine-tuning de um detector (YOLO/Ultralytics ou Faster R-CNN/
  torchvision) no Colab (GPU).
- Registrar curvas de treino e obter as primeiras métricas de validação.
- Documentar hiperparâmetros (épocas, tamanho de imagem, batch,
  augmentation).

**Entregáveis:** notebook de treino com saídas visíveis, métricas de
validação, hiperparâmetros documentados.

**Critério do barema:** "2. Detecção de objetos" — 25% (pipeline funcional,
fine-tuning correto, desempenho e documentação dos hiperparâmetros).

## Fase 3 — Segmentação ✅ Concluída

**Status:** YOLOv8n-seg treinado (fine-tuning), 30 épocas, CPU — ver
[`../reports/segmentacao-fase3.md`](../reports/segmentacao-fase3.md).

- **Resultado:** mask mAP@0.5 = 0.559, mask mAP@0.5:0.95 = 0.288, precisão =
  0.697, recall = 0.507 (conjunto de validação, classe `person`).
- **Comparação caixas×máscaras:** feita sobre as mesmas imagens do domínio
  de canteiro de obra — máscara revela contorno/oclusão que a caixa não
  mostra; detector revela informação de EPI que a máscara não tem.
- **Achado adicional:** parte do dataset de detecção (Fase 2) é composta por
  imagens-mosaico 2×2, documentado em `reports/deteccao-fase2.md`.
- **Pesos e curvas:** `models/segmentation/coco_person_yolov8n_seg_baseline/`.

**Objetivo original:** treinar ou adaptar um modelo de segmentação no mesmo domínio e
comparar com a detecção.

**Atividades:**
- Treinar/adaptar segmentação de instâncias (YOLO-seg ou Mask R-CNN) ou
  semântica (DeepLab / U-Net).
- Comparar visualmente caixas × máscaras: o que a segmentação revela que a
  detecção não mostra?
- Ajustar dataset/anotações se necessário.

**Entregáveis:** notebook de treino/segmentação, comparação visual
documentada.

**Critério do barema:** "3. Segmentação" — 20% (implementação correta,
qualidade das máscaras e comparação com a detecção).

## Fase 4 — Avaliação e vídeo ✅ Concluída

**Status:** avaliação no teste e inferência em vídeo concluídas — ver
[`../reports/avaliacao-fase4.md`](../reports/avaliacao-fase4.md).

- **Detector (teste):** mAP@0.5 = 0.547, mAP@0.5:0.95 = 0.324, IoU médio
  (TP) = 0.793, precisão = 0.710, recall = 0.481.
- **Segmentador (teste):** mask mAP@0.5 = 0.393, mask mAP@0.5:0.95 = 0.177,
  precisão = 0.635, recall = 0.376.
- **Análise de erros:** 4 exemplos comentados (2 FN, 2 FP) — padrão comum:
  cenas de alta densidade (multidões, grupos sobrepostos) e objetos
  pequenos.
- **Vídeo:** `video/output/deteccao_epi/` e `video/output/segmentacao_pessoas/`
  (38.3s, mesmo vídeo de entrada).

**Objetivo original:** avaliar rigorosamente no conjunto de teste e demonstrar o
sistema em vídeo.

**Atividades:**
- Rodar avaliação completa no conjunto de teste (nunca visto no treino):
  mAP@0.5, mAP@0.5:0.95, IoU, precisão/recall, matriz de confusão.
- Montar análise de erros com exemplos comentados de falsos positivos e
  falsos negativos.
- Executar inferência em um vídeo real do cenário (≥30 segundos) e gravar o
  resultado.
- (Bônus, opcional, até +0,5 ponto) rastreamento de objetos (ByteTrack ou
  DeepSORT) ou demo interativa (Gradio / Hugging Face Spaces).

**Entregáveis:** relatório de métricas, análise de erros, vídeo com
inferência em `video/output/`.

**Critério do barema:** "4. Avaliação e análise crítica" — 20% e
"5. Aplicação em vídeo" — 10%.

## Fase 5 — Entrega e apresentação 🟡 Em andamento

**Status:**
- ✅ Relatório técnico consolidado: [`../docs/relatorio-tecnico.md`](relatorio-tecnico.md).
- ✅ Repositório Git local inicializado (`git init` + primeiro commit) — push
  para o GitHub pendente de decisão do integrante (conta/nome do repo).
- ✅ Notebook Colab executável: `notebooks/pipeline_completo.ipynb`
  (35 células, cobrindo `step01` a `step14`).
- ⬜ Vídeo-pitch (5-8 min) — pendente, exige gravação do integrante.

**Objetivo original:** consolidar e entregar todos os artefatos do projeto.

**Atividades:**
- Finalizar o relatório técnico (README, 6–10 páginas): problema e cenário,
  dataset e EDA, metodologia, resultados, análise de erros, limitações e
  próximos passos.
- Organizar o repositório GitHub com instruções de reprodução e link do
  dataset.
- Gravar o vídeo-pitch (5–8 min, com todos os integrantes participando).
- Submeter tudo no Moodle/AVA dentro do prazo do cronograma.

**Entregáveis:** relatório técnico, repositório organizado, notebook Colab
executável, vídeo-pitch.

**Critério do barema:** "6. Relatório e repositório" — 10% e
"7. Vídeo-pitch" — 5%.

## Como abrir cada fase como mudança OpenSpec

```bash
openspec new change "fase-2-baseline-deteccao"
```

Siga o fluxo padrão (`proposal.md` → `specs/` → `design.md` quando fizer
sentido → `tasks.md`) antes de implementar, e arquive a mudança
(`openspec archive`) ao concluir a fase.
