"""Bonus do enunciado: rastreamento de objetos no video (ByteTrack, embutido
no Ultralytics). Roda o detector com tracking sobre o video do cenario,
gera um video anotado com IDs persistentes por objeto, e refina o
relatorio de conformidade contando VIOLACOES UNICAS (por track) em vez de
eventos brutos por quadro/lacuna de tempo (que podem contar a mesma pessoa
varias vezes).

Uso:
    python src/step16_inference_tracking.py
"""

from collections import defaultdict
from pathlib import Path

import pandas as pd
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
VIDEO_INPUT = ROOT / "video" / "input" / "video_final_canteiro_obra.mp4"
VIDEO_OUTPUT_DIR = ROOT / "video" / "output"
DETECTION_WEIGHTS = ROOT / "models" / "detection" / "css_yolov8n_baseline" / "weights" / "best.pt"
REPORTS_DIR = ROOT / "reports"

CLASS_NAMES = [
    "Hardhat", "Mask", "NO-Hardhat", "NO-Mask", "NO-Safety Vest",
    "Person", "Safety Cone", "Safety Vest", "machinery", "vehicle",
]
VIOLATION_CLASSES = {"NO-Hardhat", "NO-Mask", "NO-Safety Vest"}
CONF_THRESHOLD = 0.25
TRACKER = "bytetrack.yaml"  # tracker embutido no Ultralytics


def run_tracking():
    """Roda o detector com ByteTrack sobre o video, salvando o video anotado
    com IDs persistentes e coletando (track_id, classe, confianca) por
    quadro em que cada track aparece."""
    model = YOLO(str(DETECTION_WEIGHTS))

    track_observations = defaultdict(list)  # track_id -> [(classe, conf), ...]

    for result in model.track(
        source=str(VIDEO_INPUT),
        conf=CONF_THRESHOLD,
        tracker=TRACKER,
        persist=True,
        stream=True,
        save=True,
        project=str(VIDEO_OUTPUT_DIR),
        name="deteccao_epi_tracking",
        exist_ok=True,
        verbose=False,
    ):
        if result.boxes.id is None:
            continue
        track_ids = result.boxes.id.int().tolist()
        classes = result.boxes.cls.tolist()
        confs = result.boxes.conf.tolist()
        for tid, cls_id, conf in zip(track_ids, classes, confs):
            track_observations[tid].append((CLASS_NAMES[int(cls_id)], conf))

    return track_observations


def summarize_tracks(track_observations):
    """Para cada track, usa a classe mais frequente observada (modo) como a
    classe "real" do track, e a confianca media. Retorna um DataFrame com
    uma linha por track."""
    rows = []
    for track_id, observations in track_observations.items():
        classes = [c for c, _ in observations]
        confs = [c for _, c in observations]
        dominant_class = max(set(classes), key=classes.count)
        rows.append({
            "track_id": track_id,
            "classe": dominant_class,
            "n_deteccoes": len(observations),
            "confianca_media": round(sum(confs) / len(confs), 3),
        })
    return pd.DataFrame(rows)


def main():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    print("Rodando deteccao + rastreamento (ByteTrack) no video...")
    track_observations = run_tracking()
    print(f"Objetos rastreados (tracks unicos): {len(track_observations)}")

    tracks_df = summarize_tracks(track_observations)
    tracks_path = REPORTS_DIR / "tracking-epi.parquet"
    tracks_df.to_parquet(tracks_path, engine="pyarrow", index=False)
    print(f"Parquet salvo: {tracks_path}")

    n_person_tracks = (tracks_df["classe"] == "Person").sum()
    print(f"\nPessoas unicas rastreadas no video: {n_person_tracks}")

    print("\nViolacoes UNICAS (por track, deduplicadas) por classe:")
    violation_counts = {}
    for cls in sorted(VIOLATION_CLASSES):
        n = (tracks_df["classe"] == cls).sum()
        violation_counts[cls] = int(n)
        print(f"  {cls}: {n} objeto(s) rastreado(s) distinto(s)")

    # Comparacao com a contagem de eventos por lacuna de tempo (step14/15)
    frame_events_path = REPORTS_DIR / "violacoes-epi.parquet"
    if frame_events_path.exists():
        frame_events = pd.read_parquet(frame_events_path)
        print("\nComparacao com eventos brutos (agrupados por lacuna de tempo, step14):")
        for cls in sorted(VIOLATION_CLASSES):
            n_events = (frame_events["classe"] == cls).sum()
            n_tracks = violation_counts[cls]
            print(f"  {cls}: {n_events} eventos (tempo) vs {n_tracks} objetos rastreados distintos")

    report_path = REPORTS_DIR / "relatorio-tracking.md"
    lines = [
        "# Rastreamento de Objetos (Bônus) — ByteTrack\n",
        f"Vídeo analisado: `video/input/video_final_canteiro_obra.mp4`. "
        f"Detector: `models/detection/css_yolov8n_baseline` + tracker `{TRACKER}` "
        f"(conf≥{CONF_THRESHOLD}).\n",
        f"**Total de objetos rastreados (tracks únicos):** {len(track_observations)}\n",
        f"**Pessoas únicas (`Person`) rastreadas no vídeo:** {n_person_tracks}\n",
        "## Violações únicas por classe (deduplicadas por track)\n",
        "| Classe | Objetos rastreados distintos |",
        "|---|---:|",
    ]
    for cls in sorted(VIOLATION_CLASSES):
        lines.append(f"| {cls} | {violation_counts[cls]} |")

    lines.append(
        "\n## Por que isso importa\n\n"
        "O relatório de conformidade original (`reports/relatorio-conformidade-epi.md`) "
        "agrupa detecções por proximidade de tempo, mas não sabe se duas detecções em "
        "momentos diferentes são a *mesma* pessoa/objeto ou pessoas diferentes. Com "
        "rastreamento (ByteTrack), cada objeto detectado recebe um ID persistente entre "
        "quadros, permitindo contar quantas violações **realmente distintas** ocorreram, "
        "em vez de apenas quantos intervalos de tempo tiveram detecção.\n"
    )
    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nRelatório salvo: {report_path}")
    print(f"Vídeo com rastreamento salvo em: {VIDEO_OUTPUT_DIR / 'deteccao_epi_tracking'}")


if __name__ == "__main__":
    main()
