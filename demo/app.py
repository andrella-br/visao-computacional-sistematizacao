"""Demo interativa (Gradio) do sistema de deteccao de EPIs + segmentacao de
pessoas. Publicada como Hugging Face Space.

Espera os pesos em:
    detection_best.pt      (detector YOLOv8n, 10 classes de EPI)
    segmentation_best.pt   (segmentador YOLOv8n-seg, classe person)
"""

import tempfile
from pathlib import Path

import cv2
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
MODEL_LABELS = {"Detecção de EPIs": "detector", "Segmentação de pessoas": "segmentador"}

detector = YOLO(str(DETECTION_WEIGHTS))
segmenter = YOLO(str(SEGMENTATION_WEIGHTS))


def analisar_imagem(imagem):
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


def analisar_video(video_path, modelo_escolhido, progress=gr.Progress()):
    if video_path is None:
        return None, "Envie um vídeo de um canteiro de obra."

    model = detector if MODEL_LABELS[modelo_escolhido] == "detector" else segmenter

    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) or None

    out_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    writer = cv2.VideoWriter(out_path, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

    violacoes_encontradas = set()
    frame_count = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        result = model.predict(frame, conf=CONF_THRESHOLD, verbose=False)[0]
        writer.write(result.plot())

        if MODEL_LABELS[modelo_escolhido] == "detector":
            for cls_id in result.boxes.cls.tolist():
                nome = CLASS_NAMES[int(cls_id)]
                if nome in VIOLATION_CLASSES:
                    violacoes_encontradas.add(nome)

        frame_count += 1
        if total_frames:
            progress(frame_count / total_frames, desc=f"Processando quadro {frame_count}/{total_frames}")

    cap.release()
    writer.release()

    duracao = frame_count / fps if fps else 0
    if MODEL_LABELS[modelo_escolhido] == "detector":
        if violacoes_encontradas:
            resumo = (
                f"⚠️ Violações encontradas em algum momento do vídeo ({duracao:.1f}s, "
                f"{frame_count} quadros): " + ", ".join(sorted(violacoes_encontradas))
            )
        else:
            resumo = f"✅ Nenhuma violação de EPI detectada no vídeo ({duracao:.1f}s, {frame_count} quadros)."
    else:
        resumo = f"Segmentação de pessoas concluída ({duracao:.1f}s, {frame_count} quadros processados)."

    return out_path, resumo


DESCRICAO = """
Sistema de visão computacional para segurança do trabalho — projeto da
disciplina de Visão Computacional e Reconhecimento de Padrões.

Duas abas: **Imagem** (uma foto, resultado instantâneo com os dois modelos)
e **Vídeo** (processa quadro a quadro, pode levar alguns minutos
dependendo da duração e se há GPU disponível).

Repositório com o código completo, relatório técnico e notebooks:
ver descrição do Space.
"""

aba_imagem = gr.Interface(
    fn=analisar_imagem,
    inputs=gr.Image(type="numpy", label="Imagem do canteiro de obra"),
    outputs=[
        gr.Image(label="Detecção de EPIs (caixas)"),
        gr.Image(label="Segmentação de pessoas (máscaras)"),
        gr.Textbox(label="Resumo de conformidade"),
    ],
    examples=[str(p) for p in sorted((ROOT / "examples").glob("*.jpg"))] or None,
)

aba_video = gr.Interface(
    fn=analisar_video,
    inputs=[
        gr.Video(label="Vídeo do canteiro de obra"),
        gr.Radio(list(MODEL_LABELS), value="Detecção de EPIs", label="Modelo"),
    ],
    outputs=[
        gr.Video(label="Vídeo anotado"),
        gr.Textbox(label="Resumo"),
    ],
)

with gr.Blocks(title="🦺 Detecção de EPIs e Segmentação de Pessoas") as demo:
    gr.Markdown("# 🦺 Detecção de EPIs e Segmentação de Pessoas")
    gr.Markdown(DESCRICAO)
    gr.TabbedInterface([aba_imagem, aba_video], ["Imagem", "Vídeo"])

if __name__ == "__main__":
    demo.launch()
