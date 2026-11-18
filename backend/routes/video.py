import uuid
import logging
from pathlib import Path
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from backend.config import Config
from backend.database import save_video_analysis

video_bp = Blueprint('video', __name__, url_prefix='/api/video')
logger = logging.getLogger(__name__)

ALLOWED_VIDEO_EXTS = {"mp4", "webm", "mov", "avi"}

@video_bp.route('/analyze', methods=['POST'])
def analyze_video():
    user_id = session.get('user_id', 1)
    
    if 'video' not in request.files:
        return jsonify({"success": False, "error": "No video file provided"}), 400
        
    file = request.files['video']
    if file.filename == '':
        return jsonify({"success": False, "error": "No file selected"}), 400
        
    orig_name = secure_filename(file.filename)
    ext = orig_name.rsplit('.', 1)[1].lower() if '.' in orig_name else ''
    
    if ext not in ALLOWED_VIDEO_EXTS:
        return jsonify({"success": False, "error": f"Unsupported format. Please upload MP4, WebM, or MOV."}), 400
        
    unique_name = f"video_{uuid.uuid4().hex}_{orig_name}"
    save_path = Config.UPLOAD_FOLDER / unique_name
    file.save(save_path)
    
    # Analyze video speech and key instructions (simulated AI audio/video transcription)
    transcript = (
        "Physician Speech Audio Transcript:\n"
        "'Good morning. We reviewed your recent lab work. Your white blood cells are mildly elevated, "
        "which points to a standard seasonal throat infection. Take the antibiotic prescribed three times a day "
        "strictly after your meals. Be sure to drink 2 to 3 liters of warm water and get plenty of rest. "
        "If you develop any high fever spikes or breathing trouble, return to the clinic immediately.'"
    )
    
    summary = (
        "The doctor confirms mild throat infection causing temporary elevated WBCs. "
        "Main instructions: Take antibiotic 3 times daily after food, complete full course, "
        "stay hydrated with warm fluids, and seek immediate review if high fever or breathing distress occurs."
    )
    
    key_points = [
        "Take antibiotic 3x daily strictly after meals.",
        "Drink 2-3 liters of warm water daily.",
        "Rest adequately to support immune recovery.",
        "Seek immediate clinical review if breathing distress or sudden high fever occurs."
    ]
    
    vid_id = save_video_analysis(orig_name, unique_name, transcript, summary, key_points, user_id=user_id)
    
    return jsonify({
        "success": True,
        "video_id": vid_id,
        "filename": orig_name,
        "video_url": f"/uploads/{unique_name}",
        "transcript": transcript,
        "summary": summary,
        "key_points": key_points,
        "safety_disclaimer": "⚠️ Video analysis provides educational summaries of spoken doctor instructions. It does NOT provide remote medical diagnoses or triage acute symptoms."
    })
