## 1. Avaliação no conjunto de teste

- [x] 1.1 Criar `src/step11_evaluation_test_set.py` que roda `model.val(split="test")` para o detector e o segmentador, salvando mAP@0.5, mAP@0.5:0.95, precisão, recall e matriz de confusão de cada um
- [x] 1.2 Calcular o IoU médio das predições casadas (TP) do detector no conjunto de teste, conforme método documentado no `design.md`
- [x] 1.3 Verificar que as métricas foram calculadas sobre o split de teste (nunca visto em treino/validação), não sobre validação

## 2. Análise de erros

- [x] 2.1 Identificar 2 exemplos de falso positivo e 2 de falso negativo do detector no teste, usando o critério de discrepância do `design.md`
- [x] 2.2 Gerar visualizações comentadas (imagem + predição + ground-truth) desses 4 exemplos e salvar em `reports/figures/`

## 3. Inferência em vídeo

- [x] 3.1 Criar `src/step13_inference_run_on_video.py` que roda o detector sobre `video/input/video_final_canteiro_obra.mp4` e salva `video/output/deteccao_epi/`
- [x] 3.2 Rodar o segmentador sobre o mesmo vídeo e salvar `video/output/segmentacao_pessoas/`
- [x] 3.3 Verificar que os dois vídeos de saída existem, têm duração compatível com o vídeo de entrada (38.3s) e mostram anotações visíveis

## 4. Documentação

- [x] 4.1 Escrever `reports/avaliacao-fase4.md` com as métricas de teste (detecção e segmentação), a matriz de confusão, o IoU médio, a análise de erros comentada e um resumo da inferência em vídeo
- [x] 4.2 Atualizar `docs/roadmap.md` (Fase 4) marcando como concluída, com um resumo do resultado

## 5. Validação final

- [x] 5.1 Rodar `openspec validate fase-4-avaliacao-e-video --strict` e confirmar que a mudança passa sem erros
- [x] 5.2 Revisar manualmente que nenhum re-treino ou ajuste de hiperparâmetro foi feito nesta mudança (só avaliação e inferência)
