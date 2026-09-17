"""Seleciona um subconjunto reprodutivel (~300-400 imagens) do dataset
"Construction Site Safety" (formato YOLO, baixado do Kaggle) por amostragem
estratificada por classe, garantindo que todas as 10 classes apareçam no
subconjunto, e copia imagens + labels para data/raw/construction-site-safety/.

Uso:
    python src/step01_data_prepare_construction_site_safety.py
"""

import random
import shutil
import subprocess
import sys
import tempfile
from collections import defaultdict
from pathlib import Path

SEED = 42
TARGET_TOTAL = 350
MIN_PER_CLASS = 15

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

KAGGLE_DATASET = "snehilsanyal/construction-site-safety-image-dataset-roboflow"
OUTPUT_ROOT = Path(__file__).resolve().parents[1] / "data" / "raw" / "construction-site-safety"


def download_kaggle_dataset(tmp_dir: Path) -> Path:
    """Baixa (uma unica vez) o dataset do Kaggle via CLI. Requer um token
    configurado em ~/.kaggle/access_token (kaggle.com/settings/api)."""
    css_data_dir = tmp_dir / "css-data"
    if css_data_dir.exists():
        return css_data_dir

    token_path = Path.home() / ".kaggle" / "access_token"
    if not token_path.exists():
        raise RuntimeError(
            f"Token do Kaggle nao encontrado em {token_path}. "
            "Configure-o (kaggle.com/settings/api) antes de rodar esta celula."
        )

    print("Baixando dataset 'Construction Site Safety' do Kaggle (~206MB)...")
    result = subprocess.run(
        [
            sys.executable, "-m", "kaggle", "datasets", "download",
            "-d", KAGGLE_DATASET,
            "-p", str(tmp_dir),
            "--unzip",
        ],
        capture_output=True,
        text=True,
    )
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(
            f"Falha ao baixar dataset do Kaggle (codigo {result.returncode}). "
            "Veja a mensagem de erro acima - geralmente e token invalido/expirado "
            "ou o dataset exige aceitar os termos de uso no site do Kaggle primeiro."
        )
    return css_data_dir


def read_classes_in_label(label_path: Path) -> set:
    classes = set()
    if not label_path.exists():
        return classes
    with open(label_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            cls_id = int(line.split()[0])
            classes.add(cls_id)
    return classes


def collect_pool(source_root: Path):
    pool = []
    for split in ["train", "valid", "test"]:
        images_dir = source_root / split / "images"
        labels_dir = source_root / split / "labels"
        if not images_dir.exists():
            continue
        for img_path in sorted(images_dir.iterdir()):
            if img_path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
                continue
            label_path = labels_dir / (img_path.stem + ".txt")
            classes = read_classes_in_label(label_path)
            pool.append((img_path, label_path, classes))
    return pool


def main():
    random.seed(SEED)

    tmp_dir = Path(tempfile.gettempdir()) / "css_kaggle_cache"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    source_root = download_kaggle_dataset(tmp_dir)

    pool = collect_pool(source_root)
    print(f"Total de imagens disponiveis na fonte: {len(pool)}")

    random.shuffle(pool)

    selected = []
    selected_paths = set()
    class_counts = defaultdict(int)

    # Passo 1: garantir cobertura minima de cada classe
    for cls_id in range(len(CLASS_NAMES)):
        for img_path, label_path, classes in pool:
            if img_path in selected_paths:
                continue
            if cls_id in classes and class_counts[cls_id] < MIN_PER_CLASS:
                selected.append((img_path, label_path, classes))
                selected_paths.add(img_path)
                for c in classes:
                    class_counts[c] += 1
            if class_counts[cls_id] >= MIN_PER_CLASS:
                break

    # Passo 2: completar ate o total alvo com amostragem aleatoria (seed fixa)
    for img_path, label_path, classes in pool:
        if len(selected) >= TARGET_TOTAL:
            break
        if img_path in selected_paths:
            continue
        selected.append((img_path, label_path, classes))
        selected_paths.add(img_path)
        for c in classes:
            class_counts[c] += 1

    print(f"Subconjunto selecionado: {len(selected)} imagens (seed={SEED})")
    print("Contagem de instancias-imagem por classe no subconjunto:")
    for cls_id, name in enumerate(CLASS_NAMES):
        print(f"  {name}: {class_counts.get(cls_id, 0)} imagens")

    images_out = OUTPUT_ROOT / "images"
    labels_out = OUTPUT_ROOT / "labels"
    images_out.mkdir(parents=True, exist_ok=True)
    labels_out.mkdir(parents=True, exist_ok=True)

    copied = 0
    for img_path, label_path, _ in selected:
        shutil.copy2(img_path, images_out / img_path.name)
        if label_path.exists():
            shutil.copy2(label_path, labels_out / label_path.name)
        copied += 1

    print(f"Imagens+labels copiados: {copied}")
    print("data.yaml (formato Ultralytics, com train/val/test) e escrito pelo step05, nao aqui.")


if __name__ == "__main__":
    main()
