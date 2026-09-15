## Context

O projeto já tem todo o conteúdo técnico disperso em `docs/` e `reports/` (proposta, EDA, métricas de detecção/segmentação, avaliação de teste, relatório de conformidade). Falta consolidar isso no formato de entrega exigido (README/relatório técnico, repositório Git, notebook Colab). Ver `proposal.md` para a motivação.

## Goals / Non-Goals

**Goals:**
- Relatório técnico legível como documento único, sem forçar o leitor a abrir 6+ arquivos separados.
- `git init` seguro: cria histórico local sem nenhum risco de publicar nada sem consentimento.
- Notebook que reproduz o pipeline real (mesmo código dos scripts `src/`), não uma reescrita paralela que possa divergir.

**Non-Goals:**
- Não é objetivo desta mudança fazer push para um GitHub remoto — isso depende de decisão do integrante (conta, nome do repositório, público/privado).
- Não é objetivo produzir o vídeo-pitch (exige gravação humana).
- Não é objetivo reescrever os scripts `src/step*.py` — o notebook os reaproveita/adapta, não os substitui.

## Decisions

**Decisão 1 — Relatório técnico como arquivo separado, README enxuto.**
`docs/relatorio-tecnico.md` concentra o conteúdo completo (6-10 páginas); `README.md` continua sendo a porta de entrada rápida do repositório (estrutura de pastas, como reproduzir), com um link para o relatório. Alternativa considerada: colocar tudo dentro do próprio `README.md`; rejeitada porque o README já cumpre bem seu papel de navegação rápida do repositório, e misturar os dois propósitos (overview rápido vs. relatório de 6-10 páginas) prejudicaria os dois.

**Decisão 2 — `git init` + 1 commit, sem push.**
Escopo desta mudança termina no commit local. Push depende de o integrante ter (ou criar) um repositório remoto no GitHub e decidir se será público ou privado — decisão que não deve ser tomada automaticamente.

**Decisão 3 — Notebook único consolidado, célula-a-célula na ordem `stepNN`.**
Um notebook único (`notebooks/pipeline_completo.ipynb`) com uma célula markdown + uma célula de código por script `stepNN_*.py` (01 a 14), na ordem de execução, em vez de notebooks separados por fase. Isso casa com a convenção de nomenclatura já adotada em `src/` e evita fragmentar a entrega em vários arquivos. Cada célula de código reaproveita a lógica dos scripts (import direto quando possível, ou código adaptado com os mesmos parâmetros/seeds), com uma célula inicial de setup (clonar repo ou montar Google Drive, instalar `requirements.txt`).

**Decisão 4 — Treino no notebook usa os mesmos hiperparâmetros documentados, sem alterá-los.**
O notebook não "melhora" hiperparâmetros para aproveitar GPU do Colab — reproduz exatamente o que foi documentado (30 épocas, batch=16, imgsz=640, seed=42), para que os resultados sejam comparáveis aos já documentados. Uma nota no notebook explica que, com GPU, o mesmo treino roda em muito menos tempo, e que aumentar épocas é uma extensão natural fora do escopo desta entrega.

## Risks / Trade-offs

- [Risco] Notebook Colab depende de baixar os datasets (Kaggle + COCO) toda vez que reinicia o ambiente → Mitigação: reaproveitar os scripts `step01`/`step02` (já testados) nas primeiras células; documentar que o integrante precisa de um token Kaggle próprio no Colab (`kaggle.json` ou secret).
- [Risco] `git init` num diretório com histórico de trabalho já extenso pode incluir arquivos indesejados no primeiro commit → Mitigação: revisar `git status` antes de commitar, confiando no `.gitignore` já validado nas fases anteriores.
