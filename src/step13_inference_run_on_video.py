"""Roda o detector (Fase 2) e o segmentador (Fase 3) sobre o vídeo real do
cenário (video/input/video_final_canteiro_obra.mp4), salvando as saídas
anotadas em video/output/.

Uso:
    python src/step13_inference_run_on_video.py
"""

from pathlib import Path

from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
VIDEO_INPUT = ROOT / "video" / "input" / "video_final_canteiro_obra.mp4"
VIDEO_OUTPUT_DIR = ROOT / "video" / "output"

DETECTION_WEIGHTS = ROOT / "models" / "detection" / "css_yolov8n_baseline" / "weights" / "best.pt"
SEGMENTATION_WEIGHTS = ROOT / "models" / "segmentation" / "coco_person_yolov8n_seg_baseline" / "weights" / "best.pt"

CONF_THRESHOLD = 0.25


def run_inference(weights_path, run_name):
    model = YOLO(str(weights_path))
    model.predict(
        source=str(VIDEO_INPUT),
        conf=CONF_THRESHOLD,
        save=True,
        project=str(VIDEO_OUTPUT_DIR),
        name=run_name,
        exist_ok=True,
        verbose=False,
    )
    print(f"Inferencia concluida: {run_name}")


def main():
    print("=== Inferencia do detector (EPI) no video ===")
    run_inference(DETECTION_WEIGHTS, "deteccao_epi")

    print("\n=== Inferencia do segmentador (pessoas) no video ===")
    run_inference(SEGMENTATION_WEIGHTS, "segmentacao_pessoas")


if __name__ == "__main__":
    main()
