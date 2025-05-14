from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from ocr_utils import extract_table_data
from google_sheets import send_to_google_sheet

app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    file_path = os.path.join('uploads', file.filename)
    file.save(file_path)

    try:
        rows = extract_table_data(file_path)
        send_to_google_sheet(rows)
        return jsonify({'status': 'success', 'rows_sent': len(rows)})  # ✅ Return JSON!
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)