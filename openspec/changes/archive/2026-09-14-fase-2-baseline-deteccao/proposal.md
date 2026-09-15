## Why

A Fase 1 entregou os dados prontos (subconjunto de 350 imagens do Construction Site Safety, splits reprodutíveis com seed=42). A Fase 2 do roadmap exige treinar um detector baseline (YOLO ou Faster R-CNN), registrar curvas de treino, obter métricas de validação e documentar hiperparâmetros — nenhuma dessas entregas existe ainda.

## What Changes

- Gerar a configuração de dataset no formato Ultralytics YOLO (`data.yaml` + listas `train.txt`/`val.txt`/`test.txt`) a partir dos splits já existentes da Fase 1.
- Fazer o fine-tuning de um **YOLOv8n** (Ultralytics) pré-treinado no COCO, adaptando para as 10 classes de EPI do subconjunto Construction Site Safety.
- Treinar localmente nesta sessão, em **CPU** (não há GPU disponível no ambiente), com hiperparâmetros escolhidos para caber num tempo viável (medido empiricamente: ~173s/época com batch=16, imgsz=640, 244 imagens de treino).
- Registrar curvas de treino (loss, mAP por época) e métricas de validação (mAP@0.5, mAP@0.5:0.95, precisão, recall).
- Documentar todos os hiperparâmetros usados (épocas, tamanho de imagem, batch, otimizador, augmentation) em `docs/` ou `reports/`.

Fora de escopo desta mudança: avaliação completa no conjunto de teste com matriz de confusão e análise de erros (isso é Fase 4), e segmentação (Fase 3).

## Capabilities

### New Capabilities
- `detection-baseline`: pipeline de fine-tuning do detector (dataset YOLO, treino, métricas de validação, hiperparâmetros documentados) para a Fase 2 do roadmap.

### Modified Capabilities
(nenhuma)

## Impact

- Novos arquivos: `src/step05_detection_prepare_yolo_config.py` (gera `data.yaml`), `src/step06_detection_train_yolo.py` (treino), resultados em `models/detection/<run>/` (pesos, curvas, métricas — gitignorado por serem checkpoints/artefatos grandes) e um resumo documentado em `reports/`.
- `data/raw/construction-site-safety/` ganha `data.yaml`, `train.txt`, `val.txt`, `test.txt` (listas de caminho no formato Ultralytics).
