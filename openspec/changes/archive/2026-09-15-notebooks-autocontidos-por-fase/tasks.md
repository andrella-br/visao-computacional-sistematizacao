## 1. Corrigir portabilidade dos scripts de dados

- [x] 1.1 Corrigir `src/step01_data_prepare_construction_site_safety.py` para baixar o dataset do Kaggle programaticamente (sem path local hardcoded) e verificar que reproduz os mesmos 350 imagens/classe
- [x] 1.2 Corrigir `src/step02_data_prepare_coco_person_subset.py` para baixar/extrair as anotações do COCO programaticamente e verificar que reproduz os mesmos 300 imagens/1280 instâncias
- [x] 1.3 Remover a escrita de `data.yaml` do `step01` (colisão com o `step05`) e restaurar o `data.yaml` correto rodando `step05`

## 2. Criar os 6 notebooks autocontidos

- [x] 2.1 Remover `notebooks/pipeline_completo.ipynb`
- [x] 2.2 Criar `01_data.ipynb` (steps 01-04) com código inline
- [x] 2.3 Criar `02_detection.ipynb` (steps 05-06) com código inline
- [x] 2.4 Criar `03_segmentation.ipynb` (steps 07-09) com código inline
- [x] 2.5 Criar `04_evaluation.ipynb` (steps 11-12) com código inline
- [x] 2.6 Criar `05_inference_video.ipynb` (steps 10, 13) com código inline
- [x] 2.7 Criar `06_report.ipynb` (step 14) com código inline

## 3. Validação

- [x] 3.1 Validar os 6 notebooks com `nbformat` (JSON válido, sem warnings) e checar sintaxe Python de cada célula de código
- [x] 3.2 Rodar de fato o código de uma célula extraída (avaliação no teste) contra os dados reais do projeto e confirmar que reproduz exatamente as mesmas métricas dos relatórios já publicados
- [x] 3.3 Atualizar `README.md` com a lista dos 6 notebooks e instruções de uso no Colab

## 4. Validação final

- [x] 4.1 Rodar `openspec validate notebooks-autocontidos-por-fase --strict` e confirmar que a mudança passa sem erros
