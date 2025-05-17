import cv2
import pytesseract
import numpy as np
import shutil
from PIL import Image


# ✅ Set tesseract path explicitly (based on Railway nix profile)
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

def extract_table_data(image_path):
    # Load image
    image = cv2.imread(image_path)

    # Convert to grayscale and apply threshold for better OCR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    # Define crop regions (adjust based on image width)
    h, w = image.shape[:2]
    
    # Approximate column positions (tweak if needed)
    name_col = image[0:h, 0:int(w * 0.6)]
    lodging_col = image[0:h, int(w * 0.82):w]

    # OCR both columns
    name_text = pytesseract.image_to_string(name_col, config='--psm 6')
    lodging_text = pytesseract.image_to_string(lodging_col, config='--psm 6')

    # Split lines
    name_lines = name_text.strip().split('\n')
    lodging_lines = lodging_text.strip().split('\n')

    # Clean lines
    name_lines = [line.strip().strip(',') for line in name_lines if line.strip()]
    lodging_lines = [line.strip().replace(' ', '').replace('O', '0') for line in lodging_lines if line.strip()]

    # Pair and filter valid rows (only numeric Lodging values)
    rows = []
    for name, lodging in zip(name_lines, lodging_lines):
        if any(char.isdigit() for char in lodging):
            rows.append([name, lodging])

    return rows
