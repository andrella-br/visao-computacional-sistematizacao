# Roteiro — Vídeo-Pitch (5-8 min)

Roteiro para apresentar o projeto usando o notebook
`visao_computacional_pipeline_completo.ipynb` como fio condutor. Estrutura
em 8 blocos com tempo sugerido (soma ≈ 7 min, com folga dentro dos 5-8 min
exigidos). Ajuste o ritmo conforme for gravando — é um guia, não um texto
para decorar.

**Antes de gravar:** rode o notebook inteiro com antecedência (para não
precisar esperar treino/download na hora), deixe as células já executadas
com saída visível, e tenha `docs/relatorio-tecnico.md` aberto numa aba para
conferir números se travar. Se o token do Kaggle estiver visível na célula
de autenticação, considere ocultar essa célula da tela ou trocar o token
antes de gravar.

---

## 1. Abertura e cenário (0:00 – 0:40)

**Mostre:** a primeira célula markdown do notebook (título + introdução).

**Fale:**
- Seu nome, a disciplina (Visão Computacional e Reconhecimento de Padrões).
- O problema: em canteiros de obra, fiscalizar manualmente se todo
  trabalhador usa capacete e colete é caro, lento e não escala para grandes
  obras ou múltiplas câmeras.
- O que o sistema faz: detecta uso/ausência de EPIs, segmenta pessoas na
  cena, e demonstra tudo funcionando em vídeo real — indo além, com uma
  aplicação prática de auditoria automática.

> *"Meu projeto é um sistema de visão computacional para segurança do
> trabalho em canteiros de obra. Ele resolve um problema real: verificar
> manualmente se cada trabalhador está usando capacete e colete é
> inviável em obras grandes. Construí um sistema que detecta EPIs,
> segmenta as pessoas na cena, e transforma isso automaticamente num
> relatório de auditoria."*

## 2. Preparação dos dados (0:40 – 1:40)

**Mostre:** a seção "Etapa 1 — Preparação dos Dados" rodando (ou já
executada), destacando a contagem de imagens e o gráfico de instâncias por
classe (EDA).

**Fale — as duas fontes de dados:**
- **Detecção de EPIs:** dataset público *Construction Site Safety*
  (licença CC BY 4.0), 2.801 imagens reais de canteiro de obra disponíveis;
  usei uma amostra estratificada de **350 imagens**, garantindo que as 10
  classes apareçam (capacete/colete/máscara presentes ou ausentes, pessoa,
  cone, máquina, veículo).
- **Segmentação de pessoas:** subconjunto do **COCO 2017** (categoria
  `person`), que já vem com máscaras prontas — **300 imagens**, sem
  precisar anotar nada manualmente.
- Splits reprodutíveis: 70% treino / 20% validação / 10% teste, com seed
  fixa, para poder comparar resultados de forma justa.
- **Achado interessante da EDA:** boa parte das imagens do dataset de EPI
  são, na verdade, mosaicos 2×2 (4 fotos combinadas em uma) — um detalhe
  que só percebi ao analisar os dados, e que documentei como limitação.

> *"Usei duas fontes públicas: um dataset de canteiro de obra do Kaggle
> para os EPIs, e um subconjunto do COCO para pessoas, que já vem com
> máscaras prontas — isso evitou ter que anotar imagens manualmente. A
> análise exploratória mostrou um desbalanceamento moderado entre classes
> e revelou que parte do dataset original é composta por imagens-mosaico,
> algo que não era óbvio à primeira vista."*

## 3. Modelos utilizados — detecção (1:40 – 2:40)

**Mostre:** seção "Etapa 2 — Detecção de EPIs", a célula de treino e (se já
tiver rodado) o resultado.

**Fale:**
- Modelo: **YOLOv8n** (versão nano da família YOLOv8, da Ultralytics),
  pré-treinado no COCO, com *fine-tuning* para as 10 classes de EPI.
- Por que YOLOv8: framework único que cobre detecção e segmentação de
  instância na mesma família, simplificando a stack do projeto.
