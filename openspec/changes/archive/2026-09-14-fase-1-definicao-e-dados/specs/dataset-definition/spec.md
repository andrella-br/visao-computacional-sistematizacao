## Purpose

Define e documenta o cenário do projeto e as fontes de dados (detecção e segmentação) com origem citável, licença compatível e splits reprodutíveis, servindo de base para todas as fases seguintes.

## ADDED Requirements

### Requirement: Cenário do projeto documentado
O repositório SHALL declarar o cenário escolhido (Segurança do Trabalho — EPIs e segmentação de pessoas) no `README.md` e em `docs/roadmap.md`, substituindo qualquer marcação de "a definir".

#### Scenario: Avaliador confere o cenário do projeto
- **WHEN** o professor abre o `README.md`
- **THEN** o cenário "Segurança do Trabalho" está descrito com as classes-alvo (EPIs: capacete, colete; segmentação: pessoa)

### Requirement: Fontes de dataset citadas com licença
O repositório SHALL documentar, para cada dataset usado, a fonte, o link/identificador, a licença, o número total de imagens disponíveis na fonte e o tamanho do subconjunto efetivamente usado: o dataset de detecção de EPIs (Construction Site Safety, CC BY 4.0, 2.801 imagens disponíveis, 10 classes) e o subconjunto do COCO usado para segmentação de pessoas (categoria `person`).

#### Scenario: Integrante futuro reproduz a coleta de dados
- **WHEN** alguém lê a documentação de dados do projeto
- **THEN** encontra o nome, a fonte, a licença e o link de cada dataset usado, sem precisar perguntar de onde vieram os dados

### Requirement: Subconjunto mínimo com amostragem estratificada
O projeto SHALL usar um subconjunto de no mínimo 300 imagens de cada fonte (detecção e segmentação), em vez do dataset completo, selecionado por amostragem estratificada que preserve a presença de todas as classes-alvo no subconjunto.

#### Scenario: Classe rara continua representada após a amostragem
- **WHEN** o subconjunto de ~300-400 imagens é selecionado do Construction Site Safety
- **THEN** todas as 10 classes (incluindo as mais raras, como `Safety Cone` ou `NO-Mask`) aparecem em pelo menos algumas imagens do subconjunto, não apenas as classes mais frequentes

#### Scenario: Volume mínimo é respeitado
- **WHEN** o subconjunto final é contado
- **THEN** cada fonte (detecção e segmentação) tem pelo menos 300 imagens anotadas, atendendo ao requisito mínimo do enunciado

### Requirement: Splits reprodutíveis com seed fixa
O projeto SHALL definir splits de treino/validação/teste com uma seed fixa e documentada, cobrindo tanto o dataset de detecção quanto o subconjunto de segmentação.

#### Scenario: Splits são reproduzidos por outro integrante
- **WHEN** alguém roda o script/notebook de split com a mesma seed documentada
- **THEN** obtém exatamente as mesmas imagens em treino, validação e teste
