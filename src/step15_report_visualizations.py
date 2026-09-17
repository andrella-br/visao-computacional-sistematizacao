"""Gera visualizacoes do relatorio de conformidade de EPI (step14): graficos
de barras (eventos e tempo total por classe), uma linha do tempo das
violacoes ao longo do video, e quadros de exemplo anotados para cada classe
de violacao.

Uso:
    python src/step15_report_visualizations.py
"""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt
import pandas as pd
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
VIDEO_INPUT = ROOT / "video" / "input" / "video_final_canteiro_obra.mp4"
DETECTION_WEIGHTS = ROOT / "models" / "detection" / "css_yolov8n_baseline" / "weights" / "best.pt"
REPORTS_DIR = ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
PARQUET_PATH = REPORTS_DIR / "violacoes-epi.parquet"

CONF_THRESHOLD = 0.25
VIOLATION_COLORS = {
    "NO-Hardhat": "#E24A33",
    "NO-Mask": "#348ABD",
    "NO-Safety Vest": "#988ED5",
}


def get_video_info():
    cap = cv2.VideoCapture(str(VIDEO_INPUT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    cap.release()
    return duration, fps


def plot_bars(df, video_duration):
    resumo = (
        df.groupby("classe")
        .agg(eventos=("classe", "count"), tempo_total_s=("duracao_s", "sum"))
        .reindex(list(VIOLATION_COLORS))
        .fillna(0)
    )
    resumo["pct_do_video"] = (resumo["tempo_total_s"] / video_duration * 100).round(1)
    colors = [VIOLATION_COLORS[c] for c in resumo.index]

    fig, axes = plt.subplots(1, 2, figsize=(12, 4.5))

    axes[0].bar(resumo.index, resumo["eventos"], color=colors)
    axes[0].set_title("Número de eventos por classe")
    axes[0].set_ylabel("Eventos")
    axes[0].tick_params(axis="x", rotation=20)

    axes[1].bar(resumo.index, resumo["tempo_total_s"], color=colors)
    axes[1].set_title("Tempo total de violação por classe")
    axes[1].set_ylabel("Segundos")
    axes[1].tick_params(axis="x", rotation=20)
    for i, (_, row) in enumerate(resumo.iterrows()):
        axes[1].text(i, row["tempo_total_s"] + 0.3, f"{row['pct_do_video']}%", ha="center", fontsize=9)

    plt.tight_layout()
    out_path = FIGURES_DIR / "conformidade_barras_por_classe.png"
    fig.savefig(out_path, dpi=150)
    plt.show()
    print(f"Gráfico salvo: {out_path}")
    return resumo


def plot_timeline(df, video_duration):
    classes = list(VIOLATION_COLORS)
    fig, ax = plt.subplots(figsize=(12, 3))
    for i, cls in enumerate(classes):
        rows = df[df["classe"] == cls]
        bars = [(row.inicio_s, max(row.duracao_s, 0.15)) for row in rows.itertuples()]
        ax.broken_barh(bars, (i - 0.4, 0.8), facecolors=VIOLATION_COLORS[cls])
    ax.set_yticks(range(len(classes)))
    ax.set_yticklabels(classes)
    ax.set_xlabel("Tempo no vídeo (s)")
    ax.set_xlim(0, video_duration)
    ax.set_title("Linha do tempo das violações de EPI")
    ax.grid(axis="x", alpha=0.3)
    plt.tight_layout()
    out_path = FIGURES_DIR / "conformidade_timeline.png"
    fig.savefig(out_path, dpi=150)
    plt.show()
    print(f"Gráfico salvo: {out_path}")


def save_example_frames(df, fps):
    model = YOLO(str(DETECTION_WEIGHTS))
    cap = cv2.VideoCapture(str(VIDEO_INPUT))

    fig, axes = plt.subplots(1, len(VIOLATION_COLORS), figsize=(15, 5))
    for ax, cls in zip(axes, VIOLATION_COLORS):
        rows = df[df["classe"] == cls]
        ax.axis("off")
        if rows.empty:
            ax.set_title(f"{cls}\n(nenhum evento)")
            continue

        best = rows.loc[rows["duracao_s"].idxmax()]
        mid_time = (best["inicio_s"] + best["fim_s"]) / 2
        frame_idx = int(mid_time * fps)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ok, frame = cap.read()
        if not ok:
            ax.set_title(f"{cls}\n(falha ao ler quadro)")
            continue

        result = model.predict(source=frame, conf=CONF_THRESHOLD, verbose=False)[0]
        annotated = result.plot()
        ax.imshow(annotated[:, :, ::-1])
        ax.set_title(f"{cls}\nt={mid_time:.1f}s, dur={best['duracao_s']:.1f}s")

    cap.release()
    plt.tight_layout()
    out_path = FIGURES_DIR / "conformidade_exemplos_por_classe.png"
    fig.savefig(out_path, dpi=150)
    plt.show()
    print(f"Exemplos salvos: {out_path}")


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_parquet(PARQUET_PATH)
    video_duration, fps = get_video_info()

    resumo = plot_bars(df, video_duration)
    print(resumo)

    plot_timeline(df, video_duration)
    save_example_frames(df, fps)


if __name__ == "__main__":
    main()
