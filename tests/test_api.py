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
        """Test home page, dashboard, and analyzer route access."""
        res_home = self.client.get('/')
        self.assertEqual(res_home.status_code, 200)

        res_dash = self.client.get('/dashboard')
        self.assertEqual(res_dash.status_code, 200)

        res_analyzer = self.client.get('/analyzer')
        self.assertEqual(res_analyzer.status_code, 200)

    def test_analyzer_endpoint(self):
        """Test unified medical analyzer endpoint."""
        sample_text = (
            "COMPLETE BLOOD COUNT\n"
            "Hemoglobin: 10.2 g/dL [LOW]\n"
            "Total Leucocyte Count (WBC): 14,800 /mcL [HIGH]\n"
            "Platelet Count: 220,000 /mcL [NORMAL]"
        )
        res = self.client.post('/api/analyzer/process', json={'text': sample_text, 'title': 'Test CBC'})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        
        # Check 5-column table structure
        table = data['simplification']['results_table']
        self.assertGreaterEqual(len(table), 1)
        self.assertIn('test_name', table[0])
        self.assertIn('measured_value', table[0])
        self.assertIn('unit', table[0])
        self.assertIn('reference_range', table[0])
        self.assertIn('simple_explanation', table[0])

    def test_hospital_full_details(self):
        """Test hospital query with full verified street addresses and single lookup."""
        res = self.client.get('/api/hospitals?q=110029')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(len(data['hospitals']), 0)
        
        first = data['hospitals'][0]
        self.assertIn('full_address', first)
        self.assertIn('pincode', first)

        # Single hospital detail lookup
        h_id = first['id']
        res_single = self.client.get(f'/api/hospitals/{h_id}')
        self.assertEqual(res_single.status_code, 200)
        single_data = json.loads(res_single.data)
        self.assertTrue(single_data['success'])
        self.assertEqual(single_data['hospital']['id'], h_id)

    def test_speech_command_parsing(self):
        """Test advanced speech NLU parsing."""
        res_en = self.client.post('/api/speech/command', json={'transcript': 'please open the dashboard'})
        self.assertEqual(res_en.status_code, 200)
        data_en = json.loads(res_en.data)
        self.assertTrue(data_en['result']['matched'])
        self.assertEqual(data_en['result']['action'], 'NAVIGATE')

        # Test Hindi command
        res_hi = self.client.post('/api/speech/command', json={'transcript': 'डैशबोर्ड खोलो'})
        self.assertEqual(res_hi.status_code, 200)
        data_hi = json.loads(res_hi.data)
        self.assertTrue(data_hi['result']['matched'])

if __name__ == '__main__':
    unittest.main()
