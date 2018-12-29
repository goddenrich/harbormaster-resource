import unittest
import check
from unittest.mock import patch

class TestPhabricator(unittest.TestCase):
    def setUp(self):
        self.latest_target = {'data': [{
            "id": 2,
            "type": "HMBT",
            "phid": "PHID-HMBT-n6rbr4r5djx2o4wii7fm",
            "fields": {
                "name": "Make HTTP Request",
                "buildPHID": "PHID-HMBD-roipk7qjjmwgbtvmzg3c",
                "buildStepPHID": "PHID-HMCS-kzlrqdivjddl6ervz7zu",
                "status": {
                    "value": "target/failed",
                    "name": "Failed"
                },
                "epochStarted": 1545663455,
                "epochCompleted": 1545663456,
                "buildGeneration": 2,
                "dateCreated": 1545663455,
                "dateModified": 1545663456,
                "policy": {
                    "view": "users"
                }
            },
            "attachments": {}
        }]}

    def test_test(self):
        with patch('check.Phabricator') as mock_phab:
            mock_phab.harbourmaster.target.search.return_value = self.latest_target
            print(check.Phabricator.get_latest_target())
            # print(check.Phabricator.harbourmaster.target.search())
            self.assertEqual(1,2)

if __name__ == '__main__':
    unittest.main()
