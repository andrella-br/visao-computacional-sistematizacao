"""Seleciona um subconjunto reprodutível de imagens do COCO val2017 contendo a
categoria "person" (com máscaras de instância) e salva as imagens e um JSON de
anotações filtrado em data/raw/coco-person/.

Uso:
    python src/step02_data_prepare_coco_person_subset.py
"""

import json
import random
import urllib.request
from pathlib import Path

SEED = 42
TARGET_IMAGES = 300
ANNOTATIONS_PATH = Path(
    r"C:\Users\andre.luiz\AppData\Local\Temp\coco_tmp\annotations\instances_val2017.json"
)
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "data" / "raw" / "coco-person"
IMAGES_DIR = OUTPUT_DIR / "images"
COCO_IMAGE_BASE_URL = "http://images.cocodataset.org/val2017/"


def main():
    random.seed(SEED)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    with open(ANNOTATIONS_PATH, "r", encoding="utf-8") as f:
        coco = json.load(f)

    person_cat_id = next(
        c["id"] for c in coco["categories"] if c["name"] == "person"
    )

    images_by_id = {img["id"]: img for img in coco["images"]}

    person_anns_by_image = {}
    for ann in coco["annotations"]:
        if ann["category_id"] == person_cat_id and ann.get("iscrowd", 0) == 0:
            person_anns_by_image.setdefault(ann["image_id"], []).append(ann)

    eligible_image_ids = [
        img_id for img_id, anns in person_anns_by_image.items() if len(anns) >= 1
    ]
    eligible_image_ids.sort()
    random.shuffle(eligible_image_ids)

    selected_ids = sorted(eligible_image_ids[:TARGET_IMAGES])
    print(f"Imagens elegiveis (com pessoa e mascara): {len(eligible_image_ids)}")
    print(f"Selecionadas (seed={SEED}): {len(selected_ids)}")

    selected_images = [images_by_id[i] for i in selected_ids]
    selected_annotations = [
        ann for i in selected_ids for ann in person_anns_by_image[i]
    ]

    subset = {
        "info": coco.get("info", {}),
        "licenses": coco.get("licenses", []),
        "categories": [c for c in coco["categories"] if c["id"] == person_cat_id],
        "images": selected_images,
        "annotations": selected_annotations,
    }

    subset_path = OUTPUT_DIR / "instances_person_subset.json"
    with open(subset_path, "w", encoding="utf-8") as f:
        json.dump(subset, f)
    print(f"Anotacoes filtradas salvas em: {subset_path}")

    total_instances = len(selected_annotations)
    print(f"Total de instancias de pessoa no subconjunto: {total_instances}")

    downloaded = 0
    for img in selected_images:
        dest = IMAGES_DIR / img["file_name"]
        if dest.exists():
            downloaded += 1
            continue
        url = COCO_IMAGE_BASE_URL + img["file_name"]
        try:
            urllib.request.urlretrieve(url, dest)
            downloaded += 1
        except Exception as e:
            print(f"Falha ao baixar {img['file_name']}: {e}")

    print(f"Imagens baixadas: {downloaded}/{len(selected_images)}")


if __name__ == "__main__":
    main()
