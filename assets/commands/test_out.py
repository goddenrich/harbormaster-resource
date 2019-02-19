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

    def test_get_version_from_git_config(self):
        version = out.get_version_from_git_config('test_gitconfig')
        self.assertEqual(version.targetPHID, 'target-phid-config')
        self.assertEqual(version.base, 'test-base')
        self.assertEqual(version.branch, 'test-branch')
        self.assertEqual(version.diff, '123')
        self.assertEqual(version.target, '1')


    def test_update_phabricator_with_build_status(self):
        targetPHID = 'testTargetPHID'
        out.update_phabricator_with_build_status(self.mock_obj, targetPHID, self.build_status)
        self.assertIsNone(self.mock_obj.harbormaster.sendmessage.assert_called_once_with(buildTargetPHID=targetPHID, type='pass'))

if __name__ == '__main__':
    unittest.main()

