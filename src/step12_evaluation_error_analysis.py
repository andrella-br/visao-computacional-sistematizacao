"""Seleciona exemplos de falso positivo e falso negativo do detector no
conjunto de teste (por discrepancia de contagem de instancias por classe
entre ground-truth e predicao) e salva visualizacoes comentadas.

Uso:
    python src/step12_evaluation_error_analysis.py
"""

from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
DETECTION_WEIGHTS = ROOT / "models" / "detection" / "css_yolov8n_baseline" / "weights" / "best.pt"
IMAGES_DIR = ROOT / "data" / "raw" / "construction-site-safety" / "images"
LABELS_DIR = ROOT / "data" / "raw" / "construction-site-safety" / "labels"
TEST_LIST = ROOT / "data" / "splits" / "construction-site-safety" / "test.txt"
FIGURES_DIR = ROOT / "reports" / "figures"

CLASS_NAMES = [
    "Hardhat", "Mask", "NO-Hardhat", "NO-Mask", "NO-Safety Vest",
    "Person", "Safety Cone", "Safety Vest", "machinery", "vehicle",
]
CONF_THRESHOLD = 0.25
N_EXAMPLES_EACH = 2


def read_gt_classes(label_path):
    if not label_path.exists():
        return Counter()
    counts = Counter()
    for line in label_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            counts[int(line.split()[0])] += 1
    return counts


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    model = YOLO(str(DETECTION_WEIGHTS))

    test_names = [n.strip() for n in TEST_LIST.read_text(encoding="utf-8").splitlines() if n.strip()]

    fn_candidates = []  # (score, img_name, missing_classes)
    fp_candidates = []  # (score, img_name, extra_classes)

    for name in test_names:
        img_path = IMAGES_DIR / name
        label_path = LABELS_DIR / (Path(name).stem + ".txt")

        gt_counts = read_gt_classes(label_path)
        result = model.predict(source=str(img_path), conf=CONF_THRESHOLD, verbose=False)[0]
        pred_counts = Counter(int(c) for c in result.boxes.cls.tolist())

        missing = gt_counts - pred_counts  # presente no GT, faltando na predicao (FN)
        extra = pred_counts - gt_counts    # presente na predicao, ausente no GT (FP)

        if missing:
            fn_candidates.append((sum(missing.values()), name, missing))
        if extra:
            fp_candidates.append((sum(extra.values()), name, extra))

    fn_candidates.sort(key=lambda x: -x[0])
    fp_candidates.sort(key=lambda x: -x[0])

    examples = []
    for score, name, missing in fn_candidates[:N_EXAMPLES_EACH]:
        classes_str = ", ".join(f"{CLASS_NAMES[c]} x{n}" for c, n in missing.items())
        examples.append(("Falso Negativo", name, classes_str, score))
    for score, name, extra in fp_candidates[:N_EXAMPLES_EACH]:
        classes_str = ", ".join(f"{CLASS_NAMES[c]} x{n}" for c, n in extra.items())
        examples.append(("Falso Positivo", name, classes_str, score))

    for idx, (kind, name, classes_str, score) in enumerate(examples, start=1):
        img_path = IMAGES_DIR / name
        label_path = LABELS_DIR / (Path(name).stem + ".txt")

        gt_result_img = model.predict(source=str(img_path), conf=CONF_THRESHOLD, verbose=False)[0].plot()

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        axes[0].imshow(Image.open(img_path))
        axes[0].set_title(f"Original ({name})")
        axes[0].axis("off")

        axes[1].imshow(gt_result_img[:, :, ::-1])
        axes[1].set_title(f"Predição do modelo (conf>={CONF_THRESHOLD})")
        axes[1].axis("off")

        fig.suptitle(f"{kind}: {classes_str}", fontsize=12)
        plt.tight_layout()
        out_path = FIGURES_DIR / f"erro_{idx}_{kind.lower().replace(' ', '_')}.png"
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        print(f"{kind} salvo: {out_path} — {classes_str}")


if __name__ == "__main__":
    main()
