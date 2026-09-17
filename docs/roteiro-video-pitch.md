# Roteiro — Vídeo-Pitch (5-8 min)

Roteiro para apresentar o projeto usando o notebook
`visao_computacional_pipeline_completo.ipynb` como fio condutor, mais a
demo interativa publicada. Estrutura em 10 blocos com tempo sugerido (soma
≈ 7:50, dentro dos 5-8 min exigidos). Ajuste o ritmo conforme for gravando
— é um guia, não um texto para decorar.

**Antes de gravar:**
- Rode o notebook inteiro com antecedência (para não precisar esperar
  treino/download na hora), deixe as células já executadas com saída
  visível.
- Tenha `docs/relatorio-tecnico.md` aberto numa aba para conferir números
  se travar.
- Se o token do Kaggle estiver visível na célula de autenticação, oculte
  essa célula da tela ou troque o token antes de gravar.
- Deixe a aba da **demo Gradio** (link gerado no Colab, `*.gradio.live`)
  já aberta numa aba separada — o link expira em ~72h, gere de novo pouco
  antes de gravar se necessário.

---

## 1. Abertura e cenário (0:00 – 0:35)

**Mostre:** a primeira célula markdown do notebook (título + introdução).

**Fale:**
- Seu nome, a disciplina (Visão Computacional e Reconhecimento de Padrões).
- O problema: em canteiros de obra, fiscalizar manualmente se todo
  trabalhador usa capacete e colete é caro, lento e não escala.
- O que o sistema faz: detecta uso/ausência de EPIs, segmenta pessoas na
  cena, demonstra tudo em vídeo real, e vai além com auditoria automática
  e rastreamento de objetos.

> *"Meu projeto é um sistema de visão computacional para segurança do
> trabalho em canteiros de obra. Ele resolve um problema real: verificar
> manualmente se cada trabalhador está usando capacete e colete é
> inviável em obras grandes. Construí um sistema que detecta EPIs,
> segmenta as pessoas na cena, e transforma isso automaticamente num
> relatório de auditoria — com rastreamento de objetos e uma demo
> interativa publicada."*

## 2. Preparação dos dados (0:35 – 1:20)

**Mostre:** a seção "Etapa 1 — Preparação dos Dados" rodando (ou já
executada), destacando a contagem de imagens e o gráfico de instâncias por
classe (EDA).

**Fale — as duas fontes de dados:**
- **Detecção de EPIs:** dataset público *Construction Site Safety*
  (licença CC BY 4.0), 2.801 imagens; amostra estratificada de **350
  imagens**, garantindo que as 10 classes apareçam.
- **Segmentação de pessoas:** subconjunto do **COCO 2017** (`person`), já
  com máscaras prontas — **300 imagens**, sem anotação manual.
- Splits reprodutíveis: 70/20/10, seed fixa.
- **Achado da EDA:** boa parte das imagens do dataset de EPI são, na
  verdade, mosaicos 2×2 — um detalhe que só percebi ao analisar os dados.

> *"Usei duas fontes públicas: um dataset de canteiro de obra do Kaggle
> para os EPIs, e um subconjunto do COCO para pessoas, que já vem com
> máscaras prontas. A análise exploratória revelou um desbalanceamento
> moderado e que parte do dataset original é composta por
> imagens-mosaico, algo que não era óbvio à primeira vista."*

## 3. Modelos utilizados — detecção (1:20 – 2:10)

**Mostre:** seção "Etapa 2 — Detecção de EPIs", a célula de treino e o
resultado.

**Fale:**
- Modelo: **YOLOv8n** (Ultralytics), pré-treinado no COCO, *fine-tuning*
  para as 10 classes de EPI.
- Hiperparâmetros: 30 épocas, imagens 640×640, batch 16, seed fixa.
- Resultado no **conjunto de teste** (nunca visto): **mAP@0.5 = 0,547**,
  **mAP@0.5:0.95 = 0,324**, **IoU médio = 0,793**.

