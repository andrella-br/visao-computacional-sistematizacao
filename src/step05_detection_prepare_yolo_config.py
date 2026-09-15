"""Gera as listas de caminhos de imagem (train/val/test) e o data.yaml no
formato Ultralytics YOLO, a partir dos manifests de split já gerados na
Fase 1 (data/splits/construction-site-safety/{train,val,test}.txt).

Uso:
    python src/step05_detection_prepare_yolo_config.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATASET_DIR = ROOT / "data" / "raw" / "construction-site-safety"
SPLITS_DIR = ROOT / "data" / "splits" / "construction-site-safety"

CLASS_NAMES = [
    "Hardhat",
    "Mask",
    "NO-Hardhat",
    "NO-Mask",
    "NO-Safety Vest",
    "Person",
    "Safety Cone",
    "Safety Vest",
    "machinery",
    "vehicle",
]


def main():
    for split in ["train", "val", "test"]:
        manifest = SPLITS_DIR / f"{split}.txt"
        filenames = [
            line.strip() for line in manifest.read_text(encoding="utf-8").splitlines() if line.strip()
        ]
        out_path = DATASET_DIR / f"{split}.txt"
        images_dir = DATASET_DIR / "images"
        with open(out_path, "w", encoding="utf-8") as f:
            for name in filenames:
                f.write((images_dir / name).as_posix() + "\n")
        print(f"{split}: {len(filenames)} imagens -> {out_path}")

    data_yaml = DATASET_DIR / "data.yaml"
    with open(data_yaml, "w", encoding="utf-8") as f:
        f.write(f"path: {DATASET_DIR.as_posix()}\n")
        f.write("train: train.txt\n")
        f.write("val: val.txt\n")
        f.write("test: test.txt\n")
        f.write(f"nc: {len(CLASS_NAMES)}\n")
        f.write(f"names: {CLASS_NAMES}\n")

    print(f"data.yaml (Ultralytics) escrito em: {data_yaml}")


if __name__ == "__main__":
    main()
