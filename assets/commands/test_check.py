import unittest
import check
from unittest import mock
from pkg_resources import resource_string

class TestPhabricator(unittest.TestCase):
    def setUp(self):
        self.target_response = {'data': 
            [
                {
                    "id": 2,
                    "phid": "PHID-HMBT-n6rbr4r5djx2o4wii7fm",
                    "fields": {
                        "buildPHID": "PHID-HMBD-roipk7qjjmwgbtvmzg3c",
                    },
                }
            ]
        }
        self.build_response = {'data':
            [
                {
                    "id": 1,
                    "phid": "PHID-HMBD-roipk7qjjmwgbtvmzg3c",
                    "fields": {
                        "buildablePHID": "PHID-HMBB-en7qg4hzo7gg2fuqlmry",
                    },
                }
            ]
        }
        self.buildable_response = {'data':
            [
                {
                    "id": 1,
                    "type": "HMBB",
                    "phid": "PHID-HMBB-en7qg4hzo7gg2fuqlmry",
                    "fields": {
                        "objectPHID": "PHID-DIFF-ya5b4a5urnyikincj6e5",
                        "containerPHID": "PHID-DREV-d2s436jqt4pqsfucs6pm",
                    },
                }
            ]
        }
        self.diff_response = {'data':
            [
                {
                    "id": 932,
                    "phid": "PHID-DIFF-zbyph2rdona74vcgsu2g",
                    "fields": {
                        "refs": [
                            {
                                "type": "branch",
                                "name": "arcpatch-D225_3"
                            },
                        ],
                    },
                }
            ]
        }
        self.rev_response = {'data':
            [
                {
                    "id": 225,
                    "phid": "PHID-DREV-lyl4plyiheajccqjkmo6",
                },
            ]
        }
        self.no_version_payload = {
            "source": {
                "conduit_uri": "https://test.conduit.uri/api/",
                "conduit_token": "test-conduit-token",
            },
        }
        self.empty_version_payload = {
            'source': {
                "conduit_uri": "https://test.conduit.uri/api/",
                "conduit_token": "test-conduit-token",
            },
            'version': {}
        }
        self.previous_version_payload = {
            "source": {
                "conduit_uri": "https://test.conduit.uri/api/",
                "conduit_token": "test-conduit-token",
            },
            "version": {
                "target": "5",
                "diff": "diffID",
                "branch": "test-branch",
                "revision_id": "testrev",
            }
        }


    @mock.patch('check.Phabricator')
    def test_get_latest_if_no_version_in_payload(self, mock_phab):
        mock_obj = mock_phab.return_value = mock.Mock() 
        mock_obj.harbourmaster.target.search.return_value = self.target_response
        mock_obj.harbourmaster.build.search.return_value = self.build_response
        mock_obj.harbourmaster.buildable.search.return_value = self.buildable_response
        mock_obj.differential.diff.search.return_value = self.diff_response
        mock_obj.differential.revision.search.return_value = self.rev_response
        new_versions = check.get_new_versions(mock_obj, self.no_version_payload)
        self.assertIsNone(mock_obj.harbourmaster.target.search.assert_called_with(limit=1))
        
    @mock.patch('check.Phabricator')
    def test_get_latest_if_empty_version_in_payload(self, mock_phab):
        mock_obj = mock_phab.return_value = mock.Mock() 
        mock_obj.harbourmaster.target.search.return_value = self.target_response
        mock_obj.harbourmaster.build.search.return_value = self.build_response
        mock_obj.harbourmaster.buildable.search.return_value = self.buildable_response
        mock_obj.differential.diff.search.return_value = self.diff_response
        mock_obj.differential.revision.search.return_value = self.rev_response
        new_versions = check.get_new_versions(mock_obj, self.empty_version_payload)
        self.assertIsNone(mock_obj.harbourmaster.target.search.assert_called_with(limit=1))
        
    @mock.patch('check.Phabricator')
    def test_get_versions_since_if_version_in_payload(self, mock_phab):
        mock_obj = mock_phab.return_value = mock.Mock() 
        mock_obj.harbourmaster.target.search.return_value = self.target_response
        mock_obj.harbourmaster.build.search.return_value = self.build_response
        mock_obj.harbourmaster.buildable.search.return_value = self.buildable_response
        mock_obj.differential.diff.search.return_value = self.diff_response
        mock_obj.differential.revision.search.return_value = self.rev_response
        new_versions = check.get_new_versions(mock_obj, self.previous_version_payload)
        previous_version_target_id = int(self.previous_version_payload['version']['target'])
        self.assertIsNone(mock_obj.harbourmaster.target.search.assert_called_with(after=previous_version_target_id-1, order=['-id']))

if __name__ == '__main__':
    unittest.main()