- Hiperparâmetros: 30 épocas, imagens 640×640, batch 16, seed fixa —
  documentados integralmente no relatório técnico.
- Resultado no **conjunto de teste** (nunca visto em treino/validação):
  **mAP@0.5 = 0,547**, **mAP@0.5:0.95 = 0,324**, **IoU médio = 0,793**.

> *"Para detecção usei o YOLOv8n, um modelo pequeno da Ultralytics, com
> fine-tuning para as 10 classes de EPI. Treinei por 30 épocas com
> hiperparâmetros documentados no relatório. No conjunto de teste — dados
> que o modelo nunca viu — obtive mAP de 0,547 e um IoU médio de 0,79 nas
> detecções corretas, ou seja, quando o modelo acerta, a caixa prevista se
> sobrepõe bem à caixa real."*

## 4. Segmentação e comparação caixas × máscaras (2:40 – 3:50)

**Mostre:** seção "Etapa 3 — Segmentação de Pessoas", e principalmente a
imagem gerada na comparação caixas × máscaras (as 3 imagens lado a lado:
original, caixas do detector, máscaras do segmentador).

**Fale:**
- Modelo: **YOLOv8n-seg**, mesma família, fine-tuning para a classe única
  `person`, mesmos hiperparâmetros do detector (para manter comparável).
- Resultado no teste: **mask mAP@0.5 = 0,393**, precisão 0,635, recall
  0,376.
- A comparação visual é o ponto-chave desta etapa: rodei os dois modelos
  na mesma imagem do canteiro de obra. A **caixa** diz *o quê* está
  presente (ex. "capacete presente"); a **máscara** mostra *a forma exata*
  da pessoa — contorno, oclusão (ex. uma haste de ferragem passando na
  frente do corpo) — algo que uma caixa retangular não capta.
- Limitação honesta: o segmentador só viu o COCO no treino, nunca um
  canteiro de obra — por isso, às vezes generaliza mal (ex. confundiu um
  pneu de máquina com pessoa). Isso está documentado como limitação.

> *"O segmentador usa YOLOv8n-seg para reconhecer a silhueta completa da
> pessoa, não só uma caixa. Nessa comparação dá pra ver a diferença: a
> caixa diz que ali tem uma pessoa sem colete, mas a máscara mostra o
> contorno exato dela, inclusive onde está parcialmente encoberta. Os dois
> se complementam — um sistema completo usaria as duas informações
> juntas."*

## 5. Avaliação rigorosa e análise de erros (3:50 – 5:00)

**Mostre:** seção "Etapa 4 — Avaliação Rigorosa", a matriz de confusão e
pelo menos 1 dos 4 exemplos de erro comentado (falso positivo ou negativo).

**Fale:**
- Diferente da validação (usada durante o treino), aqui avaliei num
  conjunto de **teste** — dados totalmente novos para o modelo — para ter
  uma medida honesta de desempenho.
- Métricas completas: mAP, IoU, precisão/recall, matriz de confusão.
- Principais confusões: `Hardhat` ↔ `NO-Hardhat` e `Mask` ↔ `NO-Mask` —
  faz sentido, já que reconhecer a *ausência* de algo é mais difícil que
  reconhecer a presença.
- Análise de erros **objetiva**: escolhi os exemplos pela maior diferença
  de contagem entre o esperado e o previsto, não por achar visualmente
  interessante. Padrão encontrado: os erros se concentram em cenas de alta
  densidade (multidões, grupos de pessoas sobrepostas) e objetos pequenos.

> *"Testei os modelos num conjunto de imagens que eles nunca viram. As
> confusões mais comuns foram entre presença e ausência do mesmo EPI — o
> que faz sentido, é mais difícil notar que *falta* algo do que notar que
> *tem* algo. Na análise de erros, identifiquei que o modelo erra mais em
> cenas com muitas pessoas próximas ou objetos pequenos — um padrão claro
> que aponta o que melhorar numa próxima iteração."*

## 6. Demonstração em vídeo (5:00 – 6:00)

