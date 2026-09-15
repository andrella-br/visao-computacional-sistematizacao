## Context

A Fase 1 preparou o subconjunto COCO `person` em formato COCO (JSON com polígonos), não em formato treinável por YOLO. A Fase 2 já validou o fluxo de treino local em CPU com Ultralytics (YOLOv8n, detecção). Um smoke test de 1 época com YOLOv8n-seg (210 imagens de treino, batch=16, imgsz=640) levou ~162s, próximo do medido na Fase 2 para detecção.

## Goals / Non-Goals

**Goals:**
- Reaproveitar a mesma ferramenta (Ultralytics) e convenções de hiperparâmetro da Fase 2, para manter o projeto consistente e comparável.
- Converter as anotações COCO para YOLO-seg sem perder instâncias (poligonos com menos de 3 pontos são descartados por não formarem uma área válida).
- Produzir uma comparação visual caixas×máscaras genuína, não apenas conceitual: rodar o segmentador (treinado em pessoas do COCO) sobre imagens do **domínio de canteiro de obra** (dataset da Fase 2), já que a classe `person` generaliza entre os dois domínios.

**Non-Goals:**
- Não é objetivo re-anotar ou aumentar o subconjunto COCO.
- Não é objetivo treinar em Mask R-CNN/DeepLab/U-Net — YOLOv8n-seg (instância) atende ao requisito do enunciado e mantém a mesma stack de ferramentas.

## Decisions

**Decisão 1 — Conversão manual COCO→YOLO-seg (sem pycocotools).**
Os polígonos do JSON já filtrado na Fase 1 (`iscrowd=0`, só `person`) são convertidos diretamente para linhas YOLO-seg (classe + coordenadas normalizadas), sem depender de `pycocotools` (evita mais uma dependência e mascaras RLE, que não aparecem neste subconjunto — confirmado: 100% dos registros são polígonos, não RLE).

**Decisão 2 — YOLOv8n-seg, 30 épocas, mesmos hiperparâmetros de forma (imgsz=640, batch=16, seed=42, optimizer=auto).**
Consistência com a Fase 2 facilita comparação e documentação. 30 épocas ≈ 81 minutos medidos empiricamente — mesmo orçamento de tempo aceito na Fase 2.

**Decisão 3 — Comparação caixas×máscaras nas imagens do canteiro de obra, não do COCO.**
Diferente do que o `design.md` da Fase 1 havia planejado (comparação "conceitual" entre domínios diferentes), agora com os dois modelos treinados é possível rodar o segmentador (person, treinado no COCO) diretamente sobre 2-3 imagens do dataset de EPIs (que também contêm pessoas) e comparar com as caixas do detector da Fase 2 **na mesma imagem**. Isso produz uma comparação visual real e mais informativa do que a alternativa puramente conceitual. Risco aceito: o segmentador nunca viu imagens de canteiro de obra durante o treino (generalização fora do domínio de treino), o que é declarado explicitamente na análise.

## Risks / Trade-offs

- [Risco] Segmentador treinado só em COCO pode generalizar mal para poses/oclusões típicas de canteiro de obra (capacete, colete, equipamento) → Mitigação: aceitável para uma comparação qualitativa ilustrativa da Fase 3; qualidade quantitativa da segmentação nesse domínio cruzado não é o objetivo desta fase.
- [Risco] Polígonos multi-parte (pessoa ocluída, mais de um polígono por instância) podem gerar múltiplas linhas YOLO-seg para a mesma instância → Aceito: é o comportamento padrão do formato YOLO-seg para instâncias com múltiplas regiões; não afeta a métrica de mAP de forma incorreta.
