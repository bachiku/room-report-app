import os
import subprocess

print("RAILWAY ENV PATH:", os.environ.get("PATH"))
try:
    path = subprocess.run(["which", "tesseract"], stdout=subprocess.PIPE).stdout.decode().strip()
    print("FOUND TESSERACT AT:", path)
except Exception as e:
    print("❌ Tesseract not found:", str(e))
