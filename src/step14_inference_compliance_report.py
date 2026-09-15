"""Roda o detector (Fase 2) sobre o video do cenario e gera um relatorio de
conformidade de EPI: agrupa detecoes de violacao (NO-Hardhat, NO-Mask,
NO-Safety Vest) em eventos (inicio/fim/duracao/confianca media) e salva os
dados brutos em Parquet + um resumo em Markdown.

Uso:
    python src/step14_inference_compliance_report.py
"""

from pathlib import Path

import cv2
import pandas as pd
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
VIDEO_INPUT = ROOT / "video" / "input" / "video_final_canteiro_obra.mp4"
DETECTION_WEIGHTS = ROOT / "models" / "detection" / "css_yolov8n_baseline" / "weights" / "best.pt"
REPORTS_DIR = ROOT / "reports"

CLASS_NAMES = [
    "Hardhat", "Mask", "NO-Hardhat", "NO-Mask", "NO-Safety Vest",
    "Person", "Safety Cone", "Safety Vest", "machinery", "vehicle",
]
VIOLATION_CLASSES = {"NO-Hardhat", "NO-Mask", "NO-Safety Vest"}
CONF_THRESHOLD = 0.25
MAX_GAP_SECONDS = 0.5  # lacuna tolerada (sem deteccao) para nao quebrar um evento


def get_video_fps(video_path):
    cap = cv2.VideoCapture(str(video_path))
    fps = cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    return fps


def collect_frame_detections(fps):
    """Roda o detector quadro a quadro e retorna uma lista de
    (timestamp_seg, classe, confianca) para cada deteccao de violacao."""
    model = YOLO(str(DETECTION_WEIGHTS))
    detections = []

    frame_idx = 0
    for result in model.predict(source=str(VIDEO_INPUT), conf=CONF_THRESHOLD, stream=True, verbose=False):
        timestamp = frame_idx / fps
        for cls_id, conf in zip(result.boxes.cls.tolist(), result.boxes.conf.tolist()):
            class_name = CLASS_NAMES[int(cls_id)]
            if class_name in VIOLATION_CLASSES:
                detections.append((timestamp, class_name, conf))
        frame_idx += 1

    return detections


def group_into_events(detections):
    """Agrupa deteccoes consecutivas da mesma classe em eventos, tolerando
    lacunas curtas (MAX_GAP_SECONDS)."""
    by_class = {}
    for ts, cls, conf in detections:
        by_class.setdefault(cls, []).append((ts, conf))

    events = []
    for cls, items in by_class.items():
        items.sort(key=lambda x: x[0])
        current_start = items[0][0]
        current_end = items[0][0]
        current_confs = [items[0][1]]

        for ts, conf in items[1:]:
            if ts - current_end <= MAX_GAP_SECONDS:
                current_end = ts
                current_confs.append(conf)
            else:
                events.append((cls, current_start, current_end, sum(current_confs) / len(current_confs)))
                current_start = ts
                current_end = ts
                current_confs = [conf]

        events.append((cls, current_start, current_end, sum(current_confs) / len(current_confs)))

    events.sort(key=lambda e: e[1])
    return events


def write_parquet(events, out_path):
    df = pd.DataFrame(
        [
            {
                "classe": cls,
                "inicio_s": round(start, 2),
                "fim_s": round(end, 2),
                "duracao_s": round(end - start, 2),
                "confianca_media": round(conf, 3),
            }
            for cls, start, end, conf in events
        ]
    )
    df.to_parquet(out_path, engine="pyarrow", index=False)


def write_report(events, video_duration, out_path):
    by_class = {}
    for cls, start, end, conf in events:
        by_class.setdefault(cls, []).append((start, end, conf))

    lines = [
        "# Relatório de Conformidade de EPI\n",
        f"Vídeo analisado: `video/input/video_final_canteiro_obra.mp4` "
        f"({video_duration:.1f}s). Detector: `models/detection/css_yolov8n_baseline` "
        f"(conf≥{CONF_THRESHOLD}).\n",
        "## Resumo por classe de violação\n",
        "| Classe | Eventos | Tempo total (s) | % do vídeo |",
        "|---|---:|---:|---:|",
    ]
    for cls in sorted(VIOLATION_CLASSES):
        items = by_class.get(cls, [])
        n_events = len(items)
        total_time = sum(end - start for start, end, _ in items)
        pct = (total_time / video_duration * 100) if video_duration else 0
        lines.append(f"| {cls} | {n_events} | {total_time:.1f} | {pct:.1f}% |")

    lines.append("\n## Eventos individuais\n")
    lines.append("| Classe | Início (s) | Fim (s) | Duração (s) | Confiança média |")
    lines.append("|---|---:|---:|---:|---:|")
    for cls, start, end, conf in events:
        lines.append(f"| {cls} | {start:.2f} | {end:.2f} | {end - start:.2f} | {conf:.3f} |")

    lines.append(
        "\n## Nota sobre ruído\n\n"
        "Alguns eventos têm duração muito curta (~0s, um único quadro) e "
        "confiança próxima do limiar (0.25) — provavelmente falsos positivos "
        "pontuais do baseline (30 épocas, ver `reports/deteccao-fase2.md`). "
        "Um sistema de produção usaria um limiar de confiança mais alto e/ou "
        "duração mínima de evento (ex. ≥1s) para reduzir ruído.\n"
    )
    lines.append(
        "\n## Aplicação prática\n\n"
        "Este relatório é uma auditoria automática de segurança: em vez de assistir "
        "ao vídeo inteiro, um responsável de segurança do trabalho pode consultar "
        "diretamente os eventos acima (`reports/violacoes-epi.parquet`) para saber "
        "exatamente quando cada EPI esteve ausente, sem precisar rever a gravação "
        "manualmente.\n"
    )

    out_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    fps = get_video_fps(VIDEO_INPUT)
    print(f"FPS do vídeo: {fps}")

    print("Rodando detector quadro a quadro (stream=True)...")
    detections = collect_frame_detections(fps)
    print(f"Detecções de violação capturadas: {len(detections)}")

    events = group_into_events(detections)
    print(f"Eventos agregados: {len(events)}")

    cap = cv2.VideoCapture(str(VIDEO_INPUT))
    video_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    cap.release()

    parquet_path = REPORTS_DIR / "violacoes-epi.parquet"
    write_parquet(events, parquet_path)
    print(f"Parquet salvo: {parquet_path}")

    report_path = REPORTS_DIR / "relatorio-conformidade-epi.md"
    write_report(events, video_duration, report_path)
    print(f"Relatório salvo: {report_path}")


if __name__ == "__main__":
    main()
