from flask import Blueprint, request, jsonify
from backend.services.translation_service import translate_text, SUPPORTED_LANGUAGES

translate_bp = Blueprint('translate', __name__, url_prefix='/api')

@translate_bp.route('/translate', methods=['POST'])
def handle_translation():
    data = request.get_json() or {}
    text = data.get('text', '')
    target_lang = data.get('target_lang', 'hi')
    
    if not text:
        return jsonify({"success": False, "error": "No text provided to translate"}), 400
        
    translated = translate_text(text, target_lang=target_lang)
    lang_info = SUPPORTED_LANGUAGES.get(target_lang, {"name": target_lang, "native": target_lang})
    
    return jsonify({
        "success": True,
        "original_text": text,
        "translated_text": translated,
        "target_lang": target_lang,
        "language_name": lang_info["name"],
        "native_name": lang_info["native"]
    }), 200

@translate_bp.route('/languages', methods=['GET'])
def list_languages():
    return jsonify({
        "success": True,
        "languages": SUPPORTED_LANGUAGES
    }), 200
