## Why

A convenção `stepN_*.py` adotada na mudança anterior (`reorganizar-scripts-e-ambiente-virtual`) indica a ordem de execução, mas não deixa claro a qual fase do roadmap (dados, detecção, segmentação, avaliação, inferência) cada script pertence — informação que antes vinha do nome da subpasta (`src/detection/`, `src/segmentation/` etc.) e que o integrante quer preservar, mesmo com a estrutura flat.

## What Changes

- Renomear os 4 scripts existentes de `stepN_*.py` para `stepNN_<fase>_*.py` (dois dígitos + tag de fase):
  - `step1_prepare_construction_site_safety.py` → `step01_data_prepare_construction_site_safety.py`
  - `step2_prepare_coco_person_subset.py` → `step02_data_prepare_coco_person_subset.py`
  - `step3_make_splits.py` → `step03_data_make_splits.py`
  - `step4_eda_construction_site_safety.py` → `step04_data_eda_construction_site_safety.py`
- Corrigir as docstrings de uso (`python src/stepNN_...`) dentro de cada script.
- Atualizar `README.md` e `CLAUDE.md` com a convenção `stepNN_<fase>_<descrição>.py`, onde `<fase>` é uma de `data`, `detection`, `segmentation`, `evaluation`, `inference`.
- Atualizar a spec `project-scaffolding` (**MODIFIED**) para formalizar o padrão de nomenclatura com tag de fase.

## Capabilities

### Modified Capabilities
- `project-scaffolding`: o requisito de estrutura de `src/` passa a exigir o padrão `stepNN_<fase>_<descrição>.py` (dois dígitos + tag de fase), não apenas `stepN_*.py`.

## Impact

- Apenas renomeação de arquivos já existentes (Fase 1) e atualização de documentação/spec — nenhum dado ou split é refeito.
