"""Avaliacao completa no conjunto de TESTE (nunca visto em treino/validacao)
dos dois modelos treinados (detector da Fase 2, segmentador da Fase 3):
mAP@0.5, mAP@0.5:0.95, precisao, recall, matriz de confusao, e IoU medio das
predicoes corretamente casadas (TP) do detector.

Uso:
    python src/step11_evaluation_test_set.py
"""

import json
from pathlib import Path

from ultralytics import YOLO
from ultralytics.utils.metrics import box_iou
import torch

ROOT = Path(__file__).resolve().parents[1]

DETECTION_WEIGHTS = ROOT / "models" / "detection" / "css_yolov8n_baseline" / "weights" / "best.pt"
DETECTION_DATA_YAML = ROOT / "data" / "raw" / "construction-site-safety" / "data.yaml"
DETECTION_LABELS_DIR = ROOT / "data" / "raw" / "construction-site-safety" / "labels"
DETECTION_TEST_LIST = ROOT / "data" / "splits" / "construction-site-safety" / "test.txt"

SEGMENTATION_WEIGHTS = ROOT / "models" / "segmentation" / "coco_person_yolov8n_seg_baseline" / "weights" / "best.pt"
SEGMENTATION_DATA_YAML = ROOT / "data" / "raw" / "coco-person" / "data.yaml"

RESULTS_DIR = ROOT / "reports" / "test-evaluation"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

CONF_THRESHOLD = 0.25
IOU_MATCH_THRESHOLD = 0.5


def summarize_val_metrics(results):
    return {
        "precision": float(results.box.mp),
        "recall": float(results.box.mr),
        "mAP50": float(results.box.map50),
        "mAP50-95": float(results.box.map),
    }


def compute_mean_iou_detection():
    """Roda o detector no conjunto de teste, casa cada predicao com a caixa
    de mesma classe com maior IoU no ground-truth, e retorna o IoU medio dos
    pares casados (TP) com confianca >= CONF_THRESHOLD."""
    model = YOLO(str(DETECTION_WEIGHTS))
    test_images = [
        ROOT / "data" / "raw" / "construction-site-safety" / "images" / name
        for name in DETECTION_TEST_LIST.read_text(encoding="utf-8").splitlines()
        if name.strip()
    ]

    ious = []
    for img_path in test_images:
        result = model.predict(source=str(img_path), conf=CONF_THRESHOLD, verbose=False)[0]
        pred_boxes = result.boxes.xyxy
        pred_classes = result.boxes.cls

        label_path = DETECTION_LABELS_DIR / (img_path.stem + ".txt")
        if not label_path.exists() or len(pred_boxes) == 0:
            continue

        img_w, img_h = result.orig_shape[1], result.orig_shape[0]
        gt_boxes = []
        gt_classes = []
        for line in label_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            parts = line.split()
            cls_id = int(parts[0])
            cx, cy, bw, bh = (float(x) for x in parts[1:5])
            x1 = (cx - bw / 2) * img_w
            y1 = (cy - bh / 2) * img_h
            x2 = (cx + bw / 2) * img_w
            y2 = (cy + bh / 2) * img_h
            gt_boxes.append([x1, y1, x2, y2])
            gt_classes.append(cls_id)

        if not gt_boxes:
            continue

        gt_boxes_t = torch.tensor(gt_boxes)
        gt_classes_t = torch.tensor(gt_classes)
        iou_matrix = box_iou(pred_boxes, gt_boxes_t)

        for i in range(len(pred_boxes)):
            same_class = gt_classes_t == pred_classes[i].item()
            if not same_class.any():
                continue
            candidate_ious = iou_matrix[i][same_class]
            best_iou = candidate_ious.max().item()
            if best_iou >= IOU_MATCH_THRESHOLD:
                ious.append(best_iou)

    return sum(ious) / len(ious) if ious else 0.0, len(ious)


def main():
    summary = {}

    print("=== Avaliando detector (Fase 2) no conjunto de TESTE ===")
    det_model = YOLO(str(DETECTION_WEIGHTS))
    det_results = det_model.val(
        data=str(DETECTION_DATA_YAML),
        split="test",
        project=str(RESULTS_DIR),
        name="detection_test",
        exist_ok=True,
    )
    summary["detection"] = summarize_val_metrics(det_results)

    print("\n=== Calculando IoU medio (TP) do detector no conjunto de TESTE ===")
    mean_iou, n_matched = compute_mean_iou_detection()
    summary["detection"]["mean_iou_tp"] = mean_iou
    summary["detection"]["n_matched_boxes"] = n_matched
    print(f"IoU medio (predicoes casadas, conf>={CONF_THRESHOLD}): {mean_iou:.4f} (n={n_matched})")

    print("\n=== Avaliando segmentador (Fase 3) no conjunto de TESTE ===")
    seg_model = YOLO(str(SEGMENTATION_WEIGHTS))
    seg_results = seg_model.val(
        data=str(SEGMENTATION_DATA_YAML),
        split="test",
        project=str(RESULTS_DIR),
        name="segmentation_test",
        exist_ok=True,
    )
    summary["segmentation"] = {
        "box_precision": float(seg_results.box.mp),
        "box_recall": float(seg_results.box.mr),
        "box_mAP50": float(seg_results.box.map50),
        "box_mAP50-95": float(seg_results.box.map),
        "mask_precision": float(seg_results.seg.mp),
        "mask_recall": float(seg_results.seg.mr),
        "mask_mAP50": float(seg_results.seg.map50),
        "mask_mAP50-95": float(seg_results.seg.map),
    }

    summary_path = RESULTS_DIR / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"\nResumo salvo em: {summary_path}")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
