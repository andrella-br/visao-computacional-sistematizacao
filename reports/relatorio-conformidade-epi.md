# Relatório de Conformidade de EPI

Vídeo analisado: `video/input/video_final_canteiro_obra.mp4` (38.3s). Detector: `models/detection/css_yolov8n_baseline` (conf≥0.25).

## Resumo por classe de violação

| Classe | Eventos | Tempo total (s) | % do vídeo |
|---|---:|---:|---:|
| NO-Hardhat | 1 | 0.1 | 0.3% |
| NO-Mask | 7 | 12.4 | 32.4% |
| NO-Safety Vest | 4 | 24.0 | 62.8% |

## Eventos individuais

| Classe | Início (s) | Fim (s) | Duração (s) | Confiança média |
|---|---:|---:|---:|---:|
| NO-Safety Vest | 0.00 | 20.40 | 20.40 | 0.466 |
| NO-Mask | 0.00 | 10.04 | 10.04 | 0.469 |
| NO-Mask | 14.44 | 14.80 | 0.36 | 0.453 |
| NO-Mask | 15.92 | 16.00 | 0.08 | 0.344 |
| NO-Mask | 16.64 | 16.92 | 0.28 | 0.341 |
| NO-Safety Vest | 21.72 | 25.36 | 3.64 | 0.401 |
| NO-Safety Vest | 26.04 | 26.04 | 0.00 | 0.272 |
| NO-Safety Vest | 26.96 | 26.96 | 0.00 | 0.251 |
| NO-Mask | 32.20 | 33.68 | 1.48 | 0.348 |
| NO-Mask | 35.84 | 36.00 | 0.16 | 0.343 |
| NO-Hardhat | 37.08 | 37.20 | 0.12 | 0.307 |
| NO-Mask | 38.24 | 38.24 | 0.00 | 0.343 |

## Nota sobre ruído

Alguns eventos têm duração muito curta (~0s, um único quadro) e confiança próxima do limiar (0.25) — provavelmente falsos positivos pontuais do baseline (30 épocas, ver `reports/deteccao-fase2.md`). Um sistema de produção usaria um limiar de confiança mais alto e/ou duração mínima de evento (ex. ≥1s) para reduzir ruído.


## Aplicação prática

Este relatório é uma auditoria automática de segurança: em vez de assistir ao vídeo inteiro, um responsável de segurança do trabalho pode consultar diretamente os eventos acima (`reports/violacoes-epi.parquet`) para saber exatamente quando cada EPI esteve ausente, sem precisar rever a gravação manualmente.
