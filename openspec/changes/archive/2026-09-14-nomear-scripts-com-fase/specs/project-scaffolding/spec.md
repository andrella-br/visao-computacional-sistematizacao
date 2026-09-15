## MODIFIED Requirements

### Requirement: Estrutura de diretórios do projeto
O repositório SHALL conter os diretórios `data/raw`, `data/processed`, `data/splits`, `notebooks`, `models/detection`, `models/segmentation`, `reports/figures`, `video/input` e `video/output`, cada um versionado mesmo quando vazio (via `.gitkeep` ou README curto). O diretório `src/` SHALL conter scripts nomeados no padrão `stepNN_<fase>_<descrição>.py`, onde `NN` é o número de ordem global de execução (dois dígitos) e `<fase>` é uma das etapas do roadmap (`data`, `detection`, `segmentation`, `evaluation`, `inference`), em vez de subpastas fixas por tarefa (não deve haver `src/detection/`, `src/segmentation/`, `src/evaluation/` ou `src/inference/` como diretórios fixos).

#### Scenario: Diretório de dados brutos existe e está vazio
- **WHEN** o grupo clona o repositório antes de qualquer dataset ser adicionado
- **THEN** `data/raw/` existe no repositório e está pronto para receber as imagens anotadas, sem exigir criação manual da pasta

#### Scenario: Diretórios de modelos separam detecção e segmentação
- **WHEN** o grupo salva um checkpoint treinado
- **THEN** existe um diretório dedicado (`models/detection/` ou `models/segmentation/`) para o tipo de modelo, evitando mistura de artefatos de detecção e segmentação

#### Scenario: Ordem de execução dos scripts fica explícita
- **WHEN** um integrante abre a pasta `src/`
- **THEN** o nome de cada arquivo (`step01_data_...`, `step05_detection_...`, ...) indica tanto a ordem de execução (`NN`) quanto a fase do roadmap a que o script pertence (`<fase>`), sem precisar abrir o arquivo ou navegar por subpastas para descobrir a sequência ou o contexto

#### Scenario: Novo script de uma fase futura é adicionado
- **WHEN** a Fase 2 precisa de um novo script (ex. treino do detector)
- **THEN** o script é adicionado em `src/` continuando a numeração global e usando a tag da fase correspondente (ex. `step05_detection_train_yolo.py`), não criando uma nova subpasta por tarefa
