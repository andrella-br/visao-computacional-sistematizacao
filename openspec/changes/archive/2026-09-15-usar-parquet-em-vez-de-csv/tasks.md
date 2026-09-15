## 1. Trocar CSV por Parquet

- [x] 1.1 Instalar `pyarrow` no ambiente virtual e adicionar ao `requirements.txt`
- [x] 1.2 Atualizar `src/step14_inference_compliance_report.py` (`write_csv` → `write_parquet`, saída `reports/violacoes-epi.parquet`)
- [x] 1.3 Remover `reports/violacoes-epi.csv` e regenerar `reports/violacoes-epi.parquet` + `reports/relatorio-conformidade-epi.md`, verificando que os dados batem com a versão anterior em CSV

## 2. Validação final

- [x] 2.1 Rodar `openspec validate usar-parquet-em-vez-de-csv --strict` e confirmar que a mudança passa sem erros
