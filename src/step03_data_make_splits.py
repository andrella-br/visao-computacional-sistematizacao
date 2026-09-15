"""Gera splits reprodutíveis (treino/validação/teste, 70/20/10, seed fixa)
para os subconjuntos já preparados em data/raw/, salvando listas de arquivos
(um nome por linha) em data/splits/<fonte>/{train,val,test}.txt.

Uso:
    python src/step03_data_make_splits.py
"""

import random
from pathlib import Path

SEED = 42
RATIOS = {"train": 0.7, "val": 0.2, "test": 0.1}

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    "construction-site-safety": ROOT / "data" / "raw" / "construction-site-safety" / "images",
    "coco-person": ROOT / "data" / "raw" / "coco-person" / "images",
}
SPLITS_ROOT = ROOT / "data" / "splits"


def split_list(files, ratios, seed):
    files = sorted(files)
    rng = random.Random(seed)
    rng.shuffle(files)
    n = len(files)
    n_train = int(n * ratios["train"])
    n_val = int(n * ratios["val"])
    return {
        "train": files[:n_train],
        "val": files[n_train : n_train + n_val],
        "test": files[n_train + n_val :],
    }


def main():
    for source_name, images_dir in SOURCES.items():
        if not images_dir.exists():
            print(f"[aviso] pasta nao encontrada, pulando: {images_dir}")
            continue
        files = [p.name for p in images_dir.iterdir() if p.is_file()]
        splits = split_list(files, RATIOS, SEED)

        out_dir = SPLITS_ROOT / source_name
        out_dir.mkdir(parents=True, exist_ok=True)
        for split_name, split_files in splits.items():
            out_path = out_dir / f"{split_name}.txt"
            with open(out_path, "w", encoding="utf-8") as f:
                f.write("\n".join(split_files) + "\n")

        print(f"{source_name}: total={len(files)} "
              f"train={len(splits['train'])} val={len(splits['val'])} test={len(splits['test'])} "
              f"(seed={SEED})")


if __name__ == "__main__":
    main()