> *"Para detecção usei o YOLOv8n, com fine-tuning para as 10 classes de
> EPI. No conjunto de teste — dados que o modelo nunca viu — obtive mAP
> de 0,547 e IoU médio de 0,79 nas detecções corretas."*

## 4. Segmentação e comparação caixas × máscaras (2:10 – 3:10)

**Mostre:** seção "Etapa 3 — Segmentação de Pessoas", e a imagem da
comparação caixas × máscaras (3 imagens lado a lado).

**Fale:**
- Modelo: **YOLOv8n-seg**, classe única `person`, mesmos hiperparâmetros
  do detector.
- Resultado no teste: **mask mAP@0.5 = 0,393**, precisão 0,635, recall
  0,376.
- A **caixa** diz *o quê* está presente; a **máscara** mostra *a forma
  exata* da pessoa — contorno, oclusão.
- Limitação honesta: o segmentador só viu o COCO no treino, por isso às
  vezes generaliza mal fora desse domínio.

> *"O segmentador reconhece a silhueta completa da pessoa, não só uma
> caixa. A caixa diz que ali tem uma pessoa sem colete; a máscara mostra
> o contorno exato dela, inclusive onde está parcialmente encoberta — os
> dois se complementam."*

## 5. Avaliação rigorosa e análise de erros (3:10 – 4:10)

**Mostre:** seção "Etapa 4 — Avaliação Rigorosa", a matriz de confusão e
1 exemplo de erro comentado.

**Fale:**
- Avaliação no conjunto de **teste** (nunca visto), não na validação usada
  durante o treino.
- Principais confusões: `Hardhat` ↔ `NO-Hardhat`, `Mask` ↔ `NO-Mask` —
  reconhecer *ausência* é mais difícil que reconhecer presença.
- Análise de erros **objetiva** (maior diferença de contagem, não escolha
  visual): erros se concentram em cenas de alta densidade e objetos
  pequenos.

> *"Testei num conjunto de imagens nunca vistas. As confusões mais comuns
> foram entre presença e ausência do mesmo EPI. Identifiquei que o modelo
> erra mais em cenas com muitas pessoas próximas ou objetos pequenos —
> um padrão claro pra melhorar numa próxima iteração."*

## 6. Demonstração em vídeo (4:10 – 4:50)

**Mostre:** **toque o vídeo anotado** (`video/output/deteccao_epi/...`)
por alguns segundos.

**Fale:**
- Vídeo real, 38s (acima do mínimo de 30s), montado a partir de 3 clipes
  públicos (Pexels).
- Os dois modelos rodaram quadro a quadro, gerando versões anotadas com
  caixas e com máscaras.

> *"Aqui está o sistema rodando num vídeo real, não só em fotos estáticas.
> Dá pra ver o modelo identificando, quadro a quadro, quando um
> trabalhador está sem colete ou sem capacete."*

## 7. Relatório de conformidade (4:50 – 5:40)

**Mostre:** os 3 gráficos gerados (barras, linha do tempo, quadros de
exemplo por classe).

**Fale:**
- Detector quadro a quadro + agrupamento em **eventos** de ausência de EPI
  (início, fim, duração).
- Resultado real: colete ausente em **62,8%** do vídeo, máscara em
  **32,4%**, capacete em **0,3%**.
- A linha do tempo mostra *quando* cada violação ocorreu.

> *"Transformei as detecções num relatório de auditoria automática. Nesse
> vídeo, o colete esteve ausente em quase 63% do tempo — informação
> pronta pra um responsável de segurança consultar sem assistir ao vídeo
> inteiro."*

## 8. Bônus — Rastreamento de objetos (5:40 – 6:30)

**Mostre:** a célula "Bônus — Rastreamento de Objetos" e, se possível,
alguns segundos do vídeo com IDs (`video/output/deteccao_epi_tracking/`),
mostrando o mesmo ID grudado numa pessoa entre quadros.

