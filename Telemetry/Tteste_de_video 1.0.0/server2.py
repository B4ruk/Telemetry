from flask import Flask, Response
import cv2
import numpy as np
import mss
import time

app = Flask(__name__)

def gerar_frames():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  # Monitor 1 é a tela principal
        while True:
            start_time = time.time()
            
            # Captura a tela
            img = sct.grab(monitor)

            # Converte a imagem capturada para um array NumPy
            frame = np.array(img)

            # Verifica se a captura foi bem-sucedida
            if frame is None or frame.size == 0:
                print("Erro ao capturar a tela.")
                continue

            # Converte BGRA para BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            # Codifica a imagem para JPEG
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            frame = buffer.tobytes()

            # Envia o frame como parte de um fluxo de vídeo
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

            # Aguarda o tempo necessário para manter 60 FPS
            elapsed_time = time.time() - start_time
            time_to_sleep = max(0, (1 / 60) - elapsed_time)
            time.sleep(time_to_sleep)

@app.route('/video_feed')
def video_feed():
    return Response(gerar_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
