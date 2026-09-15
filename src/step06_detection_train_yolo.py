"""Fine-tuning do detector YOLOv8n sobre o subconjunto Construction Site
Safety (Fase 1). Hiperparametros documentados em
openspec/changes/fase-2-baseline-deteccao/design.md (e depois em
reports/deteccao-fase2.md).

Uso:
    python src/step06_detection_train_yolo.py
"""

from pathlib import Path

from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
DATA_YAML = ROOT / "data" / "raw" / "construction-site-safety" / "data.yaml"
PROJECT_DIR = ROOT / "models" / "detection"
RUN_NAME = "css_yolov8n_baseline"

HYPERPARAMS = dict(
    model="yolov8n.pt",
    epochs=30,
    imgsz=640,
    batch=16,
    optimizer="auto",
    seed=42,
    patience=100,
)


def main():
    model = YOLO(HYPERPARAMS["model"])
    model.train(
        data=str(DATA_YAML),
        epochs=HYPERPARAMS["epochs"],
        imgsz=HYPERPARAMS["imgsz"],
        batch=HYPERPARAMS["batch"],
        optimizer=HYPERPARAMS["optimizer"],
        seed=HYPERPARAMS["seed"],
        patience=HYPERPARAMS["patience"],
        project=str(PROJECT_DIR),
        name=RUN_NAME,
        exist_ok=True,
        verbose=True,
    )
    print(f"Treino concluido. Resultados em: {PROJECT_DIR / RUN_NAME}")


if __name__ == "__main__":
    main()