**Fale:**
- Item de bônus do enunciado: usei **ByteTrack** (embutido no Ultralytics)
  para dar um ID persistente a cada objeto entre quadros.
- Resultado: **99 objetos rastreados**, **20 pessoas únicas** no vídeo.
- Isso permite contar violações **realmente distintas**: 16 objetos
  distintos sem máscara, 26 sem colete — em vez de só "intervalos de
  tempo com detecção".
- Achado extra: o único evento de `NO-Hardhat` do relatório (duração de
  0,1s) **não formou nenhuma track estável** — confirma, de forma
  independente, que era ruído do modelo, não uma detecção real.

> *"Como bônus, implementei rastreamento de objetos com ByteTrack: cada
> objeto ganha um ID que persiste entre quadros. Isso identificou 20
> pessoas únicas no vídeo e permitiu contar violações de EPI realmente
> distintas, não só picos de detecção — e até confirmou que uma das
> detecções do relatório anterior era ruído, porque nunca virou uma track
> estável."*

## 9. Bônus extra — Demo interativa publicada (6:30 – 7:10)

**Mostre:** troque para a aba do navegador com a demo Gradio rodando (link
gerado no Colab). Faça o upload de uma foto de canteiro de obra **ao
vivo** e mostre o resultado aparecendo (caixas + máscara + resumo de
conformidade).

**Fale:**
- Além do notebook, publiquei uma demo interativa (Gradio) onde qualquer
  pessoa sobe uma foto e vê os dois modelos rodando na hora.
- Mencione rapidamente: o enunciado dá bônus por rastreamento *ou* demo
  interativa — já garanti o bônus com o rastreamento, então esta demo é
  um extra além do pedido.

> *"Além de tudo isso, publiquei uma demo interativa onde dá pra testar o
> sistema ao vivo, sem precisar rodar nenhum código — é só subir uma
> foto."* (demonstre com uma foto real na hora)

## 10. Conclusão, limitações e próximos passos (7:10 – 7:50)

**Mostre:** a célula de "Conclusão" no final do notebook.

**Fale:**
- Resumo do que foi entregue: detecção + segmentação + avaliação
  rigorosa + vídeo + relatório de conformidade + rastreamento + demo
  interativa.
- Limitações com transparência: dataset e treino pequenos (baseline, não
  produção), segmentador não viu o domínio de canteiro de obra, cenas
  densas são o ponto fraco mais consistente.
- Próximos passos: mais épocas em GPU, anotar máscaras no próprio
  domínio, balancear classes raras.

> *"Esse projeto entrega um sistema completo — detecção, segmentação,
> avaliação rigorosa, demonstração em vídeo, rastreamento de objetos e
> uma demo pública. As limitações estão documentadas: é um baseline,
> treinado com dados e tempo limitados, e sei exatamente onde ele erra
> mais. Os próximos passos seriam treinar com mais dados e mais tempo de
> GPU."*

---

## Checklist rápido antes de gravar

- [ ] Notebook rodado do início ao fim, com saídas visíveis (gráficos,
      prints, vídeo anotado, célula de rastreamento).
- [ ] Token do Kaggle oculto da gravação (ou trocado por um descartável).
- [ ] Vídeo anotado (`video/output/deteccao_epi/...`) e o vídeo com
      rastreamento (`video/output/deteccao_epi_tracking/...`) prontos
      para tocar um trecho.
- [ ] Aba da demo Gradio aberta e testada (link `*.gradio.live` ainda
      válido — gere de novo se tiver passado ~72h) — tenha 1-2 fotos de
      canteiro de obra prontas no computador pra fazer upload ao vivo.
- [ ] Números principais decorados ou anotados: mAP 0,547 (detecção),
      mask mAP 0,393 (segmentação), IoU 0,793, colete ausente em 62,8% do
      vídeo, 99 objetos rastreados / 20 pessoas únicas.
- [ ] Cronômetro ligado — o enunciado pede 5 a 8 minutos.
