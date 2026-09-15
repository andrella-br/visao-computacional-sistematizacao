## 1. Renomear scripts

- [x] 1.1 Renomear os 4 scripts de `stepN_*.py` para `stepNN_data_*.py` (dois dígitos + tag `data`) e verificar com `find src -type f` que só os 4 arquivos renomeados existem
- [x] 1.2 Corrigir a docstring de uso (`python src/stepNN_...`) em cada script renomeado
- [x] 1.3 Rodar `python src/step03_data_make_splits.py` e verificar que os splits reproduzidos batem com os já existentes (mesma seed, mesma contagem)

## 2. Documentação

- [x] 2.1 Atualizar `README.md` com a convenção `stepNN_<fase>_<descrição>.py` e os novos nomes de comando em "Como reproduzir"
- [x] 2.2 Atualizar `CLAUDE.md` com a convenção e os novos comandos

## 3. Validação final

- [x] 3.1 Rodar `openspec validate nomear-scripts-com-fase --strict` e confirmar que a mudança passa sem erros
