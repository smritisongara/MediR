import os
from pathlib import Path
from flask import Flask, send_from_directory, render_template_string, jsonify, request
from flask_cors import CORS
from backend.config import Config
from backend.database import init_db

# Import Route Blueprints
from backend.routes.auth import auth_bp
from backend.routes.upload import upload_bp
from backend.routes.explain import explain_bp
from backend.routes.translate import translate_bp
from backend.routes.chatbot import chatbot_bp
from backend.routes.prescription import prescription_bp
from backend.routes.history import history_bp
from backend.routes.hospital import hospital_bp
from backend.routes.video import video_bp
from backend.routes.analyzer import analyzer_bp
from backend.routes.speech import speech_bp

def create_app():
    """Application factory for MediR AI."""
    app = Flask(__name__, static_folder=str(Config.BASE_DIR / "frontend"))
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, supports_credentials=True)
    
    # Initialize SQLite database
    init_db()
    
    # Register API blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(explain_bp)
    app.register_blueprint(translate_bp)
    app.register_blueprint(chatbot_bp)
    app.register_blueprint(prescription_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(hospital_bp)
    app.register_blueprint(video_bp)
    app.register_blueprint(analyzer_bp)
    app.register_blueprint(speech_bp)
    
    # ------------------ Frontend Page Routes ------------------
    frontend_dir = Config.BASE_DIR / "frontend"
    
    @app.route('/')
    def index_page():
        return send_from_directory(frontend_dir, 'index.html')
        
    @app.route('/login')
    @app.route('/login.html')
    def login_page():
        return send_from_directory(frontend_dir, 'login.html')

    @app.route('/signup')
    @app.route('/signup.html')
    def signup_page():
        return send_from_directory(frontend_dir, 'signup.html')
        
    @app.route('/dashboard')
    @app.route('/dashboard.html')
    def dashboard_page():
        return send_from_directory(frontend_dir, 'dashboard.html')

    @app.route('/analyzer')
    @app.route('/analyzer.html')
    def analyzer_page():
        return send_from_directory(frontend_dir, 'analyzer.html')
        
    @app.route('/upload')
    @app.route('/upload.html')
    def upload_page():
        return send_from_directory(frontend_dir, 'upload.html')
        
    @app.route('/explanation')
    @app.route('/explanation.html')
    def explanation_page():
        return send_from_directory(frontend_dir, 'explanation.html')
        
    @app.route('/chatbot')
    @app.route('/chatbot.html')
    def chatbot_page():
        return send_from_directory(frontend_dir, 'chatbot.html')
        
    @app.route('/translation')
    @app.route('/translation.html')
    def translation_page():
        return send_from_directory(frontend_dir, 'translation.html')
        
    @app.route('/voice')
    @app.route('/voice.html')
    def voice_page():
        return send_from_directory(frontend_dir, 'voice.html')
        
    @app.route('/prescription')
    @app.route('/prescription.html')
    def prescription_page():
        return send_from_directory(frontend_dir, 'prescription.html')
        
    @app.route('/history')
    @app.route('/history.html')
    @app.route('/reports.html')
    def history_page():
        return send_from_directory(frontend_dir, 'history.html')
        
    @app.route('/hospital')
    @app.route('/hospital.html')
    @app.route('/hospitals')
    @app.route('/hospitals.html')
    def hospital_page():
        return send_from_directory(frontend_dir, 'hospital.html')

    @app.route('/hospital-details')
    @app.route('/hospital-details.html')
    def hospital_details_page():
        return send_from_directory(frontend_dir, 'hospital-details.html')

    @app.route('/profile')
    @app.route('/profile.html')
    def profile_page():
        return send_from_directory(frontend_dir, 'profile.html')

    # Serve static assets (CSS, JS)
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        return send_from_directory(frontend_dir / 'css', filename)
        
    @app.route('/js/<path:filename>')
    def serve_js(filename):
        return send_from_directory(frontend_dir / 'js', filename)

    # Serve sample files
    @app.route('/sample_data/<path:filename>')
    def serve_sample(filename):
        return send_from_directory(Config.BASE_DIR / 'sample_data', filename)

    # Serve uploaded user files securely
    @app.route('/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    # Error Handlers
    @app.errorhandler(413)
    def file_too_large(e):
        return jsonify({"success": False, "error": "File size exceeds 32MB limit"}), 413

    @app.errorhandler(404)
    def not_found(e):
        if request.path.startswith('/api/'):
            return jsonify({"success": False, "error": "API route not found"}), 404
        return send_from_directory(frontend_dir, 'index.html')

    return app

if __name__ == '__main__':
    app = create_app()
    print(f"🚀 MediR AI running on http://{Config.HOST}:{Config.PORT}")
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
