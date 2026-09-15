## Why

O notebook consolidado (`notebooks/pipeline_completo.ipynb`) da Fase 5 usava `%run src/stepNN_*.py` para cada etapa — funcional, mas depende de clonar/ter o repositório inteiro no Colab, e mistura "notebook" com "script chamado de fora". O integrante pediu (1) código inline nas células (sem depender de `src/`) e (2) separação em vários notebooks por fase (data, detection, segmentation, evaluation, inference_video, report), em vez de um único consolidado.

## What Changes

- Remover `notebooks/pipeline_completo.ipynb`.
- Criar 6 notebooks autocontidos, cada um com o código das etapas correspondentes reescrito diretamente nas células (não `%run`):
  - `01_data.ipynb` (steps 01-04)
  - `02_detection.ipynb` (steps 05-06)
  - `03_segmentation.ipynb` (steps 07-09)
  - `04_evaluation.ipynb` (steps 11-12)
  - `05_inference_video.ipynb` (steps 10, 13)
  - `06_report.ipynb` (step 14)
- Todos compartilham a mesma convenção de armazenamento persistente (Google Drive montado em `PROJECT_DIR`), para que rodar um notebook alimente o próximo.
- Corrigir dois bugs de portabilidade encontrados nos scripts originais durante a extração: `step01` e `step02` dependiam de downloads manuais feitos fora do script (paths locais hardcoded) — ambos agora baixam seus dados sozinhos (Kaggle CLI e zip de anotações do COCO, respectivamente).
- Corrigir uma colisão de nome de arquivo entre `step01` e `step05` (os dois escreviam `data.yaml` no mesmo caminho, um sobrescrevendo o outro) — `step01` não escreve mais esse arquivo.

## Capabilities

### Modified Capabilities
- `repository-packaging`: o requisito de notebook Colab passa a exigir múltiplos notebooks autocontidos (código inline, não dependente de `src/`), um por fase, em vez de um único notebook consolidado que chama scripts.

## Impact

- `notebooks/pipeline_completo.ipynb` removido; 6 novos notebooks criados.
- `src/step01_data_prepare_construction_site_safety.py` e `src/step02_data_prepare_coco_person_subset.py` corrigidos (download automático, sem paths locais hardcoded) — os scripts continuam existindo e funcionando para quem preferir rodar localmente.
- `src/step01` não escreve mais `data.yaml` (responsabilidade exclusiva do `step05`), corrigindo a colisão encontrada.
- `README.md` atualizado com a lista dos 6 notebooks e instruções de uso no Colab.
