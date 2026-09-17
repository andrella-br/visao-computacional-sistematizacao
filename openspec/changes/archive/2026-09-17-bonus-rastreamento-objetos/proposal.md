## Why

O enunciado oferece um item de bônus (até +0,5 ponto, limitado à nota máxima): rastreamento de objetos no vídeo (ByteTrack/DeepSORT) ou demo interativa (Gradio/HF Spaces). Com o projeto já cobrindo todos os requisitos obrigatórios (Fases 1-4), o integrante optou por implementar o rastreamento — extensão natural do relatório de conformidade já existente (Fase 4 + aplicação prática), já que o Ultralytics oferece ByteTrack embutido.

## What Changes

- Rodar o detector (Fase 2) com **ByteTrack** (`model.track()`, tracker embutido no Ultralytics) sobre o vídeo do cenário, atribuindo um ID persistente a cada objeto entre quadros.
- Gerar um vídeo anotado com os IDs visíveis (`video/output/deteccao_epi_tracking/`).
- Refinar a contagem de violações: em vez de só "eventos" agrupados por proximidade de tempo (heurística da Fase 4), contar **objetos rastreados distintos** (violações unicas, deduplicadas por identidade), e comparar as duas contagens.
- Documentar o resultado no relatório técnico e nos notebooks (célula de bônus, após o relatório de conformidade).

Fora de escopo: demo interativa (Gradio) — não implementada, mencionada como opção alternativa de bônus não escolhida.

## Capabilities

### New Capabilities
- `object-tracking`: rastreamento de objetos no vídeo (ByteTrack) com IDs persistentes, vídeo anotado e contagem de violações únicas deduplicadas — item de bônus do enunciado.

### Modified Capabilities
(nenhuma)

## Impact

- Novo arquivo: `src/step16_inference_tracking.py`.
- `requirements.txt` ganha `lap` (dependência do ByteTrack para associação de detecções).
- Novas saídas: `video/output/deteccao_epi_tracking/` (vídeo anotado, gitignorado), `reports/tracking-epi.parquet`, `reports/relatorio-tracking.md`.
- `docs/relatorio-tecnico.md` ganha a seção 8.1 (Bônus: Rastreamento).
- `visao_computacional_06_report.ipynb` e `visao_computacional_pipeline_completo.ipynb` ganham a célula de bônus, com texto e código idênticos ao script (validado rodando as células extraídas).
