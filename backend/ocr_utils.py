import cv2
import pytesseract
import numpy as np
import re
import shutil

# ✅ Ensure tesseract binary is available
if not shutil.which("tesseract"):
    raise EnvironmentError("❌ Tesseract is not installed or not in PATH. Make sure railway.nix includes pkgs.tesseract.")

def extract_table_data(image_path):
    image = cv2.imread(image_path)

    # Convert to grayscale and apply threshold
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    # Extract name region (left) and lodging region (right)
    h, w = binary.shape
    name_col = binary[50:h, 0:int(w * 0.6)]
    lodging_col = binary[50:h, int(w * 0.8):w]

    # OCR config
    config = r'--oem 3 --psm 6'
    name_text = pytesseract.image_to_string(name_col, config=config)
    lodging_text = pytesseract.image_to_string(lodging_col, config=config)

    # Split and clean rows
    names = name_text.split("\n")
    lodgings = lodging_text.split("\n")

    data = []
    for name, lodging in zip(names, lodgings):
        name = name.strip()
        lodging = lodging.strip()

        if name and lodging:
            # Clean name (before first comma)
            if ',' in name:
                name = name.split(',')[0].strip()
            name = name.upper()

            # Clean lodging value
            lodging = lodging.replace(",", "")
            if lodging.isdigit():
                data.append((name, int(lodging)))

    return data
