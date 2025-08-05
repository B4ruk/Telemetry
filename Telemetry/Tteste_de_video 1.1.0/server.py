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
