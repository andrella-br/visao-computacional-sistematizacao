## 1. Detecção e agregação

- [x] 1.1 Criar `src/step14_inference_compliance_report.py` que roda o detector sobre o vídeo (`stream=True`), captura detecções das classes `NO-Hardhat`, `NO-Mask`, `NO-Safety Vest` por quadro com timestamp e confiança
- [x] 1.2 Agrupar detecções consecutivas da mesma classe em eventos (início, fim, duração, confiança média), tolerando pequenas lacunas (ex. 1 quadro sem detecção não quebra o evento)
- [x] 1.3 Salvar os eventos em `reports/violacoes-epi.csv` e verificar que cada linha tem classe, início, fim, duração e confiança média

## 2. Relatório

- [x] 2.1 Escrever `reports/relatorio-conformidade-epi.md` com resumo por classe (nº de eventos, tempo total, % do vídeo) e a lista de eventos individuais
- [x] 2.2 Verificar que os números do resumo batem com o CSV (soma de duração por classe, contagem de eventos)

## 3. Validação final

- [x] 3.1 Rodar `openspec validate relatorio-conformidade-epi --strict` e confirmar que a mudança passa sem erros
