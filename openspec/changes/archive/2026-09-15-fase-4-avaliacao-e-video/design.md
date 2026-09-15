## Context

Os modelos já estão treinados (Fase 2: detecção, Fase 3: segmentação) e os splits de teste já existem (`data/splits/.../test.txt`, nunca usados em treino/validação). O `model.val()` do Ultralytics já calcula mAP@0.5, mAP@0.5:0.95, precisão, recall e a matriz de confusão automaticamente quando apontado para o split de teste — falta decidir como obter o **IoU médio** (que o Ultralytics não expõe como número único direto) e como estruturar a análise de erros.

## Goals / Non-Goals

**Goals:**
- Reutilizar `model.val(split="test")` do Ultralytics para mAP/precisão/recall/matriz de confusão, em vez de reimplementar métricas já corretas na biblioteca.
- Calcular IoU médio das predições corretamente casadas (TP) com um script simples usando as funções de IoU do próprio Ultralytics (`ultralytics.utils.metrics.box_iou`), sem inventar uma métrica nova.
- Escolher exemplos de erro (FP/FN) de forma objetiva (não visualmente arbitrária): comparar predições do modelo com o ground-truth do conjunto de teste, classificando por classe faltante/sobrando.

**Non-Goals:**
- Não é objetivo re-treinar ou ajustar hiperparâmetros para melhorar as métricas de teste — a Fase 4 avalia o que já foi treinado.
- Não é objetivo implementar rastreamento de objetos (ByteTrack/DeepSORT) — é bônus opcional do enunciado, fora desta mudança.

## Decisions

**Decisão 1 — IoU médio calculado via matching de caixas TP.**
Rodar `model.predict()` no conjunto de teste, casar cada predição com a caixa de ground-truth de maior IoU da mesma classe (usando `box_iou` do Ultralytics), e reportar a média do IoU dos pares casados com confiança acima do threshold padrão (0.25) — essa é a definição usual de "IoU médio" em avaliação de detecção, mesmo não sendo alan Ultralytics-native.

**Decisão 2 — Seleção de exemplos de erro por contagem de discrepância.**
Para cada imagem de teste, comparar contagem de instâncias por classe entre ground-truth e predição. Imagens com mais falsos negativos (classe no GT ausente na predição) entram no pool de exemplos de FN; imagens com mais falsos positivos (classe predita ausente no GT) entram no pool de FP. Os 2 exemplos de cada categoria com maior discrepância são escolhidos, garantindo que a análise não seja arbitrária.

**Decisão 3 — Inferência em vídeo com os dois modelos, gerando duas saídas separadas.**
Em vez de tentar combinar detecção+segmentação num único vídeo (complexidade extra de composição visual), o script gera `video/output/deteccao_epi.mp4` (caixas de EPI) e `video/output/segmentacao_pessoas.mp4` (máscaras de pessoa) separadamente, cada um demonstrando um dos dois modelos com clareza.

**Decisão 4 — Orçamento de tempo para inferência em vídeo.**
957 frames, 1280×720, CPU. Com base na velocidade medida na Fase 2 (~80ms de inferência/imagem + overhead), o tempo estimado é de alguns minutos por modelo — cada execução roda em foreground/background conforme necessário, sem exigir um orçamento de épocas como no treino.

## Risks / Trade-offs

- [Risco] IoU médio calculado manualmente pode divergir ligeiramente de alguma definição acadêmica específica → Mitigação: documentar exatamente o método usado (matching por classe + maior IoU + threshold de confiança) no relatório, para ser auditável.
- [Risco] Vídeo de teste é diferente do domínio de treino da Fase 3 (COCO) → Mitigação: já documentado na Fase 3 como limitação esperada de generalização entre domínios.
