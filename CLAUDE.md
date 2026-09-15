# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project status

Phase 1 (scenario + dataset definition) is complete. Scenario: worker safety
(PPE detection + person segmentation). No detector/segmentation model has
been trained yet — that starts in Phase 2.

Planning follows the [OpenSpec](https://github.com/Fission-AI/OpenSpec)
pattern (`openspec/` directory, `.claude/commands/opsx/*`): each roadmap
phase (see `docs/roadmap.md`) becomes its own OpenSpec change under
`openspec/changes/` with a proposal, specs, and tasks before implementation.

## Commands

```bash
# Create and activate the project-local virtual environment (once)
python -m venv .venv
source .venv/Scripts/activate   # Windows/Git Bash
# source .venv/bin/activate     # Linux/Mac
pip install -r requirements.txt

# Run pipeline scripts in execution order (see "Code layout" below)
python src/step01_data_prepare_construction_site_safety.py
python src/step02_data_prepare_coco_person_subset.py
python src/step03_data_make_splits.py
python src/step04_data_eda_construction_site_safety.py
```

There is no lint/test suite yet — this is a data-science/notebook-driven
project; validation happens via each script's printed checks and the
OpenSpec task checklists in `openspec/changes/archive/`.

## Code layout

`src/` is **flat, not organized by task**. Scripts are named
`stepNN_<fase>_<descrição>.py`: `NN` is the two-digit global execution order
across the whole project lifecycle, and `<fase>` tags which roadmap phase the
script belongs to (`data`, `detection`, `segmentation`, `evaluation`,
`inference`) — replacing what used to be `src/detection/`, `src/segmentation/`
etc. subfolders. Current scripts (Phase 1 / `data`): `step01`-`step04`. Phase
2 scripts continue the numbering with the `detection` tag (e.g.
`step05_detection_train_yolo.py`), Phase 3 with `segmentation`, and so on —
this naming convention is an explicit project decision (see
`openspec/specs/project-scaffolding/spec.md`).

Data flow: `data/raw/<source>/` (downloaded/sampled by step01-02, gitignored)
→ `data/splits/<source>/{train,val,test}.txt` (file-name manifests, seed=42,
versioned) → model training scripts (Phase 2+) read the manifests to build
train/val/test sets. `reports/figures/` and `reports/*.md` hold EDA/analysis
outputs referenced by the technical report.

## What this project is

Graduate coursework (Pós-graduação · Visão Computacional e Reconhecimento de
Padrões, Prof. Romes Heriberto) requiring a group to build, end-to-end, a
computer vision system that both **detects** and **segments** objects in
images from a chosen real-world domain, then demonstrates it on video.

Group picks one scenario (or proposes an approved custom one):
- Worker safety — PPE detection (helmet, vest) + person segmentation on
  construction sites
- Agribusiness — detection/segmentation of cattle, fruit, or pests for
  counting/monitoring
- Smart cities — potholes, parking spaces, or urban traffic analysis
- Retail — product detection/segmentation on shelves (planogram audit)
- Free scenario — any real detection + segmentation problem, pending
  professor approval in Phase 1

## Minimum technical requirements

- **Dataset**: ≥300 annotated images from the chosen domain. Public sources
  (Roboflow Universe, Kaggle, COCO subset) must be cited; self-annotated
  data uses CVAT, Label Studio, or Roboflow. Split into train/val/test.
- **Detection**: fine-tune a modern detector — YOLO (Ultralytics) or Faster
  R-CNN (torchvision).
- **Segmentation**: instance segmentation (YOLO-seg or Mask R-CNN) or
  semantic segmentation (DeepLab / U-Net) on the same domain.
- **Evaluation**: mAP@0.5 and mAP@0.5:0.95, IoU, precision/recall, confusion
  matrix, plus qualitative error analysis (annotated false positive/negative
  examples).
- **Video**: run inference on a real video from the scenario (≥30 seconds).
- **Bonus** (up to +0.5, capped at max grade): object tracking in video
  (ByteTrack or DeepSORT), or an interactive demo (Gradio / Hugging Face
  Spaces).

Suggested tooling: Google Colab (GPU), PyTorch/torchvision, Ultralytics
YOLO, OpenCV, CVAT/Label Studio/Roboflow for annotation, `supervision` for
visualization, GitHub for version control.

## Roadmap (phases)

1. **Definition and data** — form group, pick scenario/dataset, run EDA
   (per-class counts, resolution, lighting, imbalance), submit a 1-page
   proposal.
2. **Detection baseline** — prepare data (YOLO or COCO format, fixed seeded
   splits), fine-tune detector on Colab GPU, log training curves and
   validation metrics, document hyperparameters (epochs, image size, batch,
   augmentation).
3. **Segmentation** — train/adapt a segmentation model on the same domain;
   compare boxes vs. masks qualitatively; revisit annotations if needed.
4. **Evaluation and video** — full evaluation on the held-out test set (mAP,
   IoU, precision/recall, confusion matrix), commented error analysis, video
   inference run and recorded.
5. **Delivery and presentation** — finalize technical report, organize the
   GitHub repo (README with reproduction instructions), record the pitch
   video, submit via Moodle.

## Deliverables

1. Technical report README (PDF or MD, 6–10 pages): problem/scenario ·
   dataset & EDA · methodology (models, hyperparameters) · results/metrics ·
   error analysis · limitations & next steps.
2. GitHub repository: organized code + README with reproduction
   instructions and dataset link.
3. Executable Colab notebook: training, evaluation, and inference cells
   with visible outputs.
4. 5–8 min pitch video (unlisted YouTube or Google Drive) with all group
   members participating, demonstrating the working system including video
   inference.

Academic integrity: cite third-party datasets/code. Generative AI use is
allowed as support but must be declared in the report (where/how it was
used).

