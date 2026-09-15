## Why

Depois de implementar a Fase 1, o integrante do grupo pediu dois ajustes de convenção antes de iniciar a Fase 2: (1) um ambiente virtual dedicado ao projeto, para que as instalações de pacotes fiquem isoladas (não no Python global), e (2) que os scripts em `src/` sejam nomeados pela ordem de execução do pipeline (`step1_`, `step2_`, ...) em vez de organizados em subpastas por tarefa (`src/detection/`, `src/segmentation/`, etc.), para deixar explícito o que rodar antes do quê. A spec `project-scaffolding` (já arquivada da Fase de setup) ainda descreve a estrutura antiga de subpastas — precisa ser atualizada para refletir a convenção real do projeto.

## What Changes

- Criar `.venv/` (ambiente virtual Python local ao projeto) e instalar `requirements.txt` dentro dele. Já estava no `.gitignore`, então não precisa de mudança ali.
- Remover as subpastas `src/data`, `src/detection`, `src/segmentation`, `src/evaluation`, `src/inference` e mover os 4 scripts existentes para `src/` com prefixo numérico de execução: `step1_prepare_construction_site_safety.py`, `step2_prepare_coco_person_subset.py`, `step3_make_splits.py`, `step4_eda_construction_site_safety.py`.
- Corrigir os caminhos internos dos scripts (cálculo da raiz do projeto) para o novo local.
- Atualizar `README.md` e `CLAUDE.md` para descrever a nova estrutura de `src/` (flat, numerada) e o passo de criação do ambiente virtual.
- Atualizar a spec `project-scaffolding` (**MODIFIED**, pois o requisito de estrutura de diretórios muda de comportamento esperado): `src/` não tem mais subpastas fixas por tarefa; scripts futuros continuam a numeração (`step5_`, `step6_`, ...).

**BREAKING** (apenas para a convenção interna do projeto, não para dados já publicados): qualquer referência futura a `src/detection/...` ou `src/segmentation/...` como caminho fixo deixa de ser válida.

## Capabilities

### Modified Capabilities
- `project-scaffolding`: o requisito "Estrutura de diretórios do projeto" muda — `src/` deixa de ter subpastas fixas por tarefa e passa a conter scripts numerados por ordem de execução (`stepN_*.py`). Novo requisito: ambiente virtual local ao projeto (`.venv/`).

## Impact

- Scripts movidos: `src/data/*.py` → `src/step1_..._.py`...`src/step4_..._.py` (caminhos internos ajustados).
- `README.md`, `CLAUDE.md` atualizados.
- Nenhum dado baixado (`data/raw/`, `data/splits/`) precisa ser refeito — a reorganização não altera os dados já preparados na Fase 1, só a localização/nome dos scripts que os geraram.
