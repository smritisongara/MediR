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
from backend.services.video_service import process_consultation_video

analyzer_bp = Blueprint('analyzer', __name__, url_prefix='/api/analyzer')
logger = logging.getLogger(__name__)

@analyzer_bp.route('/process', methods=['POST'])
def process_analysis():
    """
    Unified Medical Problem and Report Analyzer Endpoint.
    Supports 5 input modalities:
    1. Written Input (symptoms, questions, pasted text)
    2. PDF / Document Upload
    3. Photo & Camera Capture
    4. Voice Input (Speech-to-text transcript)
    5. Video Upload
    """
    user_id = session.get('user_id', 1)
    
    # 1. Check if multipart file upload (PDF, Image, or Video)
    if 'file' in request.files:
        file = request.files['file']
        if file.filename != '':
            orig_filename = secure_filename(file.filename) or "medical_document"
            ext = orig_filename.rsplit('.', 1)[1].lower() if '.' in orig_filename else ''
            
            unique_filename = f"{uuid.uuid4().hex}_{orig_filename}"
            save_path = Config.UPLOAD_FOLDER / unique_filename
            file.save(save_path)
            
            # Handle Video
            if ext in ("mp4", "webm", "mov", "avi"):
                video_res = process_consultation_video(save_path)
                return jsonify({
                    "success": True,
                    "input_type": "video",
                    "filename": orig_filename,
                    "video_result": video_res,
                    "simplification": {
                        "summary": video_res["summary"],
                        "results_table": [],
                        "abnormal_values": [],
                        "important_observations": video_res["key_points"],
                        "unreadable_or_missing": None,
                        "recommended_doctor_questions": [
                            "Could you confirm the recommended antibiotic dosage and duration?",
                            "What warning signs should prompt an immediate in-person clinic revisit?"
                        ],
                        "glossary": []
                    }
                })
                
            # Handle PDF
            if ext == 'pdf':
                pdf_res = extract_text_from_pdf(save_path)
                extracted_text = pdf_res.get("text", "")
                if pdf_res.get("is_scanned"):
                    ocr_res = extract_text_from_image(save_path)
                    if ocr_res.get("success"):
                        extracted_text = ocr_res.get("text", "")
            else:
                # Handle Image (PNG, JPG, WEBP)
                ocr_res = extract_text_from_image(save_path)
                if not ocr_res.get("success"):
                    return jsonify({"success": False, "error": ocr_res.get("error", "Image unreadable or blurry")}), 400
                extracted_text = ocr_res.get("text", "")
                
            analysis = simplify_medical_report(extracted_text)
            report_id = save_report(orig_filename, unique_filename, ext, user_id=user_id)
            save_explanation(
                report_id, extracted_text,
                analysis["summary"],
                analysis["results_table"],
                analysis["abnormal_values"]
            )
            
            return jsonify({
                "success": True,
                "input_type": "document",
                "filename": orig_filename,
                "report_id": report_id,
                "extracted_text": extracted_text,
                "simplification": analysis
            })

    # 2. JSON Body Handling (Written input, Camera base64, Voice transcript, or Sample Text)
    data = request.get_json(silent=True) or {}
    
    # Camera Base64 Photo
    if "camera_image" in data:
        try:
            image_b64 = data["camera_image"]
            if "," in image_b64:
                image_b64 = image_b64.split(",", 1)[1]
            img_bytes = base64.b64decode(image_b64)
            filename = f"cam_{uuid.uuid4().hex[:8]}.png"
            file_path = Config.UPLOAD_FOLDER / filename
            with open(file_path, "wb") as f:
                f.write(img_bytes)
                
            ocr_res = extract_text_from_image(file_path)
            extracted_text = ocr_res.get("text", "")
            analysis = simplify_medical_report(extracted_text)
            
            report_id = save_report("Camera_Photo.png", filename, "png", user_id=user_id)
            save_explanation(
                report_id, extracted_text,
                analysis["summary"],
                analysis["results_table"],
                analysis["abnormal_values"]
            )
            
            return jsonify({
                "success": True,
                "input_type": "camera",
                "report_id": report_id,
                "extracted_text": extracted_text,
                "simplification": analysis
            })
        except Exception as e:
            return jsonify({"success": False, "error": f"Failed to process camera snapshot: {str(e)}"}), 500

    # Written symptoms, medical questions, voice transcript, or pasted text
    written_text = data.get("text") or data.get("sample_text") or data.get("voice_transcript")
    if written_text:
        title = data.get("title", "Written Medical Inquiry")
        input_type = data.get("input_type", "written")
        analysis = simplify_medical_report(written_text)
        
        report_id = save_report(title, None, "text", user_id=user_id)
        save_explanation(
            report_id, written_text,
            analysis["summary"],
            analysis["results_table"],
            analysis["abnormal_values"]
        )
        
        return jsonify({
            "success": True,
            "input_type": input_type,
            "report_id": report_id,
            "extracted_text": written_text,
            "simplification": analysis
        })

    return jsonify({"success": False, "error": "No medical input provided. Please provide text, document, photo, or audio."}), 400
