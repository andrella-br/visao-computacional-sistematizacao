# detection-baseline Specification

## Purpose

Garante que exista um detector baseline treinado (fine-tuning de YOLOv8n) sobre o dataset de EPIs da Fase 1, com métricas de validação e hiperparâmetros documentados, atendendo ao requisito de "Detecção de objetos" da Fase 2 do roadmap.

## Requirements

### Requirement: Configuração de dataset no formato Ultralytics YOLO
O projeto SHALL gerar um `data.yaml` (formato Ultralytics) e listas de caminho `train.txt`/`val.txt`/`test.txt` a partir dos splits reprodutíveis da Fase 1, sem duplicar ou modificar as imagens originais.

#### Scenario: Configuração é reprodutível a partir dos splits da Fase 1
- **WHEN** o script de preparação de configuração YOLO é executado
- **THEN** `data.yaml`, `train.txt`, `val.txt` e `test.txt` são gerados em `data/raw/construction-site-safety/`, referenciando exatamente as mesmas imagens listadas nos manifests de split da Fase 1

### Requirement: Detector treinado (fine-tuning)
O projeto SHALL treinar (fine-tuning) um detector YOLOv8n pré-treinado, adaptado para as 10 classes do dataset de EPIs, produzindo pesos salvos e curvas de treino (loss e métricas por época).

#### Scenario: Pesos do modelo treinado ficam disponíveis
- **WHEN** o treino é concluído
- **THEN** os pesos finais (`best.pt`) e as curvas de treino ficam salvos em `models/detection/<run>/`, prontos para uso na Fase 4 (avaliação) e na demonstração em vídeo

### Requirement: Métricas de validação registradas
O projeto SHALL registrar, ao final do treino, as métricas no conjunto de validação: mAP@0.5, mAP@0.5:0.95, precisão e recall (agregados e, quando disponível, por classe).

#### Scenario: Métricas ficam documentadas para o relatório
- **WHEN** alguém prepara o relatório técnico ou decide se o baseline está bom o suficiente
- **THEN** encontra as métricas de validação (mAP@0.5, mAP@0.5:0.95, precisão, recall) documentadas em `reports/`, sem precisar re-treinar o modelo

### Requirement: Hiperparâmetros documentados
O projeto SHALL documentar os hiperparâmetros usados no treino: número de épocas, tamanho de imagem (`imgsz`), tamanho de batch, otimizador e configuração de augmentation (mosaic, flips, HSV, etc.), conforme exigido pelo enunciado da Fase 2.

#### Scenario: Hiperparâmetros são auditáveis
- **WHEN** o professor avalia a documentação de hiperparâmetros da Fase 2
- **THEN** encontra épocas, imgsz, batch, otimizador e augmentation listados explicitamente, sem precisar inspecionar o código-fonte do treino
