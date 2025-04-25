import subprocess
import time
import threading
import os

def run_api():
    subprocess.run(["uvicorn", "server.api:app", "--reload"])

def run_desktop():
    os.chdir("desktop_client")
    subprocess.run(["python", "main.py"])

# Запуск API в отдельном потоке
api_thread = threading.Thread(target=run_api)
api_thread.start()

# Подождать, пока API поднимется
time.sleep(2)

# Запуск десктопного клиента
run_desktop()