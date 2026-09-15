## Context

O cenário escolhido (Segurança do Trabalho) usa **duas fontes de dados diferentes** para as duas tarefas do projeto: um dataset de detecção de EPIs (Construction Site Safety) e um subconjunto do COCO para segmentação de pessoas. Ver `proposal.md` para a motivação da escolha. Esta decisão de combinar duas fontes precisa de um plano técnico para não gerar inconsistência entre as fases 2 e 3.

## Goals / Non-Goals

**Goals:**
- Definir como as duas fontes de dados coexistem em `data/` sem conflito de formato ou de classes.
- Garantir que os splits de treino/validação/teste sejam reprodutíveis (seed fixa) em ambas as fontes.
- Deixar claro, desde já, que a comparação caixas × máscaras da Fase 3 vai comparar tarefas em imagens de **domínios diferentes** (canteiro de obra vs. imagens gerais do COCO com pessoas), não a mesma imagem com dupla anotação.

**Non-Goals:**
- Não é objetivo desta mudança anotar máscaras de pessoas nas imagens do Construction Site Safety (ficaria caro e não é necessário: o COCO já fornece máscaras de `person` em volume suficiente).
- Não é objetivo unificar as duas fontes em um único dataset multi-tarefa neste momento — cada fonte alimenta uma tarefa (detecção ou segmentação) de forma independente.

## Decisions

**Decisão 0 — Subconjunto de ~300-400 imagens, não o dataset completo.**
O Construction Site Safety tem 2.801 imagens disponíveis, mas o enunciado exige apenas um mínimo de 300 imagens anotadas. Baixar e treinar com o dataset inteiro pesaria desnecessariamente o treino (tempo de download, espaço em disco, tempo por época no Colab) sem benefício para os objetivos do projeto. Decisão: selecionar um subconjunto de ~300-400 imagens por **amostragem estratificada por classe**, garantindo que classes raras (ex. `Safety Cone`, `NO-Mask`) continuem representadas — uma amostra puramente aleatória de 300 sobre 2.801 arriscaria zerar classes pouco frequentes. O mesmo raciocínio de volume (~300 imagens) se aplica ao subconjunto do COCO. Alternativa considerada: usar o dataset completo para ter mais dados de treino; rejeitada por custo/benefício desfavorável para um grupo de 1 pessoa rodando em Colab.

**Decisão 1 — Duas fontes independentes, não uma fusão.**
Detecção de EPI usa exclusivamente o Construction Site Safety; segmentação de pessoa usa exclusivamente o subconjunto do COCO. Alternativa considerada: anotar máscaras de pessoa nas imagens do canteiro de obra (via Roboflow Smart Polygon) para ter tudo na mesma imagem. Rejeitada nesta fase por custo de anotação manual incompatível com um grupo de 1 pessoa; pode ser revisitada como extensão na Fase 3 se o tempo permitir.

**Decisão 2 — Estrutura de pastas por fonte.**
`data/raw/` terá subpastas por fonte (`data/raw/construction-site-safety/` e `data/raw/coco-person/`) em vez de misturar arquivos, para manter rastreável de onde cada imagem veio e facilitar a citação de licença por fonte.

**Decisão 3 — Seed única documentada.**
Uma única seed (a ser fixada em `docs/roadmap.md` ou em um script de preparação futuro da Fase 2) é usada para os splits de ambas as fontes, para que "reproduzir os splits" seja um processo único e documentado, não dois processos distintos.

## Risks / Trade-offs

- [Risco] Comparar EPI-detection (canteiro de obra) com person-segmentation (COCO genérico) pode parecer artificial na análise qualitativa da Fase 3 → Mitigação: documentar explicitamente no relatório técnico que a comparação é conceitual (o que caixas mostram vs. o que máscaras mostram), não pixel-a-pixel na mesma imagem.
- [Risco] Licenças diferentes (CC BY 4.0 vs. licença do COCO) exigem atribuição separada → Mitigação: documentar cada fonte e sua licença separadamente no README/relatório, conforme já previsto no requisito "Fontes de dataset citadas com licença".
- [Risco] Volume do subconjunto do COCO pode ser desnecessariamente grande se baixado por inteiro → Mitigação: baixar apenas as imagens da categoria `person` suficientes para o volume mínimo exigido (≥300), não o COCO completo.
