# Relatório Técnico — Sistema de Visão Computacional para Segurança do Trabalho

**Disciplina:** Pós-graduação · Visão Computacional e Reconhecimento de Padrões (Prof. Romes Heriberto)
**Integrante:** 1 (trabalho individual)
**Repositório:** ver `README.md` para estrutura de pastas e instruções de reprodução.

---

## 1. Problema e Cenário

Em canteiros de obra, o não uso de Equipamentos de Proteção Individual (EPI) — capacete e colete de segurança — é uma das principais causas de acidentes de trabalho. A fiscalização manual desse uso é cara, lenta e não escala para grandes obras ou múltiplas câmeras.

Este projeto constrói, de ponta a ponta, um sistema de visão computacional que:

1. **Detecta** o uso ou a ausência de EPIs (capacete, colete, máscara) em imagens de canteiro de obra, classificando também pessoas, cones de sinalização, máquinas e veículos;
2. **Segmenta** as pessoas presentes na cena (silhueta completa, não apenas caixa delimitadora);
3. Demonstra o funcionamento dos dois modelos em um **vídeo real** do cenário;
4. Vai além da demonstração visual e converte as detecções em um **relatório de conformidade** — uma aplicação prática de auditoria automática de segurança.

O cenário (Segurança do Trabalho) é um dos exemplos citados no próprio enunciado da disciplina.

## 2. Dataset e Análise Exploratória (EDA)

### 2.1 Fontes de dados

Foram usadas duas fontes públicas, cada uma cobrindo uma das duas tarefas do projeto — nenhuma anotação manual foi necessária:

