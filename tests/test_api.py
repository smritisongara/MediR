import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
import json
from backend.app import create_app
from backend.database import init_db

class MediRAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        init_db()

    def test_health_routes(self):
        """Test home page and dashboard route access."""
        res_home = self.client.get('/')
        self.assertEqual(res_home.status_code, 200)

        res_dash = self.client.get('/dashboard')
        self.assertEqual(res_dash.status_code, 200)

    def test_guest_login(self):
        """Test one-click demo patient login."""
        res = self.client.post('/api/auth/guest')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['user']['username'], 'demo_patient')

    def test_medical_explanation(self):
        """Test AI medical simplification and value checking."""
        sample_text = (
            "COMPLETE BLOOD COUNT\n"
            "Hemoglobin: 10.2 g/dL [LOW]\n"
            "Total Leucocyte Count (WBC): 14,800 /mcL [HIGH]\n"
            "Platelet Count: 220,000 /mcL [NORMAL]"
        )
        res = self.client.post('/api/explain', json={'text': sample_text})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        
        abnormal = data['simplification']['abnormal_values']
        self.assertGreaterEqual(len(abnormal), 1)

    def test_translation(self):
        """Test medical translation into Hindi."""
        text = "WBC count is high. Please consult your physician."
        res = self.client.post('/api/translate', json={'text': text, 'target_lang': 'hi'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn("translated_text", data)

    def test_hospitals_search(self):
        """Test nearby hospitals query."""
        res = self.client.get('/api/hospitals?city=New%20Delhi')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['hospitals']), 0)

if __name__ == '__main__':
    unittest.main()
