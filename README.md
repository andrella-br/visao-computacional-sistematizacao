# Sistema de Visão Computacional para Detecção e Segmentação

Projeto da disciplina de pós-graduação **Visão Computacional e Reconhecimento
de Padrões** (Prof. Romes Heriberto). O grupo assume o papel de um time de
engenharia de IA e constrói, de ponta a ponta, um sistema que detecta e
segmenta objetos em imagens de um cenário real, demonstrando o funcionamento
em vídeo.

## Cenário

**Segurança do Trabalho** — detecção de EPIs (capacete, colete) e
segmentação de pessoas em canteiros de obra.

- **Detecção (10 classes):** `Hardhat`, `NO-Hardhat`, `Safety Vest`,
  `NO-Safety Vest`, `Mask`, `NO-Mask`, `Person`, `Safety Cone`, `machinery`,
  `vehicle`. Fonte: *Construction Site Safety* (Roboflow Universe / Kaggle,
  CC BY 4.0), subconjunto de 350 imagens.
- **Segmentação (1 classe):** `person`. Fonte: subconjunto do COCO 2017
  (val2017, categoria `person`), 300 imagens com máscaras prontas.

📄 **[Relatório técnico completo](docs/relatorio-tecnico.md)** — problema,
dataset/EDA, metodologia, resultados (validação e teste), análise de erros,
aplicação prática e limitações.

Ver também [`docs/proposta-fase1.md`](docs/proposta-fase1.md) e
[`reports/eda-fase1.md`](reports/eda-fase1.md) para a proposta original e a
análise exploratória dos dados.

## Estrutura do repositório

```
data/
  raw/            # imagens originais anotadas (não versionado)
  processed/      # imagens/anotações após pré-processamento (não versionado)
  splits/         # listas de arquivos train/val/test por fonte (versionado)
notebooks/        # notebooks Colab/Jupyter (EDA, treino, avaliação, inferência)
src/
  step01_data_*.py, step02_data_*.py, ...      # Fase 1 (dados)
  step0N_detection_*.py                        # Fase 2 (detecção)
  step0N_segmentation_*.py                     # Fase 3 (segmentação)
  step0N_evaluation_*.py                       # Fase 4 (avaliação)
  step0N_inference_*.py                        # Fase 4 (inferência/vídeo)
  # nomeados `stepNN_<fase>_<descrição>.py` — NN é a ordem global de
  # execução no pipeline; <fase> é data/detection/segmentation/evaluation/
  # inference, indicando a que etapa do roadmap o script pertence
  # (substitui as antigas subpastas src/detection/, src/segmentation/ etc.)
models/
  detection/      # checkpoints do detector (não versionado)
  segmentation/   # checkpoints da segmentação (não versionado)
reports/
  figures/        # gráficos e imagens usadas no relatório técnico
video/
  input/          # vídeo(s) de entrada do cenário (não versionado)
  output/         # vídeo(s) com inferência sobreposta (não versionado)
docs/
  roadmap.md      # as 5 fases do projeto, entregáveis e critérios do barema
openspec/         # propostas de mudança e specs do projeto (padrão OpenSpec)
image/            # material de apoio do enunciado
```

Pastas de dados, modelos e vídeo são versionadas vazias (via `.gitkeep`); seu
conteúdo é ignorado pelo `.gitignore` por serem arquivos grandes. Os scripts
em `src/` não ficam em subpastas por tarefa: o nome `stepNN_<fase>_<descrição>.py`
já indica a ordem de execução (`NN`) e a fase do roadmap a que pertencem
(`data`, `detection`, `segmentation`, `evaluation`, `inference`).

## Como reproduzir

1. Criar e ativar um ambiente virtual **dedicado a este projeto** (`.venv/`,
   não versionado) e instalar as dependências dentro dele:
   ```bash
   python -m venv .venv
   # Windows (Git Bash):
   source .venv/Scripts/activate
   # Linux/Mac:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```
2. Rodar os scripts de `src/` na ordem numérica — cada um documenta seu
   propósito e uso no topo do arquivo:
   ```bash
   # Fase 1 — dados
   python src/step01_data_prepare_construction_site_safety.py
   python src/step02_data_prepare_coco_person_subset.py
   python src/step03_data_make_splits.py
   python src/step04_data_eda_construction_site_safety.py

   # Fase 2 — detecção
   python src/step05_detection_prepare_yolo_config.py
   python src/step06_detection_train_yolo.py

   # Fase 3 — segmentação
   python src/step07_segmentation_prepare_yolo_config.py
   python src/step08_segmentation_train_yolo.py
   python src/step09_segmentation_compare_boxes_vs_masks.py

   # Fase 4 — avaliação e vídeo
   python src/step10_inference_concat_videos.py
   python src/step11_evaluation_test_set.py
   python src/step12_evaluation_error_analysis.py
   python src/step13_inference_run_on_video.py
   python src/step14_inference_compliance_report.py
   ```
   `step01` espera um token do Kaggle configurado (`~/.kaggle/access_token`,
   gerado em kaggle.com/settings/api) para baixar o dataset de EPIs.

Todas as fases (1 a 4) estão concluídas — ver
[`docs/relatorio-tecnico.md`](docs/relatorio-tecnico.md) para os resultados
completos e [`docs/roadmap.md`](docs/roadmap.md) para o status por fase.

## Planejamento do projeto

O planejamento segue o padrão [OpenSpec](https://github.com/Fission-AI/OpenSpec):
cada fase do roadmap vira uma mudança em `openspec/changes/`, com proposta,
specs e tarefas rastreáveis antes da implementação. Veja `docs/roadmap.md`
para o plano de fases e `Sistematizacao_Instruções.md` para o enunciado
completo da disciplina.

## Integrantes

_A preencher pelo grupo._
