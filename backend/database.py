import sqlite3
import json
import logging
from datetime import datetime
from pathlib import Path
from werkzeug.security import generate_password_hash, check_password_hash
from backend.config import Config

logger = logging.getLogger(__name__)

def get_db_connection():
    """Create and return a thread-safe connection to the SQLite database."""
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database tables if they do not already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            preferred_language TEXT DEFAULT 'en',
            preferred_theme TEXT DEFAULT 'light',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 2. Reports Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            report_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            original_filename TEXT NOT NULL,
            stored_filename TEXT,
            file_type TEXT,
            upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            processing_status TEXT DEFAULT 'completed',
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')
    
    # 3. Report Explanations Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS report_explanations (
            explanation_id INTEGER PRIMARY KEY AUTOINCREMENT,
            report_id INTEGER NOT NULL,
            extracted_text TEXT,
            simplified_explanation TEXT,
            key_findings_json TEXT,
            abnormal_values_json TEXT,
            selected_language TEXT DEFAULT 'en',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(report_id) REFERENCES reports(report_id) ON DELETE CASCADE
        )
    ''')
    
    # 4. Chat History Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            chat_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            report_id INTEGER,
            user_question TEXT NOT NULL,
            ai_response TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE SET NULL,
            FOREIGN KEY(report_id) REFERENCES reports(report_id) ON DELETE CASCADE
        )
    ''')

    # 5. Prescriptions Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prescriptions (
            prescription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            original_filename TEXT NOT NULL,
            extracted_text TEXT,
            medicines_json TEXT,
            instructions TEXT,
            precautions TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')

    # 6. Video Analysis Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS video_analyses (
            video_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            original_filename TEXT NOT NULL,
            stored_filename TEXT,
            transcript TEXT,
            summary TEXT,
            key_points_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
        )
    ''')
    
    # Create default demo patient account if not exists
    cursor.execute('SELECT user_id FROM users WHERE username = ?', ('demo_patient',))
    if not cursor.fetchone():
        demo_pass_hash = generate_password_hash('medir123')
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            ('demo_patient', 'demo@medir.ai', demo_pass_hash)
        )
        logger.info("Initialized default demo patient: demo_patient / medir123")
        
    conn.commit()
    conn.close()

# ----------------- User Management Helpers -----------------

def create_user(username, email, password):
    """Register a new user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        password_hash = generate_password_hash(password)
        cursor.execute(
            'INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)',
            (username.strip(), email.strip().lower(), password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        return {"success": True, "user_id": user_id, "username": username}
    except sqlite3.IntegrityError:
        return {"success": False, "error": "Username or Email already registered"}
    except Exception as e:
        return {"success": False, "error": str(e)}
    finally:
        conn.close()

def authenticate_user(email_or_username, password):
    """Authenticate a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM users WHERE email = ? OR username = ?',
        (email_or_username.strip().lower(), email_or_username.strip())
    )
    user = cursor.fetchone()
    conn.close()
    
    if user and check_password_hash(user['password_hash'], password):
        return {
            "success": True,
            "user": {
                "user_id": user['user_id'],
                "username": user['username'],
                "email": user['email'],
                "preferred_language": user['preferred_language'] or 'en',
                "preferred_theme": user['preferred_theme'] or 'light'
            }
        }
    return {"success": False, "error": "Invalid email/username or password"}

def update_user_preferences(user_id, language=None, theme=None):
    """Update language and theme preferences for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if language and theme:
        cursor.execute('UPDATE users SET preferred_language = ?, preferred_theme = ? WHERE user_id = ?', (language, theme, user_id))
    elif language:
        cursor.execute('UPDATE users SET preferred_language = ? WHERE user_id = ?', (language, user_id))
    elif theme:
        cursor.execute('UPDATE users SET preferred_theme = ? WHERE user_id = ?', (theme, user_id))
    conn.commit()
    conn.close()

# ----------------- Reports & Explanation Helpers -----------------

def save_report(original_filename, stored_filename, file_type, user_id=1, status='completed'):
    """Save metadata for an uploaded medical report."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO reports (user_id, original_filename, stored_filename, file_type, processing_status)
           VALUES (?, ?, ?, ?, ?)''',
        (user_id, original_filename, stored_filename, file_type, status)
    )
    conn.commit()
    report_id = cursor.lastrowid
    conn.close()
    return report_id

