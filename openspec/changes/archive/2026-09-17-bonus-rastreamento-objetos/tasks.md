## 1. Rastreamento

- [x] 1.1 Criar `src/step16_inference_tracking.py` que roda `model.track()` (ByteTrack) sobre o vídeo, salvando o vídeo anotado com IDs e um resumo por track (Parquet)
- [x] 1.2 Adicionar `lap` ao `requirements.txt` (dependência do ByteTrack)
- [x] 1.3 Comparar a contagem de eventos por tempo (Fase 4) com a contagem de tracks únicos por classe, documentando ambas
- [x] 1.4 Rodar o script localmente e verificar que o vídeo anotado e o parquet são gerados corretamente

## 2. Documentação e notebooks

- [x] 2.1 Adicionar a seção 8.1 (Bônus: Rastreamento) em `docs/relatorio-tecnico.md`, com os números obtidos
- [x] 2.2 Adicionar a célula de bônus (código + explicação) em `visao_computacional_06_report.ipynb` e no notebook consolidado, reaproveitando as variáveis já calculadas na célula anterior
- [x] 2.3 Validar rodando as células extraídas em sequência contra os dados reais do projeto, confirmando resultado idêntico ao script

## 3. Validação final

- [x] 3.1 Rodar `openspec validate bonus-rastreamento-objetos --strict` e confirmar que a mudança passa sem erros
