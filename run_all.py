import subprocess
import os

def run_desktop():
    os.chdir("desktop_client")
    subprocess.run(["python", "main.py"])

run_desktop()