| Tarefa | Fonte | Licença | Volume total disponível | Subconjunto usado |
|---|---|---|---:|---:|
| Detecção (10 classes de EPI) | [Construction Site Safety](https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow) (Roboflow Universe, espelhado no Kaggle por `snehilsanyal`) | CC BY 4.0 | 2.801 imagens | 350 imagens |
| Segmentação (classe `person`) | [COCO 2017](https://cocodataset.org/) (conjunto de validação, categoria `person`) | Licença padrão COCO (uso livre com atribuição) | 2.693 imagens elegíveis (com máscara de pessoa) | 300 imagens |

As **10 classes de detecção** são: `Hardhat`, `NO-Hardhat`, `Safety Vest`, `NO-Safety Vest`, `Mask`, `NO-Mask`, `Person`, `Safety Cone`, `machinery`, `vehicle`. A **classe de segmentação** é `person` (silhueta completa).

Os subconjuntos foram selecionados por **amostragem estratificada com seed fixa (42)**, garantindo pelo menos 15 imagens por classe de EPI (evitando que classes raras como `Safety Cone` ou `vehicle` ficassem ausentes) e volume mínimo de 300 imagens por fonte, conforme exigido pelo enunciado — sem baixar os datasets completos, o que pesaria desnecessariamente no treino local em CPU.

### 2.2 Análise exploratória

- **Resolução:** todas as imagens do dataset de detecção já vêm padronizadas em 640×640 px (pipeline de export do Roboflow).
- **Iluminação:** brilho médio (amostra de 150 imagens) variando de 26.3 a 203.2 (escala 0-255), média 115.9 — boa diversidade de condições de luz.
- **Desbalanceamento de classes:** a classe mais frequente (`Person`, 1.246 instâncias) é ~6× mais frequente que a menos frequente (`vehicle`, 207 instâncias) — desbalanceamento moderado, não extremo, graças à amostragem estratificada.

| Classe | Instâncias | % do total |
|---|---:|---:|
| Person | 1246 | 25.4% |
| machinery | 670 | 13.6% |
| NO-Safety Vest | 525 | 10.7% |
| Safety Cone | 493 | 10.0% |
| NO-Mask | 426 | 8.7% |
| Safety Vest | 410 | 8.3% |
| Hardhat | 406 | 8.3% |
| NO-Hardhat | 316 | 6.4% |
| Mask | 214 | 4.4% |
| vehicle | 207 | 4.2% |

**Achado inesperado (descoberto na Fase 3):** boa parte das imagens do Construction Site Safety são, na verdade, **mosaicos 2×2** (4 fotos distintas combinadas em uma única imagem), provavelmente herdados de uma etapa de augmentation "Mosaic" do Roboflow que ficou embutida na exportação usada. Isso não invalida o treino — cada quadrante ainda contém objetos e caixas válidas — mas é uma característica do dataset a se considerar ao interpretar os resultados, e exigiu recortar quadrantes individuais para produzir exemplos visuais legíveis na Fase 3.

### 2.3 Splits reprodutíveis

Ambas as fontes foram divididas 70/20/10 (treino/validação/teste) com a mesma seed (42), salvas como listas de arquivos versionadas (`data/splits/<fonte>/{train,val,test}.txt`):

| Fonte | Treino | Validação | Teste | Total |
|---|---:|---:|---:|---:|
| construction-site-safety | 244 | 70 | 36 | 350 |
| coco-person | 210 | 60 | 30 | 300 |

## 3. Metodologia

Ambos os modelos foram treinados localmente em **CPU** (sem GPU disponível no ambiente de desenvolvimento), usando **Ultralytics YOLOv8** — escolhido por já vir com suporte nativo a detecção e segmentação de instância na mesma família de modelos, simplificando a stack de ferramentas do projeto.

### 3.1 Detecção (Fase 2)

- **Modelo:** YOLOv8n (nano), pré-treinado no COCO, fine-tuning para as 10 classes de EPI.
- **Hiperparâmetros:** 30 épocas, `imgsz=640`, `batch=16`, otimizador `auto` (Ultralytics escolheu AdamW, lr0=0.000714, momentum=0.9), seed=42.
- **Augmentation (padrão Ultralytics):** `hsv_h=0.015`, `hsv_s=0.7`, `hsv_v=0.4`, `translate=0.1`, `scale=0.5`, `fliplr=0.5`, `mosaic=1.0`, `auto_augment=randaugment`, `erasing=0.4` (sem rotação/shear/perspective/mixup/copy_paste).
- **Tempo de treino:** ~59 minutos (CPU).
- Justificativa do orçamento de 30 épocas: um teste empírico de 1 época (~173s) indicou que 30 épocas (~87 min estimados, 59 min reais) era o teto viável para treinar em CPU nesta sessão, mantendo o baseline honesto — mais épocas em GPU (Colab) tendem a melhorar as métricas.

### 3.2 Segmentação (Fase 3)

- **Modelo:** YOLOv8n-seg (nano), pré-treinado no COCO, fine-tuning para a classe única `person`.
- **Conversão de dados:** os polígonos de anotação do COCO (formato JSON) foram convertidos para o formato YOLO-seg (labels `.txt` com coordenadas normalizadas), sem uso de `pycocotools` — script próprio (`src/step07_segmentation_prepare_yolo_config.py`).
- **Hiperparâmetros:** mesma configuração da Fase 2 (30 épocas, `imgsz=640`, `batch=16`, seed=42), para manter os dois modelos comparáveis.
- **Tempo de treino:** ~61 minutos (CPU).

## 4. Resultados

### 4.1 Validação (durante o treino)

| Métrica | Detector (EPI) | Segmentador — caixa | Segmentador — máscara |
|---|---:|---:|---:|
| Precisão | 0.608 | 0.738 | 0.697 |
| Recall | 0.464 | 0.509 | 0.507 |
| mAP@0.5 | 0.490 | 0.561 | 0.559 |
| mAP@0.5:0.95 | 0.278 | 0.333 | 0.288 |

O segmentador teve desempenho de validação superior ao detector — esperado, pois é uma tarefa de classe única (`person`) sobre um dataset (COCO) mais próximo da distribuição de pré-treino do modelo, enquanto o detector lida com 10 classes específicas de domínio (EPIs), menos representadas no pré-treino genérico.

### 4.2 Avaliação no conjunto de TESTE (nunca visto em treino/validação)

| Métrica | Detector (EPI) | Segmentador — caixa | Segmentador — máscara |
|---|---:|---:|---:|
| Precisão | 0.710 | 0.682 | 0.635 |
| Recall | 0.481 | 0.386 | 0.376 |
| mAP@0.5 | 0.547 | 0.443 | 0.393 |
| mAP@0.5:0.95 | 0.324 | 0.231 | 0.177 |
| **IoU médio (TP)** | **0.793** (n=316 caixas) | — | — |

O detector teve desempenho no teste ligeiramente **melhor** que na validação (mAP@0.5: 0.547 vs. 0.490) — plausível para um conjunto de teste pequeno (36 imagens), onde a composição específica pode favorecer as métricas por acaso amostral. O segmentador, ao contrário, teve desempenho **inferior** no teste (mask mAP@0.5: 0.393 vs. 0.559) — mesmo raciocínio, mas na direção oposta, com um conjunto de teste de apenas 30 imagens.

**Matriz de confusão do detector (teste):** as principais confusões observadas foram `NO-Hardhat` ↔ `Hardhat` e `NO-Mask` ↔ `Mask` — esperado, já que essas classes descrevem o mesmo objeto em estados opostos (presente vs. ausente), e perceber a *ausência* de algo é uma tarefa mais difícil do que detectar sua presença.

### 4.3 Métricas por classe (detector, subconjunto completo — Fase 2)

| Classe | Precisão | Recall | mAP@0.5 | mAP@0.5:0.95 |
|---|---:|---:|---:|---:|
| machinery | 0.665 | 0.667 | 0.714 | 0.519 |
| Person | 0.716 | 0.626 | 0.665 | 0.428 |
| Mask | 0.803 | 0.533 | 0.635 | 0.371 |
| Hardhat | 0.565 | 0.568 | 0.576 | 0.305 |
| Safety Vest | 0.604 | 0.411 | 0.476 | 0.254 |
| NO-Safety Vest | 0.602 | 0.387 | 0.483 | 0.255 |
| vehicle | 0.615 | 0.467 | 0.439 | 0.328 |
| NO-Hardhat | 0.644 | 0.455 | 0.443 | 0.180 |
| Safety Cone | 0.449 | 0.301 | 0.274 | 0.084 |
| NO-Mask | 0.416 | 0.223 | 0.195 | 0.060 |

O melhor desempenho ocorre nas classes mais frequentes (`machinery`, `Person`); o pior, em `NO-Mask` — também uma das classes menos frequentes — confirmando a relação entre volume de dados por classe e desempenho, esperada para um baseline sem técnicas de balanceamento (class weights, oversampling).

## 5. Análise de Erros (detector, conjunto de teste)

Quatro exemplos foram selecionados **objetivamente** pela maior discrepância de contagem de instâncias por classe entre ground-truth e predição (não por escolha visual arbitrária) — ver `reports/figures/erro_1..4_*.png`.

1. **Falso Negativo — multidão com máscaras não detectada:** 5 instâncias de `Mask` não detectadas numa cena de multidão urbana ao fundo. Causa provável: rostos muito pequenos e densamente agrupados — desafio clássico para detectores single-shot como o YOLO.
2. **Falso Negativo — pessoas ao fundo de um grupo não contadas:** 4 instâncias de `Person` e 4 de `Hardhat` não detectadas num grupo compacto. Causa provável: oclusão parcial entre pessoas próximas.
3. **Falso Positivo — caixas duplicadas e confusão de classe:** múltiplas caixas sobrepostas para a mesma pessoa, e uma caixa de `machinery` sobre uma textura de parede de pedra (sem máquina real). Causas prováveis: (a) NMS não suprimiu completamente caixas redundantes; (b) textura visualmente similar a peças de maquinário.
4. **Falso Positivo — pessoas contadas em excesso:** 4 instâncias extras de `Person` numa cena de múltiplas pessoas sobrepostas — mesmo padrão de densidade do erro 2.

**Padrão geral:** três dos quatro erros analisados envolvem **cenas de alta densidade** (multidões, grupos sobrepostos) ou **objetos pequenos** — um padrão consistente de dificuldade do baseline (30 épocas, dataset de 350 imagens), independente do tipo de erro (FP ou FN). Mais épocas de treino e/ou mais dados de cenas densas são a extensão natural para melhorar esse ponto.

## 6. Comparação Caixas × Máscaras

O detector (Fase 2) e o segmentador (Fase 3) foram rodados sobre as **mesmas imagens** do domínio de canteiro de obra (fora do domínio de treino do segmentador, que só viu COCO), para ilustrar o que cada abordagem revela:

- **Caixa (detector):** informa *o quê* está presente — EPI usado ou não, por classe — mas é uma aproximação retangular grosseira da forma real do objeto.
- **Máscara (segmentador):** informa *a forma exata* da pessoa — silhueta, contorno, oclusão parcial (ex. hastes de ferragem passando à frente do corpo) — mas não sabe nada sobre equipamento.
- **Conclusão:** os dois modelos são complementares. Um sistema completo de auditoria se beneficiaria de combinar as duas saídas (ex. usar a máscara para recortar a região de interesse e aplicar o detector de EPI só ali).
- **Limitação observada:** o segmentador, treinado apenas no COCO, gerou pelo menos um falso positivo de máscara sobre um pneu de máquina — esperado, já que nunca viu esse domínio durante o treino.

Ver `reports/segmentacao-fase3.md` e `reports/figures/boxes_vs_masks_example_{1,2}.png` para os exemplos visuais completos.

## 7. Aplicação Prática: Relatório de Conformidade de EPI

Além da demonstração visual em vídeo, as detecções do detector foram convertidas em uma **aplicação prática de auditoria automática de segurança**: o detector roda quadro a quadro sobre o vídeo, captura toda detecção das classes de violação (`NO-Hardhat`, `NO-Mask`, `NO-Safety Vest`) e agrupa detecções consecutivas em **eventos** (início, fim, duração, confiança média) — em vez de exigir que alguém assista ao vídeo inteiro para descobrir onde houve violação.

Resultado sobre o vídeo de 38.3s analisado:

| Classe de violação | Eventos | Tempo total | % do vídeo |
|---|---:|---:|---:|
| NO-Safety Vest | 4 | 24.0s | 62.8% |
| NO-Mask | 7 | 12.4s | 32.4% |
| NO-Hardhat | 1 | 0.1s | 0.3% |

Os dados brutos ficam em `reports/violacoes-epi.parquet` (formato colunar/tipado) e o relatório legível em `reports/relatorio-conformidade-epi.md`. Um responsável de segurança do trabalho consultaria diretamente esses eventos, sem precisar rever a gravação manualmente. Nota: alguns eventos têm duração muito curta (~0s) e confiança próxima do limiar (0.25), provavelmente falsos positivos pontuais do baseline — um sistema de produção usaria um limiar de confiança mais alto e/ou duração mínima de evento para reduzir ruído.

## 8. Demonstração em Vídeo

Vídeo de entrada: `video/input/video_final_canteiro_obra.mp4` — 1280×720, 25fps, **38.3 segundos** (acima do mínimo de 30s exigido), consolidado a partir de 3 clipes gratuitos do [Pexels](https://www.pexels.com/) (licença Pexels License, uso livre sem atribuição obrigatória — fontes e links em `video/input/README.md`). Nenhum dos 3 clipes originais (19.8s, 8.4s, 10.1s) atingia sozinho o mínimo exigido; foram concatenados com padronização de resolução (letterbox para os clipes em retrato) e taxa de quadros (25fps).

Os dois modelos foram aplicados ao mesmo vídeo, gerando duas saídas anotadas:

- `video/output/deteccao_epi/` — caixas de EPI sobrepostas em cada quadro.
- `video/output/segmentacao_pessoas/` — máscaras de pessoa sobrepostas em cada quadro.

Em uma verificação pontual (dois trabalhadores empurrando um carrinho de mão), o detector identificou corretamente `Person` e `NO-Safety Vest` para ambos; o segmentador detectou corretamente apenas um dos dois trabalhadores no mesmo instante — consistente com o recall moderado medido no teste (0.376 para máscaras) e com a limitação de generalização entre domínios (COCO → canteiro de obra).

## 9. Limitações e Próximos Passos

**Limitações:**
- Dataset de treino pequeno (350 + 300 imagens) e treino curto (30 épocas em CPU) — um baseline, não um modelo de produção.
- Parte do dataset de detecção é composta por imagens-mosaico (achado documentado na Fase 3), o que pode ter afetado marginalmente o aprendizado de contexto espacial.
- Segmentador nunca viu o domínio de canteiro de obra durante o treino (apenas COCO), gerando falsos positivos/negativos ao generalizar para esse domínio.
- Cenas de alta densidade (multidões, grupos sobrepostos) são o ponto fraco mais consistente do detector, tanto em falsos positivos quanto negativos.
- Conjuntos de teste pequenos (36 e 30 imagens) tornam as métricas de teste sensíveis à composição específica das imagens.

**Próximos passos (fora do escopo desta entrega):**
- Treinar por mais épocas em GPU (Colab), reaproveitando os mesmos hiperparâmetros documentados, para comparar ganho de desempenho.
- Anotar (ou usar Smart Polygon assistido por SAM) máscaras de pessoa no próprio domínio de canteiro de obra, eliminando a limitação de generalização cruzada de domínio do segmentador.
- Aplicar técnicas de balanceamento (class weights, oversampling) para as classes minoritárias (`vehicle`, `Mask`, `Safety Cone`).
- Rastreamento de objetos em vídeo (ByteTrack/DeepSORT) e/ou demo interativa (Gradio), como bônus opcional do enunciado.
- Aumentar o limiar de confiança e a duração mínima de evento no relatório de conformidade, para reduzir ruído de falsos positivos pontuais.

## 10. Referências e Fontes de Dados

- **Construction Site Safety Image Dataset (Roboflow)** — Roboflow Universe, espelhado no Kaggle por `snehilsanyal`. CC BY 4.0. https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow
- **COCO 2017 (Common Objects in Context)** — Lin et al., 2014. Licença padrão COCO. https://cocodataset.org/
- **Vídeos de demonstração** — Pexels (Pexels License). Ver `video/input/README.md` para os 3 links individuais.
- **Ultralytics YOLOv8** — framework usado para detecção e segmentação. https://docs.ultralytics.com/

## Sobre o uso de IA generativa

Este projeto foi desenvolvido com apoio do Claude Code (Anthropic) como assistente de programação, seguindo o padrão de desenvolvimento orientado a especificações (OpenSpec — ver `openspec/`), com cada fase do roadmap planejada (proposta, especificação, tarefas) antes da implementação. Todas as decisões de escopo, cenário, dataset e hiperparâmetros foram revisadas e aprovadas pelo integrante ao longo do processo, registradas no histórico de mudanças arquivadas em `openspec/changes/archive/`.
