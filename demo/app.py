"""Demo interativa (Gradio) do sistema de deteccao de EPIs + segmentacao de
pessoas. Publicada como Hugging Face Space.

Espera os pesos em:
    detection_best.pt      (detector YOLOv8n, 10 classes de EPI)
    segmentation_best.pt   (segmentador YOLOv8n-seg, classe person)
"""

from pathlib import Path

import gradio as gr
from ultralytics import YOLO

ROOT = Path(__file__).resolve().parent
DETECTION_WEIGHTS = ROOT / "detection_best.pt"
SEGMENTATION_WEIGHTS = ROOT / "segmentation_best.pt"
CONF_THRESHOLD = 0.25

CLASS_NAMES = [
    "Hardhat", "Mask", "NO-Hardhat", "NO-Mask", "NO-Safety Vest",
    "Person", "Safety Cone", "Safety Vest", "machinery", "vehicle",
]
VIOLATION_CLASSES = {"NO-Hardhat", "NO-Mask", "NO-Safety Vest"}

detector = YOLO(str(DETECTION_WEIGHTS))
segmenter = YOLO(str(SEGMENTATION_WEIGHTS))


def analisar(imagem):
    if imagem is None:
        return None, None, "Envie uma imagem de um canteiro de obra."

    det_result = detector.predict(imagem, conf=CONF_THRESHOLD, verbose=False)[0]
    seg_result = segmenter.predict(imagem, conf=CONF_THRESHOLD, verbose=False)[0]

    det_img = det_result.plot()[:, :, ::-1]
    seg_img = seg_result.plot()[:, :, ::-1]

    violacoes = sorted({
        CLASS_NAMES[int(cls_id)]
        for cls_id in det_result.boxes.cls.tolist()
        if CLASS_NAMES[int(cls_id)] in VIOLATION_CLASSES
    })

    if violacoes:
        resumo = "⚠️ Violações de EPI detectadas: " + ", ".join(violacoes)
    else:
        resumo = "✅ Nenhuma violação de EPI detectada nesta imagem."

    return det_img, seg_img, resumo


DESCRICAO = """
Sistema de visão computacional para segurança do trabalho — projeto da
disciplina de Visão Computacional e Reconhecimento de Padrões.

Envie uma foto de um canteiro de obra: o **detector** (YOLOv8n) identifica
o uso/ausência de capacete, colete e máscara; o **segmentador** (YOLOv8n-seg)
destaca a silhueta das pessoas na cena.

Repositório com o código completo, relatório técnico e notebooks:
ver descrição do Space.
"""

demo = gr.Interface(
    fn=analisar,
    inputs=gr.Image(type="numpy", label="Imagem do canteiro de obra"),
    outputs=[
        gr.Image(label="Detecção de EPIs (caixas)"),
        gr.Image(label="Segmentação de pessoas (máscaras)"),
        gr.Textbox(label="Resumo de conformidade"),
    ],
    title="🦺 Detecção de EPIs e Segmentação de Pessoas",
    description=DESCRICAO,
    examples=[
        str(p) for p in sorted((ROOT / "examples").glob("*.jpg"))
    ] or None,
)

if __name__ == "__main__":
    demo.launch()
