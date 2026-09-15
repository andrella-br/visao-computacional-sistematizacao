## 1. Ambiente virtual

- [x] 1.1 Criar `.venv/` na raiz do projeto e instalar `requirements.txt` dentro dele, e verificar com `pip list` (dentro do venv) que os pacotes estão instalados
- [x] 1.2 Confirmar que `.venv/` já está no `.gitignore` (não precisa de nova entrada)

## 2. Reorganização de scripts

- [x] 2.1 Mover os 4 scripts de `src/data/` para `src/` com prefixo numérico de execução (`step1_...` a `step4_...`) e remover as subpastas vazias `src/detection`, `src/segmentation`, `src/evaluation`, `src/inference`
- [x] 2.2 Corrigir os caminhos internos (`parents[N]`) de cada script movido para refletir o novo local, e verificar rodando `python src/step3_make_splits.py` que os splits reproduzidos batem com os já existentes (mesma seed, mesma contagem)

## 3. Documentação

- [x] 3.1 Atualizar `README.md`: estrutura de pastas (src/ flat e numerado), passo de criação do `.venv/` em "Como reproduzir"
- [x] 3.2 Atualizar `CLAUDE.md`: comandos de setup/execução e a convenção de nomeação `stepN_` para scripts futuros

## 4. Validação final

- [x] 4.1 Rodar `openspec validate reorganizar-scripts-e-ambiente-virtual --strict` e confirmar que a mudança passa sem erros
- [x] 4.2 Verificar que `find src -type f` mostra só os 4 scripts numerados (sem subpastas remanescentes)
