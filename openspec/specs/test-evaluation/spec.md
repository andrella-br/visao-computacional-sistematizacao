# test-evaluation Specification

## Purpose

Garante que os modelos de detecção e segmentação sejam avaliados rigorosamente no conjunto de teste (nunca visto no treino), com métricas completas e análise crítica dos erros, atendendo ao requisito de "Avaliação e análise crítica" da Fase 4 do roadmap.

## Requirements

### Requirement: Avaliação no conjunto de teste
O projeto SHALL avaliar o detector (Fase 2) e o segmentador (Fase 3) no respectivo conjunto de teste (nunca usado em treino ou validação), registrando mAP@0.5, mAP@0.5:0.95, IoU médio, precisão e recall.

#### Scenario: Métricas de teste ficam documentadas
- **WHEN** alguém consulta o desempenho real dos modelos, fora do conjunto usado durante o desenvolvimento
- **THEN** encontra mAP@0.5, mAP@0.5:0.95, IoU médio, precisão e recall calculados sobre o conjunto de teste de cada modelo, documentados em `reports/`

### Requirement: Matriz de confusão do conjunto de teste
O projeto SHALL gerar a matriz de confusão do detector sobre o conjunto de teste, mostrando os acertos e confusões entre as 10 classes de EPI.

#### Scenario: Confusões entre classes ficam visíveis
- **WHEN** alguém analisa a matriz de confusão do teste
- **THEN** consegue identificar quais classes são mais confundidas entre si (ex. `Hardhat` vs `NO-Hardhat`)

### Requirement: Análise de erros comentada
O projeto SHALL apresentar pelo menos 2 exemplos comentados de falso positivo e 2 de falso negativo do detector no conjunto de teste, com uma explicação da causa provável de cada erro.

#### Scenario: Erro é comentado com causa provável
- **WHEN** alguém revisa um exemplo de falso negativo na análise de erros
- **THEN** encontra a imagem, a anotação esperada, a predição do modelo, e um comentário explicando uma causa plausível (ex. objeto pequeno, oclusão, classe rara, imagem-mosaico)
