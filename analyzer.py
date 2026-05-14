import cv2
import subprocess
import numpy as np
import wave
import os

# ── AUDIO ANALYSIS (ventanas de 3s) ──────────────────────────────────
def extract_audio_scores(video_path):
    wav_path = "temp/audio_scan.wav"
    subprocess.run(['ffmpeg', '-y', '-i', video_path, '-ac', '1', '-ar', '22050', wav_path],
                   capture_output=True)
    
    wf = wave.open(wav_path, 'rb')
    data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    volume = np.abs(data).astype(float)
    window = 22050 * 3  # bloques de 3 segundos
    
    scores = []
    for i in range(0, len(volume), window):
        chunk = volume[i:i+window]
        if len(chunk) > 0:
            scores.append(chunk.mean())
    
    wf.close()
    if os.path.exists(wav_path): os.remove(wav_path)
    return scores

# ── MOTION ANALYSIS (muestreo cada 30 frames = 1s a 30fps) ──────────
def analyze_motion_and_center(video_path):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    sample_interval = max(1, int(fps))  # 1 frame por segundo en vez de todos

    motion_scores = []
    centers = []
    frame_count = 0

    ret, prev = cap.read()
    if not ret:
        cap.release()
        return [], []

    prev_gray = cv2.cvtColor(cv2.resize(prev, (320, 180)), cv2.COLOR_BGR2GRAY)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        if frame_count % sample_interval != 0:  # solo analiza 1 de cada N frames
            continue

        # Redimensionar para velocidad
        small = cv2.resize(frame, (320, 180))
        gray = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)

        motion_scores.append(np.mean(diff))

        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        M = cv2.moments(thresh)
        if M["m00"] != 0:
            centers.append(int(M["m10"] / M["m00"]))
        else:
            centers.append(160)  # centro de frame 320px

        prev_gray = gray

    cap.release()
    return motion_scores, centers

# ── FUSIÓN HÍBRIDA IA ────────────────────────────────────────────────
def combine_scores(audio_scores, motion_scores):
    size = min(len(audio_scores), len(motion_scores))
    if size == 0:
        return audio_scores or motion_scores or [0]

    # Normalizar ambas
    def normalize(arr):
        arr = np.array(arr[:size], dtype=float)
        mx = arr.max()
        return (arr / mx).tolist() if mx > 0 else arr.tolist()

    a = normalize(audio_scores)
    m = normalize(motion_scores)

    # 65% audio, 35% movimiento
    return [(a[i] * 0.65) + (m[i] * 0.35) for i in range(size)]
