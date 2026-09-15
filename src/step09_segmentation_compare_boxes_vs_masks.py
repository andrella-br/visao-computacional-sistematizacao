"""Compara visualmente as caixas do detector da Fase 2 (classe Person) com
as mascaras do segmentador da Fase 3 (classe person), rodando os dois
modelos sobre as MESMAS imagens do dataset de canteiro de obra (Fase 2) que
contem pessoas.

Uso:
    python src/step09_segmentation_compare_boxes_vs_masks.py
"""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]
DETECTION_WEIGHTS = ROOT / "models" / "detection" / "css_yolov8n_baseline" / "weights" / "best.pt"
SEGMENTATION_WEIGHTS = ROOT / "models" / "segmentation" / "coco_person_yolov8n_seg_baseline" / "weights" / "best.pt"
CSS_IMAGES_DIR = ROOT / "data" / "raw" / "construction-site-safety" / "images"
CSS_LABELS_DIR = ROOT / "data" / "raw" / "construction-site-safety" / "labels"
FIGURES_DIR = ROOT / "reports" / "figures"

PERSON_CLASS_ID_DETECTION = 5  # indice da classe "Person" no dataset de EPIs
NUM_EXAMPLES = 2
CROPS_DIR = FIGURES_DIR / "_crops"

# NOTA: boa parte do dataset Construction Site Safety (versao exportada) e
# composta por imagens-mosaico 2x2 (4 fotos combinadas numa so), achado
# documentado em reports/deteccao-fase2.md. Para uma comparacao visual legivel,
# usamos recortes de um unico quadrante (contendo uma pessoa) em vez da
# imagem mosaico inteira.
CROP_EXAMPLES = [
    # (arquivo fonte no dataset, quadrante: "tl"/"tr"/"bl"/"br")
    ("image_1004_jpg.rf.de519703cdcdd06d06edd7cfa60b8184.jpg", "bl"),
    ("-1670-_png_jpg.rf.0463edb430019e01ec79eed27a6349d6.jpg", "tl"),
]


def crop_quadrant(img_path, quadrant, out_path):
    img = Image.open(img_path)
    w, h = img.size
    boxes = {
        "tl": (0, 0, w // 2, h // 2),
        "tr": (w // 2, 0, w, h // 2),
        "bl": (0, h // 2, w // 2, h),
        "br": (w // 2, h // 2, w, h),
    }
    img.crop(boxes[quadrant]).save(out_path)


def find_images_with_person(n):
    """Recorta quadrantes de imagens-mosaico que contem uma pessoa, para
    uma comparacao visual legivel (ver CROP_EXAMPLES)."""
    CROPS_DIR.mkdir(parents=True, exist_ok=True)
    selected = []
    for filename, quadrant in CROP_EXAMPLES[:n]:
        src = CSS_IMAGES_DIR / filename
        out_path = CROPS_DIR / f"{Path(filename).stem}_{quadrant}.jpg"
        crop_quadrant(src, quadrant, out_path)
        selected.append(out_path)
    return selected


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    detector = YOLO(str(DETECTION_WEIGHTS))
    segmenter = YOLO(str(SEGMENTATION_WEIGHTS))

    images = find_images_with_person(NUM_EXAMPLES)
    print(f"Imagens selecionadas (contem Person): {len(images)}")

    for idx, img_path in enumerate(images, start=1):
        det_result = detector.predict(source=str(img_path), conf=0.25, verbose=False)[0]
        seg_result = segmenter.predict(source=str(img_path), conf=0.25, verbose=False)[0]

        det_img = det_result.plot()  # BGR numpy array com caixas desenhadas
        seg_img = seg_result.plot()  # BGR numpy array com mascaras desenhadas

        fig, axes = plt.subplots(1, 3, figsize=(18, 6))
        axes[0].imshow(Image.open(img_path))
        axes[0].set_title("Imagem original")
        axes[0].axis("off")

        axes[1].imshow(det_img[:, :, ::-1])  # BGR -> RGB
        axes[1].set_title("Detector Fase 2 (caixas, classe Person)")
        axes[1].axis("off")

        axes[2].imshow(seg_img[:, :, ::-1])
        axes[2].set_title("Segmentador Fase 3 (mascaras, classe person)")
        axes[2].axis("off")

        plt.tight_layout()
        out_path = FIGURES_DIR / f"boxes_vs_masks_example_{idx}.png"
        fig.savefig(out_path, dpi=150)
        plt.close(fig)
        print(f"Comparacao salva: {out_path}")


if __name__ == "__main__":
    main()
