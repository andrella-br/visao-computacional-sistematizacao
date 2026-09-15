## Purpose

Mantém um documento único e rastreável com as 5 fases do projeto (definidas pelo enunciado da disciplina), seus objetivos, entregáveis e critérios de avaliação associados, para orientar a criação das próximas mudanças OpenSpec, uma por fase.

## ADDED Requirements

### Requirement: Documento de roadmap com as 5 fases
O repositório SHALL conter `docs/roadmap.md` listando as 5 fases do projeto (Definição e dados; Baseline de detecção; Segmentação; Avaliação e vídeo; Entrega e apresentação), cada uma com objetivo, principais atividades e entregáveis, conforme descrito em `Sistematizacao_Instruções.md`.

#### Scenario: Grupo consulta o que falta entregar na fase atual
- **WHEN** um integrante do grupo abre `docs/roadmap.md` durante a Fase 2
- **THEN** o documento lista as atividades e entregáveis esperados da Fase 2 (baseline de detecção), incluindo hiperparâmetros a documentar

#### Scenario: Fase referencia o critério do barema correspondente
- **WHEN** o grupo revisa uma fase no roadmap
- **THEN** o documento indica a qual critério do barema de avaliação (peso %) aquela fase contribui, permitindo priorizar esforço

### Requirement: Roadmap como base para futuras mudanças OpenSpec
O `docs/roadmap.md` SHALL declarar explicitamente que cada fase subsequente (2 a 5) deve ser proposta como uma mudança OpenSpec separada (`openspec new change`) somente após a Fase 1 (escolha de cenário e dataset) estar concluída.

#### Scenario: Grupo decide iniciar a Fase 2
- **WHEN** a Fase 1 é concluída e o grupo decide iniciar o baseline de detecção
- **THEN** o roadmap orienta a criar uma nova mudança OpenSpec dedicada à Fase 2, em vez de expandir a mudança de estrutura inicial
