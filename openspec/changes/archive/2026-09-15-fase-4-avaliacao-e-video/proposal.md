## Why

Os modelos de detecção (Fase 2) e segmentação (Fase 3) só foram avaliados no conjunto de **validação**, usado durante o treino. A Fase 4 do roadmap exige uma avaliação rigorosa no conjunto de **teste** (nunca visto), com análise crítica dos erros, além da demonstração do sistema funcionando em vídeo real — nenhuma dessas entregas existe ainda.

## What Changes

- Rodar a avaliação completa dos dois modelos (detecção e segmentação) no conjunto de **teste** (36 imagens de EPI / 30 imagens de pessoas, nunca usadas no treino ou validação): mAP@0.5, mAP@0.5:0.95, IoU médio, precisão/recall e matriz de confusão.
- Montar uma análise de erros com exemplos comentados de falsos positivos e falsos negativos do detector no conjunto de teste.
- Rodar a inferência dos dois modelos sobre o vídeo final (`video/input/video_final_canteiro_obra.mp4`, 38.3s) e salvar os vídeos anotados em `video/output/`.
- Documentar tudo em `reports/avaliacao-fase4.md`.

Fora de escopo: qualquer novo treino ou ajuste de hiperparâmetro dos modelos (isso pertenceria a uma iteração de fine-tuning, não à Fase 4); rastreamento de objetos (ByteTrack/DeepSORT) é o item de bônus opcional do enunciado, não obrigatório nesta mudança.

## Capabilities

### New Capabilities
- `test-evaluation`: avaliação dos modelos de detecção e segmentação no conjunto de teste (mAP, IoU, precisão/recall, matriz de confusão) e análise de erros comentada.
- `video-inference`: inferência dos modelos treinados sobre um vídeo real do cenário, com saída anotada salva em `video/output/`.

### Modified Capabilities
(nenhuma)

## Impact

- Novos arquivos: `src/step11_evaluation_test_set.py` (avaliação no teste + IoU), `src/step12_evaluation_error_analysis.py` (análise de erros), `src/step13_inference_run_on_video.py` (inferência em vídeo).
- Resultados em `reports/avaliacao-fase4.md`, `reports/figures/` (exemplos de erro comentados) e `video/output/` (vídeos anotados, gitignorados).
