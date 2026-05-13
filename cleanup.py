import os
import time

def cleanup_temp():
    folder = "temp"
    if not os.path.exists(folder):
        return

    now = time.time()
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        if os.path.isfile(path):
            # Borra archivos con más de 1 hora de antigüedad
            if (now - os.path.getmtime(path)) > 3600:
                try:
                    os.remove(path)
                except:
                    pass