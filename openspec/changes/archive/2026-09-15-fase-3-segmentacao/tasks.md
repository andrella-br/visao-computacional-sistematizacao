## 1. Conversão COCO → YOLO-seg

- [x] 1.1 Criar `src/step07_segmentation_prepare_yolo_config.py` que converte os polígonos COCO em labels YOLO-seg e gera `data.yaml`/`train.txt`/`val.txt`/`test.txt`, e verificar que todas as 300 imagens com anotação de `person` geram um label correspondente
- [x] 1.2 Rodar smoke test de 1 época para validar o pipeline (sem erros de path/label) e medir o tempo por época

## 2. Treino do segmentador

- [x] 2.1 Criar `src/step08_segmentation_train_yolo.py` com os hiperparâmetros documentados no `design.md` (YOLOv8n-seg, 30 épocas, imgsz=640, batch=16, seed=42, `project=` absoluto)
- [x] 2.2 Rodar o treino completo (30 épocas) em background e aguardar a conclusão, verificando que os pesos e as curvas de treino são salvos em `models/segmentation/<run>/`

## 3. Comparação visual caixas × máscaras

- [x] 3.1 Criar `src/step09_segmentation_compare_boxes_vs_masks.py` que roda o detector da Fase 2 e o segmentador desta fase sobre as mesmas imagens do dataset de canteiro de obra (que contêm pessoas), salvando as visualizações lado a lado em `reports/figures/` — usando recortes de quadrante para contornar o achado de imagens-mosaico no dataset de origem
- [x] 3.2 Escrever um comentário explicando o que a máscara revela que a caixa não mostra (silhueta, contorno, oclusão parcial), com base nos exemplos gerados

## 4. Documentação de métricas e hiperparâmetros

- [x] 4.1 Extrair as métricas finais de validação (mask mAP@0.5, mAP@0.5:0.95, precisão, recall) dos resultados do treino
- [x] 4.2 Escrever `reports/segmentacao-fase3.md` documentando hiperparâmetros, métricas de validação e a comparação visual caixas×máscaras (task 3)
- [x] 4.3 Atualizar `docs/roadmap.md` (Fase 3) marcando como concluída, com um resumo do resultado

## 5. Validação final

- [x] 5.1 Rodar `openspec validate fase-3-segmentacao --strict` e confirmar que a mudança passa sem erros
- [x] 5.2 Revisar manualmente que nenhuma decisão de avaliação de teste/matriz de confusão (Fase 4) foi tomada nesta mudança
