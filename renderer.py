import subprocess
import os

def render_clip(input_path, output_path, start_time, mute=False, subs=False, crf=18, bitrate="8M"):
    # Filtro Smart Crop (ih*9/16 es el ancho vertical)
    vf_chain = "crop=ih*9/16:ih"
    
    # Lógica de Subtítulos (Whisper)
    if subs:
        import whisper
        model = whisper.load_model("base")
        # Extraer audio temporal para Whisper
        subprocess.run(['ffmpeg', '-y', '-ss', str(start_time), '-t', '22', '-i', input_path, 'temp/sub_audio.mp3'], capture_output=True)
        result = model.transcribe("temp/sub_audio.mp3")
        # Aquí crearíamos un .srt básico, pero por ahora usamos el filtro de texto de FFmpeg
        # como placeholder para el 'Hard Burn' de subs.
        # En una versión final, aquí se añade: subtitles=temp/subs.srt
        pass

    cmd = [
        'ffmpeg', '-y', '-ss', str(start_time), '-i', input_path, '-t', '22',
        '-vf', vf_chain, '-c:v', 'libx264', '-preset', 'fast', '-crf', str(crf), '-b:v', bitrate
    ]
    
    if mute: cmd.extend(['-an'])
    else: cmd.extend(['-c:a', 'aac', '-b:a', '192k'])
    
    cmd.append(output_path)
    subprocess.run(cmd)