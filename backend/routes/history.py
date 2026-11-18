from flask import Blueprint, request, jsonify, session
from backend.database import get_all_reports, get_report_details, delete_report

history_bp = Blueprint('history', __name__, url_prefix='/api')

@history_bp.route('/reports', methods=['GET'])
def list_reports():
    user_id = session.get('user_id', 1)
    reports = get_all_reports(user_id=user_id)
    return jsonify({
        "success": True,
        "count": len(reports),
        "reports": reports
    }), 200

@history_bp.route('/reports/<int:report_id>', methods=['GET'])
def report_details(report_id):
    user_id = session.get('user_id', 1)
    report = get_report_details(report_id, user_id=user_id)
    if not report:
        return jsonify({"success": False, "error": "Report not found or unauthorized"}), 404
    return jsonify({"success": True, "report": report}), 200

@history_bp.route('/reports/<int:report_id>', methods=['DELETE'])
def remove_report(report_id):
    user_id = session.get('user_id', 1)
    success = delete_report(report_id, user_id=user_id)
    if success:
        return jsonify({"success": True, "message": f"Report #{report_id} and stored data securely deleted"}), 200
    return jsonify({"success": False, "error": "Report not found or deletion failed"}), 404
