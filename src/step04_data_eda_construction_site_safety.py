"""Analise exploratoria (EDA) do subconjunto Construction Site Safety:
contagem de instancias por classe, distribuicao de resolucao e brilho medio
(proxy de condicao de iluminacao). Salva graficos em reports/figures/ e um
resumo em texto.

Uso:
    python src/step04_data_eda_construction_site_safety.py
"""

from collections import Counter
from pathlib import Path

from PIL import Image
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "raw" / "construction-site-safety"
IMAGES_DIR = DATA_DIR / "images"
LABELS_DIR = DATA_DIR / "labels"
FIGURES_DIR = ROOT / "reports" / "figures"

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


def count_instances_per_class():
    counts = Counter()
    for label_path in LABELS_DIR.glob("*.txt"):
        with open(label_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                cls_id = int(line.split()[0])
                counts[cls_id] += 1
    return counts


def sample_resolutions_and_brightness(sample_size=100):
    image_paths = sorted(IMAGES_DIR.iterdir())[:sample_size]
    resolutions = []
    brightness = []
    for p in image_paths:
        try:
            with Image.open(p) as img:
                resolutions.append(img.size)
                gray = img.convert("L")
                pixels = list(gray.getdata())
                brightness.append(sum(pixels) / len(pixels))
        except Exception as e:
            print(f"[aviso] falha ao ler {p.name}: {e}")
    return resolutions, brightness


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Contagem de instancias por classe
    counts = count_instances_per_class()
    total_instances = sum(counts.values())
    print("Instancias por classe:")
    for cls_id, name in enumerate(CLASS_NAMES):
        n = counts.get(cls_id, 0)
        pct = (n / total_instances * 100) if total_instances else 0
        print(f"  {name}: {n} ({pct:.1f}%)")

    fig, ax = plt.subplots(figsize=(10, 5))
    names = CLASS_NAMES
    values = [counts.get(i, 0) for i in range(len(CLASS_NAMES))]
    ax.bar(names, values, color="#4C72B0")
    ax.set_ylabel("Numero de instancias")
    ax.set_title("Instancias por classe - Construction Site Safety (subconjunto)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "css_instances_per_class.png", dpi=150)
    plt.close(fig)

    # 2. Resolucao e brilho (proxy de iluminacao) em uma amostra
    resolutions, brightness = sample_resolutions_and_brightness(sample_size=150)
    widths = [w for w, h in resolutions]
    heights = [h for w, h in resolutions]

    print(f"\nResolucao (amostra de {len(resolutions)} imagens):")
    if widths:
        print(f"  largura: min={min(widths)} max={max(widths)} media={sum(widths)/len(widths):.0f}")
        print(f"  altura:  min={min(heights)} max={max(heights)} media={sum(heights)/len(heights):.0f}")
    if brightness:
        print(f"  brilho medio (0-255): min={min(brightness):.1f} max={max(brightness):.1f} "
              f"media={sum(brightness)/len(brightness):.1f}")

    fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].hist(widths, bins=20, color="#55A868")
    axes[0].set_title("Distribuicao de largura (px)")
    axes[1].hist(brightness, bins=20, color="#C44E52")
    axes[1].set_title("Distribuicao de brilho medio (proxy de iluminacao)")
    plt.tight_layout()
    fig.savefig(FIGURES_DIR / "css_resolution_brightness.png", dpi=150)
    plt.close(fig)

    # 3. Desbalanceamento
    max_class = max(counts, key=counts.get)
    min_class = min(range(len(CLASS_NAMES)), key=lambda i: counts.get(i, 0))
    ratio = counts[max_class] / max(counts.get(min_class, 1), 1)
    print(f"\nDesbalanceamento: classe mais frequente = {CLASS_NAMES[max_class]} "
          f"({counts[max_class]} instancias); classe menos frequente = "
          f"{CLASS_NAMES[min_class]} ({counts.get(min_class, 0)} instancias); "
          f"razao aproximada = {ratio:.1f}x")

    print(f"\nGraficos salvos em: {FIGURES_DIR}")


if __name__ == "__main__":
    main()
