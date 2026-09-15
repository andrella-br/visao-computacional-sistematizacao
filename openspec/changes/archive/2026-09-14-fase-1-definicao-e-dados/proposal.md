## Why

O grupo (1 integrante) definiu o cenário e as fontes de dados para o projeto, mas essa decisão ainda não está formalizada no repositório. A Fase 1 do roadmap (`docs/roadmap.md`) exige entregar uma proposta de 1 página e uma análise exploratória (EDA) antes de qualquer treino. Sem isso documentado, as Fases 2-5 não têm uma base rastreável de classes-alvo, splits e fonte dos dados.

## What Changes

- Registrar formalmente o cenário escolhido: **Segurança do Trabalho** — detecção de EPIs (capacete, colete) e segmentação de pessoas em canteiros de obra.
- Registrar as fontes de dataset:
  - **Detecção (EPIs)**: *Construction Site Safety* (Roboflow Universe / espelhado no Kaggle por `snehilsanyal`), licença CC BY 4.0, 2.801 imagens disponíveis no total, 10 classes (`Hardhat`, `NO-Hardhat`, `Safety Vest`, `NO-Safety Vest`, `Mask`, `NO-Mask`, `Person`, `Safety Cone`, `machinery`, `vehicle`). O grupo usa um **subconjunto de ~300-400 imagens**, amostrado de forma estratificada para preservar a presença de todas as 10 classes (em vez de baixar o dataset completo, evitando peso desnecessário no treino).
  - **Segmentação (pessoas)**: subconjunto do **COCO** (categoria `person`, que já possui máscaras de instância prontas) de volume equivalente (~300 imagens), citado conforme permitido pelo enunciado.
- Baixar apenas os subconjuntos selecionados (não os datasets completos) para `data/raw/` e documentar a origem e a estratégia de amostragem (README de dados).
- Definir splits fixos de treino/validação/teste com seed, reaproveitando os splits oficiais quando fizerem sentido ou redefinindo-os para garantir reprodutibilidade.
- Realizar a análise exploratória (EDA): contagem de imagens por classe, resolução, condições de iluminação, desbalanceamento de classes (esperado: EPI presente vs. ausente).
- Escrever a proposta de 1 página exigida pelo enunciado (problema, classes-alvo, fonte dos dados, ferramenta de anotação/uso).

Nenhum treino de modelo, arquitetura de detector/segmentador ou hiperparâmetro é decidido nesta mudança — isso é escopo da Fase 2 (detecção) e Fase 3 (segmentação), cada uma como uma mudança OpenSpec própria.

## Capabilities

### New Capabilities
- `dataset-definition`: escolha do cenário, das fontes de dataset (detecção e segmentação), critérios de aquisição, splits reprodutíveis e documentação da origem dos dados.
- `exploratory-data-analysis`: análise exploratória dos dados (contagem por classe, resolução, iluminação, desbalanceamento) e a proposta de 1 página exigida na Fase 1.

### Modified Capabilities
(nenhuma)

## Impact

- Novos arquivos em `data/raw/` (dados baixados, fora do controle de versão) e documentação em `docs/` ou `reports/` sobre a origem dos dados e a EDA.
- Define classes-alvo e fontes que orientarão diretamente o dataset preparation da Fase 2 (formato YOLO/COCO, splits) e da Fase 3 (segmentação de pessoas).
- `README.md` deixa de listar o cenário como "a definir".
