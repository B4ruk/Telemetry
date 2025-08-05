import platform
import psutil
import time
from datetime import datetime

def bytes_to_gb(b):
    return round(b / (1024 ** 3), 2)

print("=== INFORMAÇÕES DO SISTEMA ===")
print("Sistema:", platform.system(), platform.release())
print("Versão:", platform.version())
print("Arquitetura:", platform.machine())
print("Processador:", platform.processor)
print("Tempo de atividade:", datetime.fromtimestamp(psutil.boot_time()).strftime("%d/%m/%Y %H:%M:%S"))

print("=== MONITORAMENTO DE TELEMETRIA ===")

while True:
    cpu = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    net = psutil.net_io_counters()

    print(f"CPU: {cpu}%")
    print(f"RAM: {bytes_to_gb(ram.used)} GB / {bytes_to_gb(ram.total)} GB")
    print(f"DISCO: {bytes_to_gb(disk.used)} GB / {bytes_to_gb(disk.total)} GB")
    print(f"Enviados: {round(net.bytes_sent / (1024 * 1024), 2)} MB | Recebidos: {round(net.bytes_recv / (1024 * 1024), 2)} MB")
    print("="*40)
    time.sleep(2)