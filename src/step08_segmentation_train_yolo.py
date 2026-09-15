"""Fine-tuning do segmentador YOLOv8n-seg sobre o subconjunto coco-person
(Fase 1). Hiperparametros documentados em
openspec/changes/fase-3-segmentacao/design.md (e depois em
reports/segmentacao-fase3.md).

Uso:
    python src/step08_segmentation_train_yolo.py
"""

from pathlib import Path

from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
DATA_YAML = ROOT / "data" / "raw" / "coco-person" / "data.yaml"
PROJECT_DIR = ROOT / "models" / "segmentation"
RUN_NAME = "coco_person_yolov8n_seg_baseline"

HYPERPARAMS = dict(
    model="yolov8n-seg.pt",
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
