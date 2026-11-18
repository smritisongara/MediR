from flask import Blueprint, request, jsonify, session
from backend.services.ai_service import simplify_medical_report
from backend.database import save_explanation, get_report_details

explain_bp = Blueprint('explain', __name__, url_prefix='/api')

@explain_bp.route('/explain', methods=['POST'])
def explain_report():
    data = request.get_json() or {}
    text = data.get('text', '')
    report_id = data.get('report_id')
    user_id = session.get('user_id', 1)
    
    # If text is empty but report_id is provided, fetch report text from database
    if not text and report_id:
        report = get_report_details(report_id, user_id=user_id)
        if report and report['extracted_text']:
            text = report['extracted_text']
            
    if not text:
        return jsonify({"success": False, "error": "No medical text provided for explanation"}), 400
        
    simplification = simplify_medical_report(text)
    
    # Update database record if report_id exists
    if report_id:
        save_explanation(
            report_id,
            text,
            simplification["summary"],
            simplification["key_findings"],
            simplification["abnormal_values"]
        )
        
    return jsonify({
        "success": True,
        "simplification": simplification,
        "report_id": report_id
    }), 200

@explain_bp.route('/report/<int:report_id>', methods=['GET'])
def get_report(report_id):
    user_id = session.get('user_id', 1)
    report = get_report_details(report_id, user_id=user_id)
    if not report:
        return jsonify({"success": False, "error": "Report not found or access denied"}), 404
    return jsonify({"success": True, "report": report}), 200
