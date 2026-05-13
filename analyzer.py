import cv2
import subprocess
import numpy as np
import wave
import os

# ──────────────────────────────
# AUDIO ANALYSIS (VENTANAS DE 3s)
# ──────────────────────────────
def extract_audio_scores(video_path):
    wav_path = "temp/audio_scan.wav"
    # Extraemos audio de forma rápida
    subprocess.run(['ffmpeg', '-y', '-i', video_path, '-ac', '1', '-ar', '22050', wav_path], capture_output=True)
    
    wf = wave.open(wav_path, 'rb')
    data = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16)
    volume = np.abs(data).astype(float)
    window = 22050 * 3 # Bloques de 3 segundos
    
    scores = []
    for i in range(0, len(volume), window):
        chunk = volume[i:i+window]
        if len(chunk) > 0:
            scores.append(chunk.mean())
    
    wf.close()
    if os.path.exists(wav_path): os.remove(wav_path)
    return scores

# ──────────────────────────────
# MOTION ANALYSIS & SMART CROP
# ──────────────────────────────
def analyze_motion_and_center(video_path):
    cap = cv2.VideoCapture(video_path)
    motion_scores = []
    centers = []
    
    ret, prev = cap.read()
    if not ret: return [], []
    
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
    
    while True:
        ret, frame = cap.read()
        if not ret: break
        
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        diff = cv2.absdiff(prev_gray, gray)
        
        # Intensidad de movimiento
        motion_scores.append(np.mean(diff))
        
        # SMART CROP: Buscamos el centro de la acción
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)
        M = cv2.moments(thresh)
        if M["m00"] != 0:
            centers.append(int(M["m10"] / M["m00"]))
        else:
            centers.append(int(frame.shape[1]/2))
            
        prev_gray = gray
        
    cap.release()
    return motion_scores, centers

# ──────────────────────────────
# FUSIÓN HÍBRIDA IA
# ──────────────────────────────
def combine_scores(audio_scores, motion_scores):
    # Sincronizamos las longitudes (audio está en ventanas de 3s, motion en frames)
    # Suponiendo 30fps, 3s son 90 frames.
    size = min(len(audio_scores), len(motion_scores)//90)
    
    combined = []
    for i in range(size):
        # 65% importancia al audio, 35% al movimiento visual
        score = (audio_scores[i] * 0.65) + (motion_scores[i*90] * 0.35)
        combined.append(score)
        
    return combined