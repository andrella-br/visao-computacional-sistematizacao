## MODIFIED Requirements

### Requirement: Notebook Colab executável
O repositório SHALL conter, em `notebooks/`, um conjunto de notebooks autocontidos organizados por fase — `01_data.ipynb`, `02_detection.ipynb`, `03_segmentation.ipynb`, `04_evaluation.ipynb`, `05_inference_video.ipynb`, `06_report.ipynb` — cada um reproduzindo a lógica dos scripts `src/step01`-`step14` correspondentes **diretamente nas células de código** (não por chamada a scripts externos via `%run` ou `subprocess`), executáveis em Google Colab.

#### Scenario: Notebook reproduz o pipeline
- **WHEN** alguém abre um dos notebooks no Colab e executa as células em ordem
- **THEN** a etapa correspondente (preparação de dados, treino, avaliação ou inferência) roda usando código definido nas próprias células do notebook, sem precisar clonar ou importar os scripts de `src/`

#### Scenario: Notebooks compartilham armazenamento persistente
- **WHEN** um notebook (ex. `02_detection.ipynb`) precisa dos dados gerados por outro (ex. `01_data.ipynb`)
- **THEN** ambos leem/escrevem na mesma pasta persistente (Google Drive montado), permitindo rodá-los em sessões Colab separadas na ordem correta

#### Scenario: Saídas visíveis ou re-executáveis
- **WHEN** alguém executa as células de um notebook
- **THEN** vê as saídas (prints, gráficos, tabelas) diretamente no notebook, sem exigir edição manual do código além de configurar credenciais/paths quando aplicável
