# Vídeo de entrada — fonte e licença

Três clipes gratuitos do [Pexels](https://www.pexels.com/) (licença
[Pexels License](https://www.pexels.com/license/): uso livre comercial e
não comercial, sem atribuição obrigatória), todos do cenário de segurança
do trabalho em canteiro de obra:

| Arquivo | Fonte |
|---|---|
| `19832492-hd_1280_720_25fps.mp4` | [A Construction Worker Is Working On A Stone Wall](https://www.pexels.com/video/a-construction-worker-is-working-on-a-stone-wall-19832492/) |
| `14626383_720_1280_30fps.mp4` | [Construction Site Workers Carrying Materials Outdoors](https://www.pexels.com/video/construction-site-workers-carrying-materials-outdoors-34521515/) |
| `15518317_720_1280_60fps.mp4` | [Construction Worker Setting Up Scaffolding](https://www.pexels.com/video/construction-worker-setting-up-scaffolding-36601732/) |

Nenhum dos três, individualmente, atinge os 30 segundos mínimos exigidos
pelo enunciado (19.8s, 8.4s e 10.1s respectivamente). Por isso, foram
concatenados em um único vídeo contínuo de 38.3s:

**`video_final_canteiro_obra.mp4`** — 1280×720, 25fps, gerado por
[`src/step10_inference_concat_videos.py`](../../src/step10_inference_concat_videos.py)
(os dois clipes em retrato foram padronizados para 1280×720 com letterbox,
preservando a proporção original sem distorcer as pessoas).

Este é o vídeo usado na inferência da Fase 4.
