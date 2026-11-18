import os
import uuid
import base64
import logging
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from backend.config import Config
from backend.database import save_prescription
from backend.services.ocr_service import extract_text_from_image

prescription_bp = Blueprint('prescription', __name__, url_prefix='/api/prescription')
logger = logging.getLogger(__name__)

def parse_prescription_text(text):
    """
    Parse medicines, dosages, schedule, and safety notes from prescription text.
    Never guesses unclear medicine names or modifies dosages.
    """
    medicines = []
    lines = text.split('\n')
    
    # Common medicines list for reference
    known_meds = [
        {"name": "Amoxicillin", "type": "Antibiotic", "purpose": "Bacterial infections"},
        {"name": "Paracetamol", "type": "Antipyretic / Pain Relief", "purpose": "Fever and aches"},
        {"name": "Cetirizine", "type": "Antihistamine", "purpose": "Allergies and runny nose"},
        {"name": "Pantoprazole", "type": "Antacid (PPI)", "purpose": "Acidity and stomach lining protection"},
        {"name": "Azithromycin", "type": "Antibiotic", "purpose": "Respiratory infections"},
        {"name": "Ibuprofen", "type": "NSAID", "purpose": "Pain and inflammation"},
        {"name": "Metformin", "type": "Antidiabetic", "purpose": "Blood sugar regulation"}
    ]
    
    for line in lines:
        line_clean = line.strip()
        if not line_clean:
            continue
            
        for med in known_meds:
            if med["name"].lower() in line_clean.lower():
                medicines.append({
                    "medicine_name": med["name"],
                    "class": med["type"],
                    "purpose": med["purpose"],
                    "instruction_in_prescription": line_clean,
                    "patient_guidance": "Take exactly as prescribed with water. Complete full course."
                })
                break
                
    if not medicines:
        medicines.append({
            "medicine_name": "Review with Pharmacist",
            "class": "Prescription Medicine",
            "purpose": "Consult treating clinician",
            "instruction_in_prescription": "Handwritten or unconfirmed item",
            "patient_guidance": "⚠️ Please have your pharmacist verify this item before dispensing."
        })

    instructions = [
        "Take medicines after food unless explicitly directed to take on an empty stomach.",
        "Drink plenty of water throughout the day.",
        "Store medicines in a cool, dry place away from direct sunlight.",
        "Do not stop antibiotics early, even if you start feeling better."
    ]

    precautions = (
        "⚠️ CRITICAL SAFETY NOTICE: MediR does NOT prescribe medicines or adjust dosages. "
        "Handwritten prescriptions can be misinterpreted. Always have a registered pharmacist or your doctor "
        "verify all drug names, strengths (e.g. mg), and schedules before taking any medication."
    )

    return medicines, instructions, precautions

@prescription_bp.route('', methods=['POST'])
def process_prescription():
    user_id = session.get('user_id', 1)
    data = request.get_json(silent=True) or {}
    
    # 1. Camera capture base64
    if "camera_image" in data:
        try:
            image_b64 = data["camera_image"]
            if "," in image_b64:
                image_b64 = image_b64.split(",", 1)[1]
            img_bytes = base64.b64decode(image_b64)
            filename = f"presc_cam_{uuid.uuid4().hex[:8]}.png"
            file_path = Config.UPLOAD_FOLDER / filename
            with open(file_path, "wb") as f:
                f.write(img_bytes)
                
            ocr_res = extract_text_from_image(file_path)
            extracted_text = ocr_res.get("text", "")
            meds, instructions, precautions = parse_prescription_text(extracted_text)
            
            presc_id = save_prescription("Camera_Prescription.png", extracted_text, meds, "\n".join(instructions), precautions, user_id=user_id)
            return jsonify({
                "success": True,
                "prescription_id": presc_id,
                "extracted_text": extracted_text,
                "medicines": meds,
                "instructions": instructions,
                "precautions": precautions
            })
        except Exception as e:
            return jsonify({"success": False, "error": str(e)}), 500

    # 2. Text sample provided directly
    if "prescription_text" in data:
        extracted_text = data["prescription_text"]
        meds, instructions, precautions = parse_prescription_text(extracted_text)
        presc_id = save_prescription("Sample_Prescription.txt", extracted_text, meds, "\n".join(instructions), precautions, user_id=user_id)
        return jsonify({
            "success": True,
            "prescription_id": presc_id,
            "extracted_text": extracted_text,
            "medicines": meds,
            "instructions": instructions,
            "precautions": precautions
        })

    # 3. File upload (PNG, JPG, PDF)
    if 'file' not in request.files:
        return jsonify({"success": False, "error": "No file uploaded"}), 400
        
    file = request.files['file']
    orig_filename = secure_filename(file.filename)
    unique_filename = f"presc_{uuid.uuid4().hex}_{orig_filename}"
    save_path = Config.UPLOAD_FOLDER / unique_filename
    file.save(save_path)
    
    ocr_res = extract_text_from_image(save_path)
    extracted_text = ocr_res.get("text", "")
    meds, instructions, precautions = parse_prescription_text(extracted_text)
    
    presc_id = save_prescription(orig_filename, extracted_text, meds, "\n".join(instructions), precautions, user_id=user_id)
    return jsonify({
        "success": True,
        "prescription_id": presc_id,
        "original_filename": orig_filename,
        "extracted_text": extracted_text,
        "medicines": meds,
        "instructions": instructions,
        "precautions": precautions
    })
