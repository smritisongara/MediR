import sys
import os
from pathlib import Path

# Add project root to Python module search path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from backend.config import Config
from backend.database import init_db
from backend.app import create_app

def main():
    print("=" * 70)
    print("           🏥 MediR AI - Medical Communication Assistant")
    print("      'Understand Better. Communicate Better. Live Better.'")
    print("        CURSORFLOW: AI Insights to Innovation Hackathon")
    print("=" * 70)
    
    # Initialize SQLite database
    print("[*] Initializing SQLite database...")
    init_db()
    print("[+] Database ready: database/medir.db")
    
    # Create Flask application
    app = create_app()
    
    url = f"http://{Config.HOST}:{Config.PORT}"
    print(f"\n[🚀] Server is running!")
    print(f"[🌐] OPEN IN YOUR BROWSER: {url}")
    print(f"[*] Dashboard:            {url}/dashboard")
    print(f"[*] Report Upload:        {url}/upload")
    print(f"[*] AI Chatbot:           {url}/chatbot")
    print(f"[*] Nearby Hospitals:     {url}/hospitals")
    print(f"[*] Voice Assistant:      {url}/voice")
    print("\n[i] Press CTRL+C in this terminal window to stop the server.")
    print("=" * 70)
    
    app.run(host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)

if __name__ == '__main__':
    main()
