## 1. Estrutura de diretórios

- [x] 1.1 Criar `data/raw/`, `data/processed/`, `data/splits/{train,val,test}` com `.gitkeep` e verificar que aparecem em `git status` como pastas rastreadas
- [x] 1.2 Criar `notebooks/` com `.gitkeep` e verificar que o diretório existe
- [x] 1.3 Criar `src/{data,detection,segmentation,evaluation,inference}` com `.gitkeep` em cada subpasta e verificar a listagem via `find src -type d`
- [x] 1.4 Criar `models/{detection,segmentation}` com `.gitkeep` e verificar a listagem via `find models -type d`
- [x] 1.5 Criar `reports/figures/` com `.gitkeep` e verificar que existe
- [x] 1.6 Criar `video/{input,output}` com `.gitkeep` e verificar que existem

## 2. Configuração de ambiente

- [x] 2.1 Criar `requirements.txt` na raiz listando torch, torchvision, ultralytics, opencv-python e supervision, e verificar que `pip install -r requirements.txt` resolve sem erro de sintaxe (revisão manual do arquivo)
- [x] 2.2 Criar `.gitignore` cobrindo dados (`data/raw/*`, `data/processed/*`, mantendo `.gitkeep`), checkpoints de modelo (`models/**/*.pt`, `*.pth`), ambientes virtuais (`.venv/`, `venv/`) e checkpoints de notebook (`.ipynb_checkpoints/`), e verificar com `git status` que arquivos de teste nessas pastas não aparecem como untracked

## 3. Documentação inicial

- [x] 3.1 Criar `README.md` na raiz com objetivo do projeto, cenário (marcado como "a definir" até a Fase 1), estrutura de pastas e instruções de reprodução, e verificar que todas as pastas criadas na seção 1 são mencionadas
- [x] 3.2 Criar `docs/roadmap.md` com as 5 fases do projeto (objetivo, atividades, entregáveis e critério do barema associado a cada uma), conforme a spec `project-roadmap`, e verificar que as 5 fases do `Sistematizacao_Instruções.md` estão todas presentes
- [x] 3.3 Atualizar `CLAUDE.md` para referenciar a estrutura de pastas criada e o `docs/roadmap.md`, e verificar que a seção "Project status" deixa de dizer que não há código/estrutura

## 4. Validação final

- [x] 4.1 Rodar `openspec validate setup-estrutura-inicial-projeto --strict` e confirmar que a mudança passa sem erros
- [x] 4.2 Revisar manualmente que nenhuma escolha de cenário, dataset ou modelo foi decidida nesta mudança (fica para a Fase 1)
