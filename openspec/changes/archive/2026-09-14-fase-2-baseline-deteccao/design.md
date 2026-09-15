## Context

O ambiente de execução desta sessão não tem GPU (`torch` instalado em modo CPU). O enunciado sugere Colab (GPU), mas o integrante optou por treinar localmente agora para ter resultados reais mais cedo, aceitando o trade-off de tempo. Um teste empírico de 1 época (YOLOv8n, batch=16, imgsz=640, 244 imagens de treino) levou ~173s. Ver `proposal.md` para o porquê da escolha do dataset/modelo.

## Goals / Non-Goals

**Goals:**
- Definir um orçamento de épocas viável em CPU nesta sessão (idealmente < 2h de execução).
- Escolher hiperparâmetros que sejam facilmente portáveis para Colab (GPU) depois, sem precisar re-derivar decisões.
- Evitar problemas de path/encoding no Windows (nome do projeto tem acentos e espaço: "Visão Computacional e Reconhecimento de Padrões").

**Non-Goals:**
- Não é objetivo obter o melhor mAP possível nesta fase — é um **baseline**. Ajuste fino de hiperparâmetros fica para iterações futuras se necessário.
- Não é objetivo rodar avaliação completa no conjunto de teste (Fase 4) nem gerar o notebook Colab oficial de entrega (Fase 5) — o script local pode ser adaptado para um notebook depois, mas isso não é parte desta mudança.

## Decisions

**Decisão 1 — YOLOv8n (nano), não uma variante maior.**
Entre os modelos Ultralytics (n/s/m/l/x), o nano é o único viável em tempo razoável em CPU. Alternativa considerada: YOLOv8s (mais preciso); rejeitada por multiplicar o tempo de treino em CPU sem necessidade para um baseline.

**Decisão 2 — 30 épocas.**
Com ~173s/época medidos, 30 épocas ≈ 87 minutos — tempo aceitável para rodar em background nesta sessão. Alternativa considerada: 50-100 épocas (mais robusto, mas 2,5-8h em CPU); rejeitada para a Fase 2. Fica documentado que, ao portar para Colab (GPU) na entrega final, o mesmo script permite aumentar `epochs` sem mudar o resto da configuração.

**Decisão 3 — batch=16, imgsz=640, otimizador automático (`optimizer=auto`, escolhe AdamW).**
`imgsz=640` porque o dataset já vem padronizado nessa resolução (ver EDA da Fase 1) — evitar redimensionamento desnecessário. `batch=16` é o padrão Ultralytics e coube confortavelmente na CPU disponível no teste. `optimizer=auto` deixa a biblioteca escolher (decisão validada empiricamente no smoke test: AdamW, lr0=0.000714).

**Decisão 4 — `project=` com caminho absoluto para os resultados do treino.**
No teste inicial, passar `project="models/detection"` (relativo) fez o Ultralytics prefixar `runs/detect/` automaticamente, gerando `runs/detect/models/detection/<run>/` em vez de `models/detection/<run>/`. Corrigido usando um caminho absoluto (`Path(__file__).resolve().parents[1] / "models" / "detection"`) como `project=`, que o Ultralytics respeita como base final sem prefixo adicional.

**Decisão 5 — seed fixa (42) no treino.**
Consistente com a seed usada nos splits da Fase 1, passada como `seed=42` ao `model.train(...)` para reprodutibilidade parcial (determinismo total de treino de redes neurais não é garantido entre hardwares, mas a seed reduz variação).

## Risks / Trade-offs

- [Risco] 30 épocas em CPU pode não ser suficiente para um mAP alto → Mitigação: é aceitável para um **baseline** (a Fase 2 pede "primeiras métricas", não o resultado final); documentar isso explicitamente no relatório.
- [Risco] Caminho do projeto com acentos/espaços (`Visão Computacional e Reconhecimento de Padrões`) pode causar problemas de encoding em algumas bibliotecas → Mitigação: usar `pathlib.Path` (não strings manuais) e `project=` absoluto, como validado no smoke test; monitorar se novos scripts (Fase 3+) reproduzem o mesmo problema.
- [Risco] Rodar o treino em background nesta sessão pode ser interrompido → Mitigação: Ultralytics salva `last.pt` a cada época, permitindo retomar com `resume=True` se necessário.
