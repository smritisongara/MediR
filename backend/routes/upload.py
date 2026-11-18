import os
import uuid
import base64
import logging
from pathlib import Path
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from backend.config import Config
from backend.database import save_report, save_explanation
from backend.services.pdf_service import extract_text_from_pdf
from backend.services.ocr_service import extract_text_from_image
from backend.services.ai_service import simplify_medical_report

upload_bp = Blueprint('upload', __name__, url_prefix='/api')
logger = logging.getLogger(__name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

@upload_bp.route('/upload', methods=['POST'])
def upload_file():
    """
    Handle document upload (PDF, Image, Camera photo capture, or raw text sample).
    Extracts text, processes with AI medical simplification, and saves to database.
    """
    user_id = session.get('user_id', 1)
    
    # 1. Check if camera photo base64 was sent
    data = request.get_json(silent=True) or {}
    if data and "camera_image" in data:
        try:
            image_b64 = data["camera_image"]
            # strip data:image/...;base64,
            if "," in image_b64:
                image_b64 = image_b64.split(",", 1)[1]
            img_bytes = base64.b64decode(image_b64)
            filename = f"camera_{uuid.uuid4().hex[:8]}.png"
            file_path = Config.UPLOAD_FOLDER / filename
            with open(file_path, "wb") as f:
                f.write(img_bytes)
                
            ocr_res = extract_text_from_image(file_path)
            if not ocr_res["success"]:
                return jsonify({"success": False, "error": ocr_res.get("error", "Failed to extract text from photo")}), 400
                
            extracted_text = ocr_res["text"]
            simplification = simplify_medical_report(extracted_text)
            
            report_id = save_report("Camera_Capture.png", filename, "png", user_id=user_id)
            save_explanation(
                report_id, extracted_text,
                simplification["summary"],
                simplification["key_findings"],
                simplification["abnormal_values"]
            )
            
            return jsonify({
                "success": True,
                "report_id": report_id,
                "original_filename": "Camera_Capture.png",
                "extracted_text": extracted_text,
                "simplification": simplification,
                "source": "camera"
            }), 200
        except Exception as e:
            return jsonify({"success": False, "error": f"Camera processing failed: {str(e)}"}), 500

    # 2. Check if a pre-loaded sample report or manual text was sent
    if data and "sample_text" in data:
        sample_title = data.get("sample_title", "Sample_Medical_Report.txt")
        extracted_text = data["sample_text"]
        simplification = simplify_medical_report(extracted_text)
        
        report_id = save_report(sample_title, None, "text", user_id=user_id)
        save_explanation(
            report_id, extracted_text,
            simplification["summary"],
            simplification["key_findings"],
            simplification["abnormal_values"]
        )
        return jsonify({
            "success": True,
            "report_id": report_id,
            "original_filename": sample_title,
            "extracted_text": extracted_text,
            "simplification": simplification,
            "source": "sample"
        }), 200

    # 3. Standard file upload (multipart/form-data)
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file part in the request"}), 400
        
    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400
        
    if not allowed_file(file.filename):
        allowed = ", ".join(Config.ALLOWED_EXTENSIONS)
        return jsonify({"success": False, "error": f"File type not supported. Allowed formats: {allowed}"}), 400
        
    orig_filename = secure_filename(file.filename) or "medical_report"
    ext = orig_filename.rsplit('.', 1)[1].lower() if '.' in orig_filename else ''
    unique_filename = f"{uuid.uuid4().hex}_{orig_filename}"
    save_path = Config.UPLOAD_FOLDER / unique_filename
    file.save(save_path)
    
    # Extract text based on file type
    if ext == 'pdf':
        pdf_res = extract_text_from_pdf(save_path)
        if not pdf_res["success"]:
            return jsonify({"success": False, "error": pdf_res["error"]}), 400
        extracted_text = pdf_res["text"]
        if pdf_res.get("is_scanned"):
            # If PDF text was too short, try OCR fallback
            ocr_res = extract_text_from_image(save_path)
            if ocr_res["success"] and ocr_res["text"]:
                extracted_text = ocr_res["text"]
    else:
        # Image file (PNG, JPG, JPEG, WEBP)
        ocr_res = extract_text_from_image(save_path)
        if not ocr_res["success"]:
            return jsonify({"success": False, "error": ocr_res.get("error", "Image unreadable or blurry")}), 400
        extracted_text = ocr_res["text"]
        
    # Analyze and simplify with AI
    simplification = simplify_medical_report(extracted_text)
    
    # Save to SQLite database
    report_id = save_report(orig_filename, unique_filename, ext, user_id=user_id)
    save_explanation(
        report_id, extracted_text,
        simplification["summary"],
        simplification["key_findings"],
        simplification["abnormal_values"]
    )
    
    return jsonify({
        "success": True,
        "report_id": report_id,
        "original_filename": orig_filename,
        "file_type": ext,
        "extracted_text": extracted_text,
        "simplification": simplification
    }), 200

@upload_bp.route('/extract', methods=['POST'])
def extract_only():
    """Extract raw text from uploaded document without completing simplification."""
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400
    file = request.files['file']
    orig_filename = secure_filename(file.filename)
    ext = orig_filename.rsplit('.', 1)[1].lower() if '.' in orig_filename else ''
    
    unique_filename = f"temp_{uuid.uuid4().hex}_{orig_filename}"
    temp_path = Config.UPLOAD_FOLDER / unique_filename
    file.save(temp_path)
    
    try:
        if ext == 'pdf':
            res = extract_text_from_pdf(temp_path)
        else:
            res = extract_text_from_image(temp_path)
        return jsonify(res)
    finally:
        # Secure cleanup of temporary extraction file
        if temp_path.exists():
            temp_path.unlink()
