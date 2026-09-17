# Rastreamento de Objetos (Bônus) — ByteTrack

Vídeo analisado: `video/input/video_final_canteiro_obra.mp4`. Detector: `models/detection/css_yolov8n_baseline` + tracker `bytetrack.yaml` (conf≥0.25).

**Total de objetos rastreados (tracks únicos):** 99

**Pessoas únicas (`Person`) rastreadas no vídeo:** 20

## Violações únicas por classe (deduplicadas por track)

| Classe | Objetos rastreados distintos |
|---|---:|
| NO-Hardhat | 0 |
| NO-Mask | 16 |
| NO-Safety Vest | 26 |

## Por que isso importa

O relatório de conformidade original (`reports/relatorio-conformidade-epi.md`) agrupa detecções por proximidade de tempo, mas não sabe se duas detecções em momentos diferentes são a *mesma* pessoa/objeto ou pessoas diferentes. Com rastreamento (ByteTrack), cada objeto detectado recebe um ID persistente entre quadros, permitindo contar quantas violações **realmente distintas** ocorreram, em vez de apenas quantos intervalos de tempo tiveram detecção.
