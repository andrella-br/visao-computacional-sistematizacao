"""Converte as anotacoes COCO (poligonos) do subconjunto coco-person (Fase 1)
para o formato YOLO-seg (label .txt por imagem: classe + poligono
normalizado), reaproveitando os splits reprodutiveis ja definidos, e gera o
data.yaml no formato Ultralytics.

Uso:
    python src/step07_segmentation_prepare_yolo_config.py
"""

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "data" / "raw" / "coco-person"
ANNOTATIONS_PATH = DATASET_DIR / "instances_person_subset.json"
SPLITS_DIR = ROOT / "data" / "splits" / "coco-person"
IMAGES_DIR = DATASET_DIR / "images"
LABELS_DIR = DATASET_DIR / "labels"

CLASS_ID = 0  # unica classe: person


def polygon_to_yolo_seg(segmentation, img_w, img_h):
    """Converte uma lista de poligonos COCO (pixel) em linhas YOLO-seg
    normalizadas (0-1). Poligonos com menos de 3 pontos sao descartados."""
    lines = []
    for poly in segmentation:
        if len(poly) < 6:  # menos de 3 pontos (x,y)
            continue
        norm = []
        for i in range(0, len(poly), 2):
            x = poly[i] / img_w
            y = poly[i + 1] / img_h
            norm.append(f"{x:.6f}")
            norm.append(f"{y:.6f}")
        lines.append(f"{CLASS_ID} " + " ".join(norm))
    return lines


def main():
    with open(ANNOTATIONS_PATH, "r", encoding="utf-8") as f:
        coco = json.load(f)

    images_by_id = {img["id"]: img for img in coco["images"]}
    anns_by_image = defaultdict(list)
    for ann in coco["annotations"]:
        anns_by_image[ann["image_id"]].append(ann)

    LABELS_DIR.mkdir(parents=True, exist_ok=True)

    total_labels_written = 0
    total_polygons = 0
    for img_id, anns in anns_by_image.items():
        img = images_by_id[img_id]
        w, h = img["width"], img["height"]
        stem = Path(img["file_name"]).stem
        label_path = LABELS_DIR / f"{stem}.txt"

        lines = []
        for ann in anns:
            lines.extend(polygon_to_yolo_seg(ann["segmentation"], w, h))

        if lines:
            with open(label_path, "w", encoding="utf-8") as f:
                f.write("\n".join(lines) + "\n")
            total_labels_written += 1
            total_polygons += len(lines)

    print(f"Labels YOLO-seg escritos: {total_labels_written} (poligonos totais: {total_polygons})")

    # Gera train.txt / val.txt / test.txt (caminhos absolutos das imagens)
    for split in ["train", "val", "test"]:
        manifest = SPLITS_DIR / f"{split}.txt"
        filenames = [
            line.strip() for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()
        ]
        out_path = DATASET_DIR / f"{split}.txt"
        with open(out_path, "w", encoding="utf-8") as f:
            for name in filenames:
                f.write((IMAGES_DIR / name).as_posix() + "\n")
        print(f"{split}: {len(filenames)} imagens -> {out_path}")

    data_yaml = DATASET_DIR / "data.yaml"
    with open(data_yaml, "w", encoding="utf-8") as f:
        f.write(f"path: {DATASET_DIR.as_posix()}\n")
        f.write("train: train.txt\n")
        f.write("val: val.txt\n")
        f.write("test: test.txt\n")
        f.write("nc: 1\n")
        f.write("names: ['person']\n")

    print(f"data.yaml (Ultralytics, segmentacao) escrito em: {data_yaml}")


if __name__ == "__main__":
    main()
