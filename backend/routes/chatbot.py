from flask import Blueprint, request, jsonify, session
from backend.services.ai_service import get_chatbot_response
from backend.services.speech_service import parse_voice_command
from backend.database import save_chat_message, get_chat_history, get_report_details

chatbot_bp = Blueprint('chatbot', __name__, url_prefix='/api/chat')

@chatbot_bp.route('', methods=['POST'])
def chat():
    data = request.get_json() or {}
    question = data.get('question', '').strip()
    report_id = data.get('report_id')
    user_id = session.get('user_id', 1)
    is_voice = data.get('is_voice', False)
    
    if not question:
        return jsonify({"success": False, "error": "Question cannot be empty"}), 400
        
    # Check for predefined voice command if coming from voice assistant
    if is_voice:
        cmd_res = parse_voice_command(question)
        if cmd_res["matched"]:
            return jsonify({
                "success": True,
                "is_command": True,
                "command": cmd_res,
                "response": cmd_res["speech_reply"]
            })
            
    # Retrieve report context if available
    report_context = ""
    if report_id:
        report = get_report_details(report_id, user_id=user_id)
        if report:
            report_context = report.get('extracted_text', '')
            
    # Generate contextual medical response with strict safety boundaries
    ai_response = get_chatbot_response(question, report_context=report_context)
    
    # Save conversation to chat history
    save_chat_message(user_id, report_id, question, ai_response)
    
    return jsonify({
        "success": True,
        "is_command": False,
        "question": question,
        "response": ai_response,
        "report_id": report_id,
        "speak_aloud": is_voice  # Instructs client to read answer aloud if spoken by voice
    }), 200

@chatbot_bp.route('/history', methods=['GET'])
def history():
    user_id = session.get('user_id', 1)
    report_id = request.args.get('report_id', type=int)
    messages = get_chat_history(user_id=user_id, report_id=report_id)
    return jsonify({
        "success": True,
        "history": messages
    }), 200
