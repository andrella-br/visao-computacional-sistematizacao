## Purpose

Fornece a estrutura de diretórios e arquivos de configuração versionados que todas as fases do projeto (dados, treinamento, avaliação, vídeo, relatório) usarão como convenção de organização.

## ADDED Requirements

### Requirement: Estrutura de diretórios do projeto
O repositório SHALL conter os diretórios `data/raw`, `data/processed`, `data/splits`, `notebooks`, `src/data`, `src/detection`, `src/segmentation`, `src/evaluation`, `src/inference`, `models/detection`, `models/segmentation`, `reports/figures`, `video/input` e `video/output`, cada um versionado mesmo quando vazio (via `.gitkeep` ou README curto).

#### Scenario: Diretório de dados brutos existe e está vazio
- **WHEN** o grupo clona o repositório antes de qualquer dataset ser adicionado
- **THEN** `data/raw/` existe no repositório e está pronto para receber as imagens anotadas, sem exigir criação manual da pasta

#### Scenario: Diretórios de modelos separam detecção e segmentação
- **WHEN** o grupo salva um checkpoint treinado
- **THEN** existe um diretório dedicado (`models/detection/` ou `models/segmentation/`) para o tipo de modelo, evitando mistura de artefatos de detecção e segmentação

### Requirement: Configuração de ambiente versionada
O repositório SHALL conter um arquivo de dependências (`requirements.txt`) listando as bibliotecas sugeridas pelo enunciado (PyTorch/torchvision, Ultralytics YOLO, OpenCV, supervision) e um `.gitignore` que exclua dados grandes, checkpoints de modelo, ambientes virtuais e checkpoints de notebook do versionamento.

#### Scenario: Novo integrante configura o ambiente
- **WHEN** um novo integrante do grupo clona o repositório e executa a instalação de dependências
- **THEN** `requirements.txt` na raiz lista as bibliotecas necessárias para rodar o pipeline, sem precisar perguntar ao grupo quais pacotes instalar

#### Scenario: Dataset grande não é versionado por acidente
- **WHEN** um integrante adiciona imagens ou pesos de modelo em `data/` ou `models/` e executa `git add`
- **THEN** o `.gitignore` impede que esses arquivos grandes sejam adicionados ao controle de versão

### Requirement: README inicial do projeto
O repositório SHALL conter um `README.md` na raiz descrevendo o objetivo do projeto, o cenário escolhido (ou "a definir"), a estrutura de pastas e como reproduzir o pipeline.

#### Scenario: Avaliador abre o repositório pela primeira vez
- **WHEN** o professor ou avaliador abre o repositório do GitHub
- **THEN** o `README.md` explica o que o projeto faz e como navegar pela estrutura de pastas, mesmo antes do dataset e dos modelos existirem
