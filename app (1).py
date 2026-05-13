import streamlit as st
import time
import os
import numpy as np
from pathlib import Path

# Importaciones de tu nuevo motor modular
from downloader import download_video
from analyzer import extract_audio_scores, analyze_motion_and_center, combine_scores
from renderer import render_clip
from cleanup import cleanup_temp
from presets import PRESETS

from styles import inject_css
from timeline import render_timeline

# ──────────────────────────────
# CONFIGURACIÓN Y PREPARACIÓN
# ──────────────────────────────

st.set_page_config(
    page_title="PolloClip X Beta",
    page_icon="🐔",
    layout="wide"
)

# Inyectamos el estilo visual de Pollo Enfermo Studio
inject_css()

# Aseguramos que existan las carpetas necesarias
for p in ["exports", "temp", "screenshots", "logo"]:
    Path(p).mkdir(exist_ok=True)

# Limpieza de archivos temporales antiguos (>1 hora)
cleanup_temp()

# ──────────────────────────────
# SIDEBAR (OTTO HQ)
# ──────────────────────────────

with st.sidebar:
    # --- MODIFICACIÓN: CHECK DE SEGURIDAD PARA EL LOGO ---
    logo_path = "otto.png"
    if os.path.exists(logo_path):
        st.image(logo_path, use_container_width=True)
    else:
        st.markdown("<h1 style='text-align:center; margin:0;'>🐔</h1>", unsafe_allow_html=True)
        st.info("Añade tu logo en: `assets/logo/otto.png` para personalizar tu HQ.")

    st.markdown("### OTTO HQ\n**ENGINE: BETA 6.6.0**")
    st.markdown("---")

    modo = st.radio(
        "MODO DE INICIO",
        ["🤖 AUTOMÁTICO", "🕹️ MANUAL"]
    )

    preset_name = st.selectbox(
        "PRESET DE CALIDAD",
        list(PRESETS.keys())
    )

    st.markdown("---")
    st.markdown("**OPCIONES DE RENDER**")
    mute = st.checkbox("Mute (Sin audio)")
    subs = st.checkbox("Subs (Whisper AI)")

# ──────────────────────────────
# HEADER PRINCIPAL
# ──────────────────────────────

st.markdown('<p class="main-title">POLLOCLIP X</p>', unsafe_allow_html=True)
st.markdown('<div class="header-lines">AI HYBRID ENGINE // POLLO ENFERMO STUDIO</div>', unsafe_allow_html=True)

url = st.text_input(
    "LINK DE GAMEPLAY (YOUTUBE)",
    placeholder="https://youtube.com/watch?v=..."
)

# ──────────────────────────────
# LÓGICA PRINCIPAL (MAIN)
# ──────────────────────────────

if url:
    # 1. DESCARGA
    with st.status("📥 Descargando master local...", expanded=False) as status:
        try:
            video = download_video(url)
            status.update(label="✓ Master descargado con éxito", state="complete")
        except Exception as e:
            st.error(f"Error en descarga: {e}")
            st.stop()

    # Cards de información
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">TÍTULO DEL VIDEO</div>
            <div class="stat-value">{video['title'][:65]}...</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">ENGINE STATUS</div>
            <div class="stat-value" style="color:#00ff88;">LOCAL HQ</div>
        </div>
        """, unsafe_allow_html=True)

    # 2. ANÁLISIS / SELECCIÓN DE TIEMPO
    if modo == "🤖 AUTOMÁTICO":
        with st.spinner("🧠 Analizando Audio + Movimiento (IA Híbrida)..."):
            audio_scores = extract_audio_scores(video["path"])
            motion_scores, centers = analyze_motion_and_center(video["path"])
            
            # Fusión de scores (65% Audio / 35% Visual)
            scores = combine_scores(audio_scores, motion_scores)
            
            # El mejor momento (climax)
            peak_idx = np.argmax(scores)
            climax_seconds = peak_idx * 3
            
        # Render del Timeline Visual
        st.plotly_chart(
            render_timeline(scores, climax_seconds),
            use_container_width=True
        )
        
        start_time = max(0, climax_seconds - 11) # Centrar clip de 22s
        st.markdown(f"<p style='color:#df73ff; font-size:12px;'>✓ IA detectó el clímax en el segundo {climax_seconds}</p>", unsafe_allow_html=True)
    
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        start_time = st.slider(
            "SEGUNDO DE INICIO DEL CLIP",
            0,
            int(video["duration"]),
            0
        )

    # 3. GENERACIÓN (RENDER)
    st.markdown("---")
    if st.button("🚀 GENERAR CLIP MAESTRO"):
        output_file = f"exports/pollo_beta_{int(time.time())}.mp4"
        preset = PRESETS[preset_name]
        
        log_placeholder = st.empty()
        
        with st.spinner("🎥 Renderizando con Smart Crop..."):
            render_clip(
                input_path=video["path"],
                output_path=output_file,
                start_time=start_time,
                mute=mute,
                subs=subs,
                crf=preset["crf"],
                bitrate=preset["bitrate"]
            )
        
        st.success(f"★ Clip generado exitosamente en: {output_file}")
        
        # Reproductor Compacto Centrado
        cv1, cv2, cv3 = st.columns([1.5, 1, 1.5])
        with cv2:
            st.video(output_file)
            st.markdown(f"<p style='text-align:center; font-size:10px; color:#4a4a60;'>Final Build Beta 6.6.0</p>", unsafe_allow_html=True)