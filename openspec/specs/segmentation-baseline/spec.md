# segmentation-baseline Specification

## Purpose

Garante que exista um modelo de segmentação baseline (fine-tuning de YOLOv8n-seg) treinado sobre o subconjunto de pessoas do COCO, com métricas de validação, hiperparâmetros documentados e uma comparação visual caixas×máscaras, atendendo ao requisito de "Segmentação" da Fase 3 do roadmap.

## Requirements

### Requirement: Conversão COCO para formato YOLO-seg
O projeto SHALL converter as anotações de segmentação (polígonos) do subconjunto COCO `person` da Fase 1 para o formato YOLO-seg (label `.txt` por imagem, classe + polígono normalizado), preservando a correspondência com os splits de treino/validação/teste já definidos.

#### Scenario: Labels YOLO-seg são gerados a partir do JSON do COCO
- **WHEN** o script de conversão é executado sobre `data/raw/coco-person/instances_person_subset.json`
- **THEN** cada imagem do subconjunto ganha um arquivo de label `.txt` correspondente em formato YOLO-seg, com os polígonos de todas as instâncias de `person` daquela imagem

### Requirement: Segmentador treinado (fine-tuning)
O projeto SHALL treinar (fine-tuning) um YOLOv8n-seg pré-treinado, adaptado para a classe única `person`, produzindo pesos salvos e curvas de treino.

#### Scenario: Pesos do segmentador ficam disponíveis
- **WHEN** o treino é concluído
- **THEN** os pesos finais (`best.pt`) e as curvas de treino ficam salvos em `models/segmentation/<run>/`, prontos para uso na Fase 4 e na demonstração em vídeo

### Requirement: Métricas de validação registradas
O projeto SHALL registrar, ao final do treino, as métricas de segmentação no conjunto de validação: mask mAP@0.5, mask mAP@0.5:0.95, precisão e recall.

#### Scenario: Métricas ficam documentadas para o relatório
- **WHEN** alguém prepara o relatório técnico
- **THEN** encontra as métricas de segmentação de validação documentadas em `reports/`, sem precisar re-treinar o modelo

### Requirement: Comparação visual caixas × máscaras
O projeto SHALL gerar uma comparação visual entre as caixas do detector da Fase 2 e as máscaras do segmentador da Fase 3 sobre as mesmas imagens, com uma nota explícita do que a segmentação revela que a detecção não mostra.

#### Scenario: Exemplo comentado de caixa vs máscara
- **WHEN** alguém consulta a comparação visual no relatório
- **THEN** encontra pelo menos 2 imagens lado a lado (caixa do detector vs máscara do segmentador) com um comentário explicando a diferença observada (ex. contorno/silhueta, oclusão parcial)

### Requirement: Hiperparâmetros documentados
O projeto SHALL documentar os hiperparâmetros usados no treino do segmentador: número de épocas, tamanho de imagem, batch, otimizador e augmentation.

#### Scenario: Hiperparâmetros são auditáveis
- **WHEN** o professor avalia a documentação de hiperparâmetros da Fase 3
- **THEN** encontra épocas, imgsz, batch, otimizador e augmentation listados explicitamente
