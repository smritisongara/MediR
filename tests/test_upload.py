import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import unittest
import io
import json
from backend.app import create_app
from backend.database import init_db

class MediRUploadTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        init_db()

    def test_sample_text_upload(self):
        """Test uploading sample text directly."""
        payload = {
            "sample_title": "Test CBC Sample.txt",
            "sample_text": "Hemoglobin: 11.0 g/dL [LOW]\nWBC: 12,000 /mcL [HIGH]"
        }
        res = self.client.post('/api/upload', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertIn('report_id', data)

    def test_prescription_endpoint(self):
        """Test prescription analysis endpoint."""
        payload = {
            "prescription_text": "Tab. Amoxicillin 500mg 1 tab 3 times daily x 5 days"
        }
        res = self.client.post('/api/prescription', json=payload)
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['medicines']), 0)

if __name__ == '__main__':
    unittest.main()
