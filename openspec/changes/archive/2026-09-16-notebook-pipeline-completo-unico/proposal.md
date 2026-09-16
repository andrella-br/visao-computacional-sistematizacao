## Why

O integrante pediu para manter os 6 notebooks por fase e, além deles, ter um único notebook com todo o código para rodar o pipeline inteiro em um arquivo só (útil para anexar como entrega única ou rodar tudo numa sessão Colab sem alternar entre notebooks).

## What Changes

- Criar `notebooks/visao_computacional_pipeline_completo.ipynb`, concatenando as células dos 6 notebooks por fase na ordem (dados → detecção → segmentação → avaliação → vídeo → relatório), com uma única célula de setup (pip install + mount do Drive) no topo em vez de repetida em cada seção.
- Os 6 notebooks por fase continuam existindo, inalterados.

## Capabilities

### Modified Capabilities
- `repository-packaging`: o requisito de notebooks Colab passa a incluir também um notebook consolidado (`visao_computacional_pipeline_completo.ipynb`), além dos 6 por fase.

## Impact

- Novo arquivo: `notebooks/visao_computacional_pipeline_completo.ipynb` (45 células, reaproveitando o mesmo código validado dos 6 notebooks por fase).
- `README.md` atualizado com as duas opções de uso (por fase ou consolidado).
