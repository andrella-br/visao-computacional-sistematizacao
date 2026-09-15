## Why

A Fase 2 entregou o detector baseline (YOLOv8n, EPIs). A Fase 3 do roadmap exige treinar/adaptar um modelo de segmentação no mesmo domínio do projeto (segurança do trabalho) e comparar visualmente caixas × máscaras. A Fase 1 já preparou o subconjunto do COCO (300 imagens, categoria `person`, com máscaras poligonais prontas) — falta convertê-lo para um formato treinável e efetivamente treinar o modelo de segmentação.

## What Changes

- Converter as anotações COCO (polígonos) do subconjunto `person` para o formato YOLO-seg (label `.txt` com classe + polígono normalizado), usando os splits já definidos na Fase 1 (`data/splits/coco-person/{train,val,test}.txt`).
- Fazer o fine-tuning de um **YOLOv8n-seg** (Ultralytics) pré-treinado, adaptado para a classe única `person`, mantendo a mesma ferramenta (Ultralytics) e convenções de hiperparâmetro usadas na Fase 2 para consistência.
- Treinar localmente em CPU (mesma limitação da Fase 2), com orçamento de tempo medido empiricamente antes de fixar o número de épocas.
- Registrar curvas de treino e métricas de validação (mask mAP@0.5, mAP@0.5:0.95, precisão, recall).
- Gerar uma comparação visual caixas × máscaras: rodar o detector da Fase 2 (caixas de `Person`) e o segmentador da Fase 3 (máscaras de `person`) nas **mesmas imagens** do domínio de canteiro de obra, mostrando o que a máscara revela que a caixa não mostra (silhueta, oclusão, contorno irregular).
- Documentar hiperparâmetros e resultado em `reports/`.

Fora de escopo: avaliação completa no conjunto de teste com matriz de confusão (Fase 4), inferência em vídeo (Fase 4).

## Capabilities

### New Capabilities
- `segmentation-baseline`: pipeline de conversão COCO→YOLO-seg, fine-tuning do segmentador, métricas de validação e comparação visual caixas×máscaras, para a Fase 3 do roadmap.

### Modified Capabilities
(nenhuma)

## Impact

- Novos arquivos: `src/step07_segmentation_prepare_yolo_config.py` (conversão COCO→YOLO-seg + data.yaml), `src/step08_segmentation_train_yolo.py` (treino), `src/step09_segmentation_compare_boxes_vs_masks.py` (comparação visual).
- Resultados em `models/segmentation/<run>/` (pesos gitignorados, curvas versionadas) e `reports/segmentacao-fase3.md`.
- `data/raw/coco-person/` ganha `labels/` (formato YOLO-seg) e `data.yaml`.
