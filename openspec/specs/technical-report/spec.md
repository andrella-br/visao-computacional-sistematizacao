# technical-report Specification

## Purpose

Consolida todo o trabalho das Fases 1-4 em um único relatório técnico legível, cobrindo problema, dados, metodologia, resultados, análise de erros e limitações — atendendo ao Item 1 da entrega da disciplina.

## Requirements

### Requirement: Relatório técnico consolidado
O repositório SHALL conter um relatório técnico único (`docs/relatorio-tecnico.md`) cobrindo: problema e cenário, dataset e EDA, metodologia (modelos e hiperparâmetros de detecção e segmentação), resultados com métricas (validação e teste), análise de erros, limitações e próximos passos — com extensão equivalente a 6-10 páginas.

#### Scenario: Avaliador encontra tudo em um único documento
- **WHEN** o professor abre `docs/relatorio-tecnico.md`
- **THEN** encontra, sem precisar navegar por múltiplos arquivos separados, o problema, o dataset, a metodologia, os resultados de detecção e segmentação, a análise de erros e as limitações do projeto

### Requirement: Citação de fontes de terceiros
O relatório técnico SHALL citar explicitamente as fontes de dados e vídeo de terceiros usadas (Construction Site Safety, COCO, vídeos do Pexels), com link e licença, conforme exigido pela integridade acadêmica do enunciado.

#### Scenario: Fonte é rastreável a partir do relatório
- **WHEN** alguém quer verificar a origem de um dataset citado no relatório
- **THEN** encontra o link e a licença da fonte diretamente no relatório técnico, sem precisar procurar em outros arquivos

### Requirement: README aponta para o relatório técnico
O `README.md` SHALL referenciar o relatório técnico completo, sem duplicar seu conteúdo.

#### Scenario: Visitante do repositório encontra o relatório
- **WHEN** alguém abre o `README.md` do repositório
- **THEN** encontra um link claro para `docs/relatorio-tecnico.md`
