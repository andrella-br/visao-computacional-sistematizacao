# Detecção — Baseline (Fase 2)

## Modelo e hiperparâmetros

- **Modelo:** YOLOv8n (Ultralytics), pré-treinado no COCO, fine-tuning para as 10 classes do Construction Site Safety.
- **Dataset:** subconjunto de 350 imagens da Fase 1 (244 treino / 70 validação / 36 teste), formato Ultralytics YOLO.
- **Ambiente de treino:** CPU local (sem GPU disponível nesta sessão), ~59 minutos para 30 épocas.

| Hiperparâmetro | Valor |
|---|---|
| Épocas | 30 |
| Tamanho de imagem (imgsz) | 640 |
| Batch | 16 |
| Otimizador | `auto` → AdamW (lr0=0.000714, momentum=0.9, escolhido automaticamente pelo Ultralytics) |
| Seed | 42 |
| Patience (early stopping) | 100 (não acionado — treino completou as 30 épocas) |

**Augmentation (padrão Ultralytics, não customizado):**

| Parâmetro | Valor | Parâmetro | Valor |
|---|---|---|---|
| `hsv_h` | 0.015 | `flipud` | 0.0 |
| `hsv_s` | 0.7 | `fliplr` | 0.5 |
| `hsv_v` | 0.4 | `mosaic` | 1.0 |
| `degrees` | 0.0 | `mixup` | 0.0 |
| `translate` | 0.1 | `copy_paste` | 0.0 |
| `scale` | 0.5 | `auto_augment` | randaugment |
| `shear` | 0.0 | `erasing` | 0.4 |
| `perspective` | 0.0 | | |

## Métricas de validação (época 30, `best.pt`)

| Métrica | Valor |
|---|---:|
| Precisão | 0.608 |
| Recall | 0.464 |
| mAP@0.5 | 0.490 |
| mAP@0.5:0.95 | 0.278 |

### Por classe

| Classe | Imagens | Instâncias | Precisão | Recall | mAP@0.5 | mAP@0.5:0.95 |
|---|---:|---:|---:|---:|---:|---:|
| Hardhat | 33 | 74 | 0.565 | 0.568 | 0.576 | 0.305 |
| Mask | 29 | 46 | 0.803 | 0.533 | 0.635 | 0.371 |
| NO-Hardhat | 35 | 66 | 0.644 | 0.455 | 0.443 | 0.180 |
| NO-Mask | 39 | 83 | 0.416 | 0.223 | 0.195 | 0.060 |
| NO-Safety Vest | 49 | 93 | 0.602 | 0.387 | 0.483 | 0.255 |
| Person | 67 | 222 | 0.716 | 0.626 | 0.665 | 0.428 |
| Safety Cone | 17 | 133 | 0.449 | 0.301 | 0.274 | 0.084 |
| Safety Vest | 33 | 73 | 0.604 | 0.411 | 0.476 | 0.254 |
| machinery | 53 | 129 | 0.665 | 0.667 | 0.714 | 0.519 |
| vehicle | 15 | 30 | 0.615 | 0.467 | 0.439 | 0.328 |

## Nota adicional (descoberta na Fase 3)

Ao preparar a comparação visual caixas×máscaras da Fase 3, identificamos que boa parte das imagens do Construction Site Safety (versão exportada usada aqui) são, na verdade, **mosaicos 2×2** (4 fotos distintas combinadas em uma única imagem), provavelmente herdados de uma etapa "Mosaic" do pipeline de augmentation do Roboflow que ficou embutida na exportação. Isso não invalida as métricas acima — cada quadrante do mosaico ainda contém objetos e caixas válidas, e o treino trata a imagem combinada normalmente — mas é uma característica do dataset a se ter em mente: o modelo aprendeu, em parte, sobre imagens artificialmente compostas, não só fotos naturais. Ver `reports/segmentacao-fase3.md` para mais detalhes.

## Observações

- **Melhor desempenho:** `machinery` (mAP@0.5=0.714) e `Person` (0.665) — classes mais frequentes no subconjunto (ver EDA da Fase 1).
- **Pior desempenho:** `NO-Mask` (mAP@0.5=0.195) — também uma das classes menos frequentes (214 instâncias no subconjunto todo), confirmando o desbalanceamento identificado na EDA da Fase 1.
- **Coerência com a EDA:** classes raras (`vehicle`, `Safety Cone`, `Mask`, `NO-Mask`) têm, em geral, métricas mais baixas ou mais instáveis que as classes frequentes — esperado para um baseline de 30 épocas sem técnicas de balanceamento (class weights, oversampling), que podem ser exploradas em iterações futuras.
- **Baseline, não resultado final:** 30 épocas em CPU é um orçamento de tempo deliberadamente reduzido (ver `openspec/changes/archive/*-fase-2-baseline-deteccao/design.md`) para viabilizar a Fase 2 sem GPU. Mais épocas (rodando em Colab GPU) tendem a melhorar essas métricas, especialmente nas classes com poucas instâncias.

## Artefatos

- Pesos: `models/detection/css_yolov8n_baseline/weights/best.pt` e `last.pt` (não versionados — checkpoints grandes)
- Curvas de treino: `models/detection/css_yolov8n_baseline/results.png`, `results.csv`
- Matriz de confusão: `models/detection/css_yolov8n_baseline/confusion_matrix.png` (nota: é uma matriz de confusão de **treino/validação**, preliminar — a matriz de confusão oficial no conjunto de teste é entregue na Fase 4)
- Curvas de precisão/recall por classe: `BoxPR_curve.png`, `BoxF1_curve.png`, `BoxP_curve.png`, `BoxR_curve.png`
