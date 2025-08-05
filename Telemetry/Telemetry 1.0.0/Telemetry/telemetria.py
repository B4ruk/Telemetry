import psutil
import os
import sys
import platform
import time
from datetime import datetime

#HARDWARE

#Infos_CPU
cpupercent = psutil.cpu_percent(interval=1, percpu=False)
cpulogic = psutil.cpu_count(logical=True)
cpufreq = psutil.cpu_freq(percpu=False)

#Infos_Disk
usage =  psutil.disk_usage('/')

#Infos_Senssors
temp = psutil.sensors_battery()

#Boot_time
timeactv = psutil.boot_time()

#Nems_Users
user = psutil.users()

print(cpupercent)
print(cpulogic)
print(cpufreq)
print(usage)
print(temp)
print(timeactv)
print(user)

#S.O

infoso = sys.plataform
print(infoso)