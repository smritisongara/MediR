from flask import Blueprint, request, jsonify, session
from backend.database import create_user, authenticate_user, update_user_preferences

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '').strip()
    
    if not username or not email or not password:
        return jsonify({"success": False, "error": "Username, email, and password are required"}), 400
        
    if len(password) < 6:
        return jsonify({"success": False, "error": "Password must be at least 6 characters long"}), 400
        
    result = create_user(username, email, password)
    if result["success"]:
        session['user_id'] = result['user_id']
        session['username'] = result['username']
        return jsonify(result), 201
    return jsonify(result), 400

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    identifier = data.get('email', '') or data.get('username', '')
    password = data.get('password', '')
    
    if not identifier or not password:
        return jsonify({"success": False, "error": "Email/Username and password are required"}), 400
        
    result = authenticate_user(identifier, password)
    if result["success"]:
        user = result["user"]
        session['user_id'] = user['user_id']
        session['username'] = user['username']
        session['email'] = user['email']
        session['preferred_language'] = user['preferred_language']
        session['preferred_theme'] = user['preferred_theme']
        return jsonify(result), 200
    return jsonify(result), 401

@auth_bp.route('/guest', methods=['POST', 'GET'])
def guest_login():
    """One-click instant demo patient login for hackathon judges and testing."""
    session['user_id'] = 1
    session['username'] = 'demo_patient'
    session['email'] = 'demo@medir.ai'
    session['preferred_language'] = 'en'
    session['preferred_theme'] = 'light'
    return jsonify({
        "success": True,
        "user": {
            "user_id": 1,
            "username": "demo_patient",
            "email": "demo@medir.ai",
            "preferred_language": "en",
            "preferred_theme": "light"
        },
        "message": "Logged in as Demo Patient"
    }), 200

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    if 'user_id' in session:
        return jsonify({
            "authenticated": True,
            "user": {
                "user_id": session['user_id'],
                "username": session['username'],
                "email": session.get('email', 'demo@medir.ai'),
                "preferred_language": session.get('preferred_language', 'en'),
                "preferred_theme": session.get('preferred_theme', 'light')
            }
        })
    # Default to demo patient if no session yet
    return jsonify({
        "authenticated": True,
        "user": {
            "user_id": 1,
            "username": "demo_patient",
            "email": "demo@medir.ai",
            "preferred_language": "en",
            "preferred_theme": "light"
        }
    })

@auth_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return jsonify({"success": True, "message": "Logged out successfully"}), 200

@auth_bp.route('/preferences', methods=['POST'])
def save_preferences():
    data = request.get_json() or {}
    user_id = session.get('user_id', 1)
    lang = data.get('language')
    theme = data.get('theme')
    
    if lang:
        session['preferred_language'] = lang
    if theme:
        session['preferred_theme'] = theme
        
    update_user_preferences(user_id, language=lang, theme=theme)
    return jsonify({"success": True, "language": session.get('preferred_language'), "theme": session.get('preferred_theme')})
