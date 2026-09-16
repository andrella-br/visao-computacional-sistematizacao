## MODIFIED Requirements

### Requirement: Notebook Colab executável
O repositório SHALL conter, em `notebooks/`, um conjunto de notebooks autocontidos organizados por fase — `visao_computacional_01_data.ipynb`, `visao_computacional_02_detection.ipynb`, `visao_computacional_03_segmentation.ipynb`, `visao_computacional_04_evaluation.ipynb`, `visao_computacional_05_inference_video.ipynb`, `visao_computacional_06_report.ipynb` — cada um reproduzindo a lógica dos scripts `src/step01`-`step14` correspondentes **diretamente nas células de código** (não por chamada a scripts externos via `%run` ou `subprocess`), executáveis em Google Colab. O repositório SHALL também conter um notebook consolidado (`visao_computacional_pipeline_completo.ipynb`) com as mesmas células dos 6 notebooks por fase, em sequência, com uma única célula de setup.

#### Scenario: Notebook reproduz o pipeline
- **WHEN** alguém abre um dos notebooks no Colab e executa as células em ordem
- **THEN** a etapa correspondente (preparação de dados, treino, avaliação ou inferência) roda usando código definido nas próprias células do notebook, sem precisar clonar ou importar os scripts de `src/`

#### Scenario: Notebooks compartilham armazenamento persistente
- **WHEN** um notebook (ex. `visao_computacional_02_detection.ipynb`) precisa dos dados gerados por outro (ex. `visao_computacional_01_data.ipynb`)
- **THEN** ambos leem/escrevem na mesma pasta persistente (Google Drive montado), permitindo rodá-los em sessões Colab separadas na ordem correta

#### Scenario: Saídas visíveis ou re-executáveis
- **WHEN** alguém executa as células de um notebook
- **THEN** vê as saídas (prints, gráficos, tabelas) diretamente no notebook, sem exigir edição manual do código além de configurar credenciais/paths quando aplicável

#### Scenario: Pipeline completo roda em um único notebook
- **WHEN** alguém abre `visao_computacional_pipeline_completo.ipynb` no Colab e executa as células em ordem, numa única sessão
- **THEN** todas as fases (dados, detecção, segmentação, avaliação, inferência em vídeo, relatório de conformidade) rodam sequencialmente sem precisar abrir os 6 notebooks separados
