"""Concatena os clipes de vídeo baixados em video/input/ em um único vídeo
contínuo (>= 30s), padronizando resolução (1280x720, letterbox para os
clipes em retrato) e taxa de quadros (25fps), para uso na inferência da
Fase 4.

Uso:
    python src/step10_inference_concat_videos.py
"""

from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
INPUT_DIR = ROOT / "video" / "input"
OUTPUT_PATH = INPUT_DIR / "video_final_canteiro_obra.mp4"

# Ordem de concatenação: paisagem primeiro (mais parecido com o dataset de
# treino), depois os dois clipes em retrato.
SOURCE_ORDER = [
    "19832492-hd_1280_720_25fps.mp4",
    "14626383_720_1280_30fps.mp4",
    "15518317_720_1280_60fps.mp4",
]

TARGET_W, TARGET_H = 1280, 720
TARGET_FPS = 25.0


def letterbox(frame, target_w, target_h):
    h, w = frame.shape[:2]
    scale = min(target_w / w, target_h / h)
    new_w, new_h = int(w * scale), int(h * scale)
    resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
    canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
    x_off = (target_w - new_w) // 2
    y_off = (target_h - new_h) // 2
    canvas[y_off : y_off + new_h, x_off : x_off + new_w] = resized
    return canvas


def main():
    writer = cv2.VideoWriter(
        str(OUTPUT_PATH),
        cv2.VideoWriter_fourcc(*"mp4v"),
        TARGET_FPS,
        (TARGET_W, TARGET_H),
    )

    total_frames_written = 0
    for filename in SOURCE_ORDER:
        src_path = INPUT_DIR / filename
        cap = cv2.VideoCapture(str(src_path))
        src_fps = cap.get(cv2.CAP_PROP_FPS) or TARGET_FPS
        src_frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        # Reamostragem simples de taxa de quadros: escolhe os indices de
        # frame mais proximos para bater com TARGET_FPS.
        duration = src_frame_count / src_fps
        n_target_frames = int(duration * TARGET_FPS)
        src_indices = [int(i * src_fps / TARGET_FPS) for i in range(n_target_frames)]

        frames_written_this_clip = 0
        idx_set = sorted(set(src_indices))
        idx_to_frame = {}
        current_idx = -1
        for target_idx in src_indices:
            if target_idx not in idx_to_frame:
                while current_idx < target_idx:
                    ok, frame = cap.read()
                    current_idx += 1
                    if not ok:
                        break
                if ok:
                    idx_to_frame[target_idx] = letterbox(frame, TARGET_W, TARGET_H)
            if target_idx in idx_to_frame:
                writer.write(idx_to_frame[target_idx])
                frames_written_this_clip += 1

        cap.release()
        total_frames_written += frames_written_this_clip
        print(f"{filename}: {frames_written_this_clip} frames escritos "
              f"({frames_written_this_clip / TARGET_FPS:.1f}s)")

    writer.release()
    total_duration = total_frames_written / TARGET_FPS
    print(f"\nVideo final: {OUTPUT_PATH}")
    print(f"Duracao total: {total_duration:.1f}s ({total_frames_written} frames a {TARGET_FPS}fps)")


if __name__ == "__main__":
    main()
