## MODIFIED Requirements

### Requirement: Estrutura de diretórios do projeto
O repositório SHALL conter os diretórios `data/raw`, `data/processed`, `data/splits`, `notebooks`, `models/detection`, `models/segmentation`, `reports/figures`, `video/input` e `video/output`, cada um versionado mesmo quando vazio (via `.gitkeep` ou README curto). O diretório `src/` SHALL conter scripts nomeados com prefixo numérico de execução (`step1_...`, `step2_...`, ...) refletindo a ordem em que devem ser rodados no pipeline completo do projeto, em vez de subpastas fixas por tarefa (não deve haver `src/detection/`, `src/segmentation/`, `src/evaluation/` ou `src/inference/` como diretórios fixos).

#### Scenario: Diretório de dados brutos existe e está vazio
- **WHEN** o grupo clona o repositório antes de qualquer dataset ser adicionado
- **THEN** `data/raw/` existe no repositório e está pronto para receber as imagens anotadas, sem exigir criação manual da pasta

#### Scenario: Diretórios de modelos separam detecção e segmentação
- **WHEN** o grupo salva um checkpoint treinado
- **THEN** existe um diretório dedicado (`models/detection/` ou `models/segmentation/`) para o tipo de modelo, evitando mistura de artefatos de detecção e segmentação

#### Scenario: Ordem de execução dos scripts fica explícita
- **WHEN** um integrante abre a pasta `src/`
- **THEN** os nomes dos arquivos (`step1_...`, `step2_...`, `step3_...`, ...) indicam a ordem em que devem ser executados, sem precisar navegar por subpastas de tarefa para descobrir a sequência

#### Scenario: Novo script de uma fase futura é adicionado
- **WHEN** a Fase 2 (ou posterior) precisa de um novo script (ex. treino do detector)
- **THEN** o script é adicionado em `src/` continuando a numeração (ex. `step5_train_detector.py`), não criando uma nova subpasta por tarefa

### Requirement: Configuração de ambiente versionada
O repositório SHALL conter um arquivo de dependências (`requirements.txt`) listando as bibliotecas sugeridas pelo enunciado (PyTorch/torchvision, Ultralytics YOLO, OpenCV, supervision) e um `.gitignore` que exclua dados grandes, checkpoints de modelo, ambientes virtuais e checkpoints de notebook do versionamento. O projeto SHALL usar um ambiente virtual Python (`.venv/`) local e não versionado, isolando as instalações de pacotes do Python global da máquina.

#### Scenario: Novo integrante configura o ambiente
- **WHEN** um novo integrante do grupo clona o repositório e executa a instalação de dependências
- **THEN** `requirements.txt` na raiz lista as bibliotecas necessárias para rodar o pipeline, sem precisar perguntar ao grupo quais pacotes instalar

#### Scenario: Dataset grande não é versionado por acidente
- **WHEN** um integrante adiciona imagens ou pesos de modelo em `data/` ou `models/` e executa `git add`
- **THEN** o `.gitignore` impede que esses arquivos grandes sejam adicionados ao controle de versão

#### Scenario: Instalação de pacotes não afeta o Python global
- **WHEN** um integrante roda `pip install -r requirements.txt` seguindo as instruções do README
- **THEN** os pacotes são instalados dentro de `.venv/` (ambiente virtual ativado), não no interpretador Python global do sistema
