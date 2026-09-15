# Análise Exploratória (EDA) — Fase 1

## Dataset de detecção: Construction Site Safety (subconjunto)

- **Fonte:** Construction Site Safety (Roboflow Universe / espelhado no Kaggle por `snehilsanyal`), licença CC BY 4.0.
- **Subconjunto usado:** 350 de 2.801 imagens disponíveis, selecionadas por amostragem estratificada (seed=42) garantindo pelo menos 15 imagens por classe.
- **Formato:** YOLO (imagem + `.txt` de bounding boxes por classe).
- **Resolução:** todas as imagens em 640×640 px (padronizado pelo pipeline de export do Roboflow).
- **Brilho médio (proxy de iluminação, amostra de 150 imagens):** varia de 26.3 a 203.2 (escala 0-255), média 115.9 — indica boa diversidade de condições de luz (imagens escuras e claras presentes).

### Instâncias por classe (350 imagens)

| Classe | Instâncias | % do total |
|---|---:|---:|
| Person | 1246 | 25.4% |
| machinery | 670 | 13.6% |
| NO-Safety Vest | 525 | 10.7% |
| Safety Cone | 493 | 10.0% |
| NO-Mask | 426 | 8.7% |
| Hardhat | 406 | 8.3% |
| Safety Vest | 410 | 8.3% |
| NO-Hardhat | 316 | 6.4% |
| Mask | 214 | 4.4% |
| vehicle | 207 | 4.2% |

Gráfico: `reports/figures/css_instances_per_class.png`
Gráfico de resolução/brilho: `reports/figures/css_resolution_brightness.png`

### Desbalanceamento

A classe mais frequente (`Person`, 1246 instâncias) é ~6× mais frequente que a menos frequente (`vehicle`, 207 instâncias). É um desbalanceamento moderado, não extremo — a amostragem estratificada (mínimo de 15 imagens por classe na seleção) evitou que classes raras como `Safety Cone` ou `vehicle` ficassem ausentes do subconjunto. Para a Fase 2, vale considerar:
- Usar `class weights` ou focal loss se o detector performar mal nas classes minoritárias (`vehicle`, `Mask`).
- Monitorar métricas por classe (não só mAP agregado) na validação.

## Dataset de segmentação: COCO (subconjunto, categoria `person`)

- **Fonte:** COCO 2017 (val2017), categoria `person`, licença padrão COCO (uso livre com atribuição).
- **Subconjunto usado:** 300 imagens (de 2.693 elegíveis com pelo menos 1 instância de `person` com máscara), seed=42.
- **Anotações:** 1.280 instâncias de `person` com máscara de segmentação de instância (polígono/RLE), prontas — sem necessidade de anotação manual.
- **Tamanho em disco:** ~47MB (300 imagens + JSON de anotações filtrado).

## Splits reprodutíveis

Ambas as fontes foram divididas com a mesma seed (42), proporção 70/20/10 (treino/validação/teste), salvas como listas de arquivos em `data/splits/<fonte>/{train,val,test}.txt`:

| Fonte | Treino | Validação | Teste | Total |
|---|---:|---:|---:|---:|
| construction-site-safety | 244 | 70 | 36 | 350 |
| coco-person | 210 | 60 | 30 | 300 |

Rodar `python src/data/make_splits.py` novamente reproduz exatamente os mesmos splits (mesma seed, mesma lista de arquivos ordenada antes do shuffle).
