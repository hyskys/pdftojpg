# app.py
import os
import zipfile
import uuid
from flask import Flask, request, render_template, send_file
from pdf2image import convert_from_bytes
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
RESULT_FOLDER = "results"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert_pdf():
    if "pdfFile" not in request.files:
        return "파일이 업로드되지 않았습니다.", 400

    pdf_file = request.files["pdfFile"]

    if pdf_file.filename == "":
        return "파일명이 비어 있습니다.", 400

    try:
        # 고유한 작업 디렉토리 생성
        task_id = str(uuid.uuid4())
        task_dir = os.path.join(RESULT_FOLDER, task_id)
        os.makedirs(task_dir, exist_ok=True)

        # PDF → 이미지 변환
        images = convert_from_bytes(pdf_file.read(), dpi=200)
        image_paths = []
        for i, img in enumerate(images):
            image_path = os.path.join(task_dir, f"page_{i+1}.jpg")
            img.save(image_path, "JPEG")
            image_paths.append(image_path)

        # 이미지들을 ZIP으로 묶기
        zip_path = os.path.join(RESULT_FOLDER, f"{task_id}.zip")
        with zipfile.ZipFile(zip_path, "w") as zipf:
            for img_path in image_paths:
                zipf.write(img_path, os.path.basename(img_path))

        return send_file(zip_path, as_attachment=True)

    except Exception as e:
        return f"변환 중 오류 발생: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)
