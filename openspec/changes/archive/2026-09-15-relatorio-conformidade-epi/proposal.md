## Why

O detector da Fase 2 e a inferência em vídeo da Fase 4 já geram, por quadro, quais EPIs estão presentes ou ausentes — mas essa informação fica "presa" dentro do vídeo anotado, exigindo assistir tudo para descobrir onde houve violação. Uma aplicação prática real (auditoria de segurança automática) é transformar essas detecções em um relatório de conformidade: quando, por quanto tempo e com que confiança cada violação de EPI ocorreu.

## What Changes

- Rodar o detector (Fase 2) sobre o vídeo (`video/input/video_final_canteiro_obra.mp4`) quadro a quadro, capturando as classes de violação (`NO-Hardhat`, `NO-Mask`, `NO-Safety Vest`) por quadro, com timestamp e confiança.
- Agrupar detecções consecutivas da mesma classe em "eventos de violação" (início/fim, duração, confiança média), em vez de listar quadro a quadro (ruidoso e repetitivo).
- Gerar um CSV bruto (um evento por linha) e um relatório em Markdown com resumo por classe (número de eventos, tempo total de violação, % do vídeo) e os eventos individuais.

Fora de escopo: alertas em tempo real, interface interativa (Gradio) — fica para o item de bônus do enunciado, se houver tempo.

## Capabilities

### New Capabilities
- `compliance-reporting`: geração de relatório de conformidade de EPI (eventos de violação agregados por classe, com timestamp/duração/confiança) a partir da inferência em vídeo do detector.

### Modified Capabilities
(nenhuma)

## Impact

- Novo arquivo: `src/step14_inference_compliance_report.py`.
- Saídas: `reports/violacoes-epi.csv` (dados brutos) e `reports/relatorio-conformidade-epi.md` (resumo legível).
