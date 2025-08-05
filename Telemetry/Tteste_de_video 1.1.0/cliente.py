from flask import Flask, jsonify, render_template
import psutil
import socket
import platform
import time

app = Flask(__name__)

# Simulação de máquinas clientes
cliente = [
    {
        "usuario": "user1",
        "hostname": socket.gethostname(),
        "ip": "192.168.254.15",
        "ram_total": psutil.virtual_memory().total,
        "ram_usada": psutil.virtual_memory().used,
        "ram_livre": psutil.virtual_memory().available,
        "cpu_percent": psutil.cpu_percent(interval=1),
        "uso_internet": psutil.net_if_stats(),
        "tempo_atividade": time.time() - psutil.boot_time(),
    },
    # Adicione mais clientes conforme necessário
]

@app.route('/')
def index():
    return render_template('index.html', cliente=cliente)

@app.route('/api/clientes')
def api_clientes():
    return jsonify(cliente)

if __name__ == '__main__':
    app.run(host='192.168.254.15', port=5000)

#------------------------------------------------------------------------------------------------#
from flask import Flask, Response
import cv2, mss, time
import numpy as np

app = Flask(__name__)

def gerar_frames():
    with mss.mss() as sct:
        monitor = sct.monitors[1]  #Área da tela e qual monitor
        while True:
            start_time = time.time()

            #Cap. Tela
            img = sct.grab(monitor)

            #conv to array NumPy
            frame = np.array(img)

            #VERIFICAÇÃO
            if frame is None or frame.size == 0:
                print("ERRO AO CAPTURAR TELA.")
                continue

            #Conv BGRA to BGR
            frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)

            #Cod img to JPEG
            _, buffer = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
            frame = buffer.tobytes()

            #frame com parte de um flux de vid
            yield (b'--frame\r\n'
                   b'Content - Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
            #Tempo para gerar os 60fps
            elapsed_time = time.time() - start_time
            time_to_sleep = max(0, (1 / 60) - elapsed_time)
            time.sleep(time_to_sleep)

@app.route('/video_feed')
def video_feed():
    return Response(gerar_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
