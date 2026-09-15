## Why

O repositório contém apenas o enunciado da atividade (`Sistematizacao_Instruções.md`) e uma pasta `image/` vazia. Antes que o grupo possa escolher o cenário, coletar dados ou treinar qualquer modelo, é preciso montar o esqueleto do projeto (pastas de dados, notebooks, código-fonte, modelos, relatórios e vídeo) e formalizar as 5 fases do roadmap como itens de trabalho rastreáveis, para que o grupo saiba onde cada artefato deve ser salvo e o que entregar em cada fase.

## What Changes

- Criar a estrutura de diretórios do projeto (`data/{raw,processed,splits}`, `notebooks/`, `src/{data,detection,segmentation,evaluation,inference}`, `models/{detection,segmentation}`, `reports/figures`, `video/{input,output}`, `docs/`), cada uma com um `.gitkeep` ou README curto para ser versionada vazia.
- Criar um `README.md` na raiz do repositório com visão geral do projeto, estrutura de pastas e instruções de reprodução (a serem completadas conforme o projeto avança).
- Criar um `requirements.txt` (ou `environment.yml`) inicial com as dependências sugeridas pelo enunciado (PyTorch/torchvision, Ultralytics YOLO, OpenCV, supervision).
- Criar um `.gitignore` adequado para projetos de visão computacional em Python (dados grandes, checkpoints de modelo, ambientes virtuais, notebooks checkpoints).
- Documentar as 5 fases do roadmap (Definição e dados; Baseline de detecção; Segmentação; Avaliação e vídeo; Entrega e apresentação) como uma lista de fases/etapas rastreável em `docs/roadmap.md`, referenciando os critérios do barema.

Nenhum código de treinamento, dataset ou escolha de cenário é definido nesta mudança — isso é objeto da Fase 1 (a ser proposta como uma mudança OpenSpec separada, após o grupo decidir o cenário).

## Capabilities

### New Capabilities
- `project-scaffolding`: estrutura de diretórios versionada do projeto (dados, notebooks, código, modelos, relatórios, vídeo), arquivos de configuração de ambiente (`requirements.txt`, `.gitignore`) e README inicial.
- `project-roadmap`: documento rastreável (`docs/roadmap.md`) com as 5 fases do projeto, seus objetivos e entregáveis, servindo de referência para futuras mudanças OpenSpec (uma por fase).

### Modified Capabilities
(nenhuma — projeto greenfield, sem specs existentes)

## Impact

- Novos diretórios e arquivos de configuração na raiz do repositório; nenhum código de aplicação é afetado (não existe ainda).
- Define a convenção de onde cada tipo de artefato (dataset, notebook, script, modelo, relatório, vídeo) deve ser salvo pelas próximas fases do projeto.
- `CLAUDE.md` deve ser atualizado (fora desta mudança, ou em revisão futura) para referenciar a estrutura de pastas criada aqui, uma vez que ela deixa de ser "projeto sem código".
