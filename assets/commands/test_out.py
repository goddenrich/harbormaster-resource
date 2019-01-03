import unittest
import out
from unittest import mock

class TestOut(unittest.TestCase):
    @mock.patch('out.Phabricator')
    def setUp(self, mock_phab):
        self.mock_obj = mock_phab.return_value = mock.Mock() 
        self.payload = {
            "params": {
                "build_status": "pass",
            },
            "source": {
                "conduit_uri": "https://test.conduit.uri/api/",
                "conduit_token": "test-conduit-token",
            },
        }
        self.build_status = out.get_build_status_from_payload(self.payload)
    def test_get_build_status_from_payload(self):
        self.assertEqual(self.build_status, "pass")

    # TODO(goddenrich) figure out how to get the targetPHID here
    def test_update_phabricator_with_build_status(self):
        out.update_phabricator_with_build_status(self.mock_obj, self.build_status)
        self.assertIsNone(self.mock_obj.harbormaster.sendmessage.assert_called_once_with(buildTargetPHID='testTargetPHID', type='pass'))

if __name__ == '__main__':
    unittest.main()

