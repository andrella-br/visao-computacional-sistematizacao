# Relatório Técnico — Sistema de Visão Computacional para Segurança do Trabalho

**CEUB - Centro Universitário de Brasília**

**Pós-graduação em Engenharia de IA** 

**Disciplina:** Visão Computacional e Reconhecimento de Padrões (Prof. Romes Heriberto)

**RA: 82600743** 

**Aluno:** André Luiz Lopes de Azevedo

**Notebook Google Colab:** https://colab.research.google.com/drive/1rgTu0MlXdp5G9vLv50gLbI_9H61HY3yW?usp=sharing

**Repositório:** https://github.com/andrella-br/visao-computacional-sistematizacao

**Vídeo de Apresentação:** https://drive.google.com/file/d/1J6dCePB5x3PLGFHZLZDyKc9cJhC9-FBF/view?usp=sharing

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

Os subconjuntos foram selecionados por **amostragem estratificada com seed fixa (42)**, garantindo pelo menos 15 imagens por classe de EPI (evitando que classes raras como `Safety Cone` ou `vehicle` ficassem ausentes) e volume mínimo de 300 imagens por fonte.

### 2.2 Análise exploratória

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


### 2.3 Splits reprodutíveis

Ambas as fontes foram divididas 70/20/10 (treino/validação/teste) com a mesma seed (42):

| Fonte | Treino | Validação | Teste | Total |
|---|---:|---:|---:|---:|
| construction-site-safety | 244 | 70 | 36 | 350 |
| coco-person | 210 | 60 | 30 | 300 |

## 3. Metodologia

Ambos os modelos foram treinados localmente, usando **Ultralytics YOLOv8** — escolhido por já vir com suporte nativo a detecção e segmentação de instância na mesma família de modelos, simplificando a stack de ferramentas do projeto.

### 3.1 Detecção (Fase 2)

- **Modelo:** YOLOv8n (nano), pré-treinado no COCO, fine-tuning para as 10 classes de EPI.
- **Hiperparâmetros:** 30 épocas, `imgsz=640`, `batch=16`, otimizador `auto`, seed=42.
- **Tempo de treino:** ~59 minutos (CPU).

### 3.2 Segmentação (Fase 3)

- **Modelo:** YOLOv8n, pré-treinado no COCO, fine-tuning para a classe única `person`.
- **Conversão de dados:** os polígonos de anotação do COCO (formato JSON) foram convertidos para o formato YOLO-seg (labels `.txt` com coordenadas normalizadas).
- **Hiperparâmetros:** mesma configuração da Fase 2 (30 épocas, `imgsz=640`, `batch=16`, seed=42), para manter os dois modelos comparáveis.
- **Tempo de treino:** ~61 minutos (CPU).

## 4. Resultados

### 4.1 Validação 

| Métrica | Detector (EPI) | Segmentador — caixa | Segmentador — máscara |
|---|---:|---:|---:|
| Precisão | 0.608 | 0.738 | 0.697 |
| Recall | 0.464 | 0.509 | 0.507 |
| mAP@0.5 | 0.490 | 0.561 | 0.559 |
| mAP@0.5:0.95 | 0.278 | 0.333 | 0.288 |


### 4.2 Avaliação no conjunto de TESTE 

| Métrica | Detector (EPI) | Segmentador — caixa | Segmentador — máscara |
|---|---:|---:|---:|
| Precisão | 0.710 | 0.682 | 0.635 |
| Recall | 0.481 | 0.386 | 0.376 |
| mAP@0.5 | 0.547 | 0.443 | 0.393 |
| mAP@0.5:0.95 | 0.324 | 0.231 | 0.177 |
| **IoU médio (TP)** | **0.793** (n=316 caixas) | — | — |


**Matriz de confusão do detector (teste):** as principais confusões observadas foram `NO-Hardhat` ↔ `Hardhat` e `NO-Mask` ↔ `Mask` — esperado, já que essas classes descrevem o mesmo objeto em estados opostos (presente vs. ausente), e perceber a *ausência* de algo é uma tarefa mais difícil do que detectar sua presença.

### 4.3 Métricas por Classe 

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


## 5. Análise de Erros 


