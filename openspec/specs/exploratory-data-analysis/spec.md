# exploratory-data-analysis Specification

## Purpose

Garante que o grupo entenda os dados antes de treinar qualquer modelo, produzindo uma análise exploratória documentada e a proposta de 1 página exigida na Fase 1 do enunciado.

## Requirements

### Requirement: Análise exploratória documentada
O projeto SHALL produzir uma análise exploratória (EDA) cobrindo, para o dataset de detecção de EPIs: quantidade de imagens por classe, resolução das imagens, condições de iluminação observadas e desbalanceamento entre classes (ex.: presença vs. ausência de EPI).

#### Scenario: Grupo identifica desbalanceamento antes de treinar
- **WHEN** a EDA é executada sobre o dataset de detecção
- **THEN** o relatório resultante mostra a contagem de instâncias por classe (`Hardhat`, `NO-Hardhat`, `Safety Vest`, `NO-Safety Vest` etc.), permitindo identificar classes sub-representadas antes da Fase 2

#### Scenario: EDA fica registrada para o relatório técnico
- **WHEN** alguém prepara o relatório técnico da Fase 5
- **THEN** encontra os gráficos/tabelas da EDA salvos em `reports/figures/` ou referenciados em `docs/`, sem precisar refazer a análise

### Requirement: Proposta de 1 página da Fase 1
O repositório SHALL conter uma proposta de 1 página (problema, classes-alvo, fonte dos dados, ferramenta de anotação/uso) conforme exigido pelo enunciado da disciplina para a Fase 1.

#### Scenario: Proposta pronta para submissão
- **WHEN** o prazo da Fase 1 chega
- **THEN** existe um documento de 1 página no repositório (ex. `docs/proposta-fase1.md`) descrevendo o problema, as classes-alvo, a fonte dos dados e a ferramenta/estratégia de anotação usada
