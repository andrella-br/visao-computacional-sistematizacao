## 1. Configuração do dataset YOLO

- [x] 1.1 Criar `src/step05_detection_prepare_yolo_config.py` que gera `data.yaml`, `train.txt`, `val.txt`, `test.txt` a partir dos splits da Fase 1, e verificar que os arquivos gerados referenciam exatamente as imagens dos manifests
- [x] 1.2 Rodar um smoke test de 1 época para validar que o pipeline de treino lê a configuração corretamente (labels encontrados, sem erros de path), e medir o tempo por época

## 2. Treino do detector

- [x] 2.1 Criar `src/step06_detection_train_yolo.py` com os hiperparâmetros documentados no `design.md` (YOLOv8n, 30 épocas, imgsz=640, batch=16, seed=42, `project=` absoluto)
- [x] 2.2 Rodar o treino completo (30 épocas) em background e aguardar a conclusão, verificando que os pesos (`best.pt`, `last.pt`) e as curvas de treino são salvos em `models/detection/<run>/`

## 3. Documentação de métricas e hiperparâmetros

- [x] 3.1 Extrair as métricas finais de validação (mAP@0.5, mAP@0.5:0.95, precisão, recall — agregado e por classe) dos resultados do treino
- [x] 3.2 Escrever `reports/deteccao-fase2.md` documentando hiperparâmetros (épocas, imgsz, batch, otimizador, augmentation), as métricas de validação e as curvas de treino (referenciando os gráficos gerados pelo Ultralytics)
- [x] 3.3 Atualizar `docs/roadmap.md` (Fase 2) marcando como concluída, com um resumo do resultado

## 4. Validação final

- [x] 4.1 Rodar `openspec validate fase-2-baseline-deteccao --strict` e confirmar que a mudança passa sem erros
- [x] 4.2 Revisar manualmente que nenhuma decisão de segmentação (Fase 3) foi tomada nesta mudança
