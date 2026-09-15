# repository-packaging Specification

## Purpose

Empacota o projeto como um repositório Git local e um notebook Colab executável, atendendo aos Itens 2 e 3 da entrega (repositório GitHub e notebook executável).

## Requirements

### Requirement: Repositório Git local inicializado
O projeto SHALL ser um repositório Git local (`git init`), com um primeiro commit contendo o estado atual do projeto, respeitando o `.gitignore` já existente. Nenhum push a um repositório remoto SHALL ocorrer sem confirmação explícita do integrante.

#### Scenario: Histórico local existe e respeita o .gitignore
- **WHEN** alguém roda `git log` no repositório após esta mudança
- **THEN** encontra pelo menos um commit, e `git status` não lista arquivos grandes/gitignorados (dados brutos, pesos de modelo, vídeos) como não rastreados

### Requirement: Notebook Colab executável
O repositório SHALL conter um notebook (`notebooks/pipeline_completo.ipynb`) com células cobrindo preparação de dados, treino de detecção, treino de segmentação, avaliação no teste e inferência em vídeo — reproduzindo o pipeline dos scripts `src/step01`-`step14`, executável em Google Colab.

#### Scenario: Notebook reproduz o pipeline
- **WHEN** alguém abre o notebook no Colab e executa as células em ordem
- **THEN** o pipeline completo (dados → treino → avaliação → inferência) roda, com saídas visíveis ou re-executáveis, sem exigir edição manual do código além de configurar credenciais/paths quando aplicável
