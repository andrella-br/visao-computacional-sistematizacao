## 1. Relatório técnico

- [x] 1.1 Escrever `docs/relatorio-tecnico.md` consolidando: problema/cenário, dataset e EDA (Fase 1), metodologia e resultados de detecção (Fase 2), metodologia e resultados de segmentação (Fase 3), avaliação no teste e análise de erros (Fase 4), aplicação prática (relatório de conformidade), limitações e próximos passos, e citação das fontes de dados/vídeo
- [x] 1.2 Verificar que o relatório tem extensão equivalente a 6-10 páginas e que todas as métricas citadas batem com os relatórios de origem (`reports/*.md`)
- [x] 1.3 Adicionar um link para o relatório técnico no `README.md`

## 2. Repositório Git

- [x] 2.1 Rodar `git init` na raiz do projeto
- [x] 2.2 Revisar `git status` (respeitando o `.gitignore`) antes de commitar, confirmando que dados brutos, pesos de modelo e vídeos não aparecem como untracked/staged
- [x] 2.3 Criar o primeiro commit com o estado atual do projeto

## 3. Notebook Colab

- [x] 3.1 Criar `notebooks/pipeline_completo.ipynb` com células markdown+código cobrindo, na ordem, os scripts `step01` a `step14`, incluindo célula de setup (clonar repo/instalar dependências) e nota sobre credenciais do Kaggle no Colab
- [x] 3.2 Verificar que o notebook é um `.ipynb` válido (abre sem erro) e que a ordem das células corresponde à ordem `stepNN` dos scripts

## 4. Validação final

- [x] 4.1 Rodar `openspec validate fase-5-relatorio-e-repositorio --strict` e confirmar que a mudança passa sem erros
- [x] 4.2 Confirmar com o integrante que nenhum push para repositório remoto foi feito (escopo desta mudança é só o commit local)