1. **Falso Negativo — multidão com máscaras não detectada:** .
2. **Falso Negativo — pessoas ao fundo de um grupo não contadas:** 
3. **Falso Positivo — caixas duplicadas e confusão de classe:** 
4. **Falso Positivo — pessoas contadas em excesso:** 


## 6. Comparação Caixas × Máscaras


- **Caixa (detector):** informa *o quê* está presente, mas é uma aproximação retangular grosseira da forma real do objeto.
- **Máscara (segmentador):** informa *a forma exata* da pessoa, mas não sabe nada sobre equipamento.
- **Conclusão:** os dois modelos são complementares. Um sistema completo de auditoria se beneficiaria de combinar as duas saídas (ex. usar a máscara para recortar a região de interesse e aplicar o detector de EPI só ali).
- **Limitação observada:** o segmentador, treinado apenas no COCO, gerou pelo menos um falso positivo de máscara sobre um pneu de máquina. 

## 7. Aplicação Prática: Relatório de Conformidade de EPI


Resultado sobre o vídeo de 38.3s analisado:

| Classe de violação | Eventos | Tempo total | % do vídeo |
|---|---:|---:|---:|
| NO-Safety Vest | 4 | 24.0s | 62.8% |
| NO-Mask | 7 | 12.4s | 32.4% |
| NO-Hardhat | 1 | 0.1s | 0.3% |


## 8. Demonstração em Vídeo

Vídeo de entrada: `video/input/video_final_canteiro_obra.mp4`.

Os dois modelos foram aplicados ao mesmo vídeo, gerando duas saídas anotadas:

- `video/output/deteccao_epi/` — caixas de EPI sobrepostas em cada quadro.
- `video/output/segmentacao_pessoas/` — máscaras de pessoa sobrepostas em cada quadro.


## Rastreamento de Objetos (ByteTrack)

O detector foi rodado com **ByteTrack** (tracker embutido no Ultralytics) sobre o mesmo vídeo, atribuindo um **ID persistente** a cada objeto entre quadros — não apenas uma detecção isolada por quadro.

**Resultado:**

| Métrica | Valor |
|---|---:|
| Objetos rastreados (tracks únicos) | 99 |
| Pessoas únicas (`Person`) no vídeo | 20 |
| `NO-Hardhat` — objetos distintos | 0 |
| `NO-Mask` — objetos distintos | 16 |
| `NO-Safety Vest` — objetos distintos | 26 |


## Demo Interativa (Gradio)


A demo roda em uma sessão do Google Colab e gera um link público temporário.

## 9. Limitações e Próximos Passos

**Limitações:**
- Dataset de treino pequeno (350 + 300 imagens) e treino curto (30 épocas em CPU).
- Parte do dataset de detecção é composta por imagens-mosaico, o que pode ter afetado marginalmente o aprendizado de contexto espacial.
- Segmentador nunca viu o domínio de canteiro de obra durante o treino (apenas COCO), gerando falsos positivos/negativos ao generalizar para esse domínio.
- Cenas de multidões, grupos sobrepostos são o ponto fraco mais consistente do detector.
- Conjuntos de teste pequenos tornam as métricas de teste sensíveis à composição específica das imagens.

**Próximos passos (fora do escopo desta entrega):**
- Aplicar técnicas de balanceamento para as classes minoritárias (`vehicle`, `Mask`, `Safety Cone`).
- Aumentar o limiar de confiança e a duração mínima de evento no relatório de conformidade, para reduzir ruído de falsos positivos pontuais.

## 10. Referências e Fontes de Dados

- **Construction Site Safety Image Dataset (Roboflow)** — Roboflow Universe, espelhado no Kaggle por `snehilsanyal`. CC BY 4.0. https://www.kaggle.com/datasets/snehilsanyal/construction-site-safety-image-dataset-roboflow
- **COCO 2017 (Common Objects in Context)** — Lin et al., 2014. Licença padrão COCO. https://cocodataset.org/
- **Vídeos de demonstração** — Pexels (Pexels License). Ver `video/input/README.md` para os 3 links individuais.
- **Ultralytics YOLOv8** — framework usado para detecção e segmentação. https://docs.ultralytics.com/