def save_explanation(report_id, extracted_text, simplified_explanation, key_findings, abnormal_values, lang='en'):
    """Save an AI simplified explanation with findings and abnormal flags."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO report_explanations 
           (report_id, extracted_text, simplified_explanation, key_findings_json, abnormal_values_json, selected_language)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (
            report_id,
            extracted_text,
            simplified_explanation,
            json.dumps(key_findings) if isinstance(key_findings, (list, dict)) else str(key_findings),
            json.dumps(abnormal_values) if isinstance(abnormal_values, (list, dict)) else str(abnormal_values),
            lang
        )
    )
    conn.commit()
    exp_id = cursor.lastrowid
    conn.close()
    return exp_id

def get_all_reports(user_id=1):
    """Retrieve all reports for the specified user with latest explanation snippet."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT r.report_id, r.original_filename, r.file_type, r.upload_date, r.processing_status,
                  e.simplified_explanation, e.abnormal_values_json, e.selected_language
           FROM reports r
           LEFT JOIN report_explanations e ON r.report_id = e.report_id
           WHERE r.user_id = ?
           ORDER BY r.upload_date DESC''',
        (user_id,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    reports = []
    for row in rows:
        abnormal = []
        if row['abnormal_values_json']:
            try:
                abnormal = json.loads(row['abnormal_values_json'])
            except Exception:
                abnormal = []
                
        reports.append({
            "report_id": row['report_id'],
            "original_filename": row['original_filename'],
            "file_type": row['file_type'],
            "upload_date": row['upload_date'],
            "processing_status": row['processing_status'],
            "simplified_explanation": row['simplified_explanation'] or "Analysis completed.",
            "abnormal_count": len(abnormal) if isinstance(abnormal, list) else 0,
            "abnormal_values": abnormal,
            "selected_language": row['selected_language'] or 'en'
        })
    return reports

def get_report_details(report_id, user_id=1):
    """Get complete details and explanation for a specific report."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT r.*, e.explanation_id, e.extracted_text, e.simplified_explanation, 
                  e.key_findings_json, e.abnormal_values_json, e.selected_language
           FROM reports r
           LEFT JOIN report_explanations e ON r.report_id = e.report_id
           WHERE r.report_id = ? AND r.user_id = ?''',
        (report_id, user_id)
    )
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        return None
        
    return {
        "report_id": row['report_id'],
        "original_filename": row['original_filename'],
        "stored_filename": row['stored_filename'],
        "file_type": row['file_type'],
        "upload_date": row['upload_date'],
        "processing_status": row['processing_status'],
        "extracted_text": row['extracted_text'] or "",
        "simplified_explanation": row['simplified_explanation'] or "",
        "key_findings": json.loads(row['key_findings_json']) if row['key_findings_json'] else [],
        "abnormal_values": json.loads(row['abnormal_values_json']) if row['abnormal_values_json'] else [],
        "selected_language": row['selected_language'] or 'en'
    }

def delete_report(report_id, user_id=1):
    """Securely delete a report, its database records, and stored file."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT stored_filename FROM reports WHERE report_id = ? AND user_id = ?', (report_id, user_id))
    row = cursor.fetchone()
    
    if not row:
        conn.close()
        return False
        
    stored_filename = row['stored_filename']
    if stored_filename:
        file_path = Config.UPLOAD_FOLDER / stored_filename
        if file_path.exists():
            try:
                file_path.unlink()
            except Exception as e:
                logger.error(f"Error removing file {file_path}: {e}")
                
    cursor.execute('DELETE FROM reports WHERE report_id = ? AND user_id = ?', (report_id, user_id))
    cursor.execute('DELETE FROM report_explanations WHERE report_id = ?', (report_id,))
    cursor.execute('DELETE FROM chat_history WHERE report_id = ?', (report_id,))
    conn.commit()
    conn.close()
    return True

# ----------------- Chat History Helpers -----------------

def save_chat_message(user_id, report_id, question, response):
    """Save a chat message exchange in history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO chat_history (user_id, report_id, user_question, ai_response)
           VALUES (?, ?, ?, ?)''',
        (user_id, report_id, question, response)
    )
    conn.commit()
    chat_id = cursor.lastrowid
    conn.close()
    return chat_id

def get_chat_history(user_id=1, report_id=None, limit=50):
    """Retrieve chat history."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if report_id:
        cursor.execute(
            '''SELECT * FROM chat_history 
               WHERE user_id = ? AND report_id = ? 
               ORDER BY timestamp ASC LIMIT ?''',
            (user_id, report_id, limit)
        )
    else:
        cursor.execute(
            '''SELECT * FROM chat_history 
               WHERE user_id = ? 
               ORDER BY timestamp ASC LIMIT ?''',
            (user_id, limit)
        )
    rows = cursor.fetchall()
    conn.close()
    
    return [
        {
            "chat_id": row['chat_id'],
            "report_id": row['report_id'],
            "user_question": row['user_question'],
            "ai_response": row['ai_response'],
            "timestamp": row['timestamp']
        }
        for row in rows
    ]

# ----------------- Prescription Helpers -----------------

def save_prescription(original_filename, extracted_text, medicines, instructions, precautions, user_id=1):
    """Save prescription explanation."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO prescriptions 
           (user_id, original_filename, extracted_text, medicines_json, instructions, precautions)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (
            user_id, original_filename, extracted_text,
            json.dumps(medicines) if isinstance(medicines, (list, dict)) else str(medicines),
            instructions, precautions
        )
    )
    conn.commit()
    presc_id = cursor.lastrowid
    conn.close()
    return presc_id

# ----------------- Video Analysis Helpers -----------------

def save_video_analysis(original_filename, stored_filename, transcript, summary, key_points, user_id=1):
    """Save video analysis results."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        '''INSERT INTO video_analyses 
           (user_id, original_filename, stored_filename, transcript, summary, key_points_json)
           VALUES (?, ?, ?, ?, ?, ?)''',
        (
            user_id, original_filename, stored_filename, transcript, summary,
            json.dumps(key_points) if isinstance(key_points, (list, dict)) else str(key_points)
        )
    )
    conn.commit()
    video_id = cursor.lastrowid
    conn.close()
    return video_id