**Mostre:** a seção "Etapa 5 — Demonstração em Vídeo" e, principalmente,
**toque o vídeo anotado** (`video/output/deteccao_epi/...`) por alguns
segundos, mostrando as caixas/rótulos sobrepostos em tempo real.

**Fale:**
- Vídeo real de canteiro de obra, 38 segundos (acima do mínimo de 30s
  exigido), montado a partir de 3 clipes públicos (Pexels).
- Os dois modelos rodaram sobre esse vídeo, quadro a quadro, gerando duas
  versões anotadas: uma com as caixas de EPI, outra com as máscaras de
  pessoa.
- Aponte um momento específico do vídeo: por exemplo, um trabalhador sem
  colete sendo corretamente marcado como `NO-Safety Vest`.

> *"Aqui está o sistema rodando num vídeo real, não só em fotos estáticas.
> Dá pra ver o modelo identificando, quadro a quadro, quando um
> trabalhador está sem colete ou sem capacete."*

## 7. Aplicação prática — relatório de conformidade (6:00 – 7:00)

**Mostre:** seção "Etapa 6", os 3 gráficos gerados (barras, linha do
tempo, quadros de exemplo por classe).

**Fale — este é o ponto alto da apresentação, o diferencial prático:**
- Em vez de alguém assistir ao vídeo inteiro procurando violações, o
  sistema roda o detector quadro a quadro e agrupa as detecções de
  ausência de EPI em **eventos** (início, fim, duração, confiança).
- Resultado real do vídeo analisado: colete ausente em **62,8%** do tempo,
  máscara ausente em **32,4%**, capacete ausente em **0,3%**.
- A linha do tempo mostra visualmente *quando* cada violação ocorreu — um
  responsável de segurança consultaria isso diretamente, sem precisar
  rever a gravação manualmente.
- Isso é o que transforma o projeto de "um modelo que detecta objetos" em
  "uma ferramenta que uma empresa de construção poderia usar de verdade".

> *"Fui além da demonstração visual: transformei as detecções num
> relatório de auditoria automática. Olhando pra linha do tempo, dá pra
> ver exatamente quando cada violação aconteceu — nesse vídeo, por
> exemplo, o colete esteve ausente em quase 63% do tempo. Isso é
> informação acionável, pronta pra um responsável de segurança consultar
> sem assistir ao vídeo inteiro."*

## 8. Conclusão, limitações e próximos passos (7:00 – 7:45)

**Mostre:** a célula de "Conclusão" no final do notebook.

**Fale:**
- Resumo do que foi entregue: detecção + segmentação + avaliação rigorosa
  + demonstração em vídeo + aplicação prática.
- Limitações assumidas com transparência: dataset e treino pequenos (um
  *baseline*, não um modelo de produção), segmentador não viu o domínio de
  canteiro de obra no treino, cenas densas são o ponto fraco mais
  consistente.
- Próximos passos: treinar mais épocas com GPU, anotar máscaras no próprio
  domínio, balancear classes raras, e (bônus) rastreamento de objetos ou
  demo interativa.

> *"Esse projeto entrega um sistema completo — não só um modelo que
> detecta objetos, mas uma ferramenta com aplicação prática real. As
> limitações estão documentadas: é um baseline, treinado com dados e tempo
> limitados, e sei exatamente onde ele erra mais. Os próximos passos
> seriam treinar com mais dados e mais tempo de GPU, e estender o
> rastreamento entre quadros do vídeo."*

---

## Checklist rápido antes de gravar

- [ ] Notebook rodado do início ao fim, com saídas visíveis (gráficos,
      prints, vídeo anotado salvo).
- [ ] Token do Kaggle oculto da gravação (ou trocado por um descartável).
- [ ] Vídeo anotado (`video/output/deteccao_epi/...`) pronto para tocar um
      trecho durante a apresentação.
- [ ] Números principais decorados ou anotados: mAP 0,547 (detecção),
      mask mAP 0,393 (segmentação), IoU 0,793, colete ausente em 62,8% do
      vídeo.
- [ ] Cronômetro ligado — o enunciado pede 5 a 8 minutos.
