from flask import Blueprint, request, jsonify
from backend.services.speech_service import parse_voice_command, VOICE_LOCALES, COMMAND_MAPPINGS

speech_bp = Blueprint('speech', __name__, url_prefix='/api/speech')

@speech_bp.route('/command', methods=['POST'])
def handle_command():
    data = request.get_json() or {}
    transcript = data.get('transcript', '').strip()
    
    if not transcript:
        return jsonify({"success": False, "error": "Transcript cannot be empty"}), 400
        
    result = parse_voice_command(transcript)
    return jsonify({
        "success": True,
        "result": result
    })

@speech_bp.route('/commands', methods=['GET'])
def list_commands():
    return jsonify({
        "success": True,
        "locales": VOICE_LOCALES,
        "commands": COMMAND_MAPPINGS
    })
