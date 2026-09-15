## Why

O integrante pediu para usar Parquet em vez de CSV para os dados tabulares gerados pelo próprio projeto (ex. eventos de violação de EPI), em vez de texto delimitado. Parquet é colunar, tipado e mais compacto — melhor para dados que podem ser consumidos depois em pandas/notebooks (Fase 5, relatório técnico).

## What Changes

- Trocar a saída de `reports/violacoes-epi.csv` para `reports/violacoes-epi.parquet` (usando `pandas.DataFrame.to_parquet`, engine `pyarrow`).
- Adicionar `pyarrow` ao `requirements.txt`.
- Fixar a convenção: dados tabulares gerados pelo projeto (não os `results.csv` que o próprio Ultralytics gera durante o treino, que ficam como estão) devem usar Parquet, não CSV.

## Capabilities

### Modified Capabilities
- `compliance-reporting`: o requisito de relatório de conformidade passa a exigir saída em Parquet, não CSV.

## Impact

- `src/step14_inference_compliance_report.py` atualizado (função `write_csv` → `write_parquet`).
- `requirements.txt` ganha `pyarrow`.
- Não afeta os `results.csv`/`results.png` gerados pelo Ultralytics durante o treino (Fases 2 e 3) — esses são artefatos padrão da biblioteca, fora do escopo desta convenção.
