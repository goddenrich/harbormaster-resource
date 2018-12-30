import unittest
import check
from unittest import mock
from pkg_resources import resource_string

class TestPhabricator(unittest.TestCase):
    @mock.patch('check.Phabricator')
    def setUp(self, mock_phab):
        self.mock_obj = mock_phab.return_value = mock.Mock() 
        target_response = {'data': 
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
        build_response = {'data':
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
        buildable_response = {'data':
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
        diff_response = {'data':
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
        rev_response = {'data':
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
        self.mock_obj.harbourmaster.target.search.return_value = target_response
        self.mock_obj.harbourmaster.build.search.return_value = build_response
        self.mock_obj.harbourmaster.buildable.search.return_value = buildable_response
        self.mock_obj.differential.diff.search.return_value = diff_response
        self.mock_obj.differential.revision.search.return_value = rev_response


    def test_get_latest_if_no_version_in_payload(self):
        new_versions = check.get_new_versions(self.mock_obj, self.no_version_payload)
        self.assertIsNone(self.mock_obj.harbourmaster.target.search.assert_called_with(limit=1))

    def test_get_latest_if_empty_version_in_payload(self):
        new_versions = check.get_new_versions(self.mock_obj, self.empty_version_payload)
        self.assertIsNone(self.mock_obj.harbourmaster.target.search.assert_called_with(limit=1))

    def test_get_versions_since_if_version_in_payload(self):
        new_versions = check.get_new_versions(self.mock_obj, self.previous_version_payload)
        previous_version_target_id = int(self.previous_version_payload['version']['target'])
        self.assertIsNone(self.mock_obj.harbourmaster.target.search.assert_called_with(after=previous_version_target_id-1, order=['-id']))

    def test_correct_call_for_build_buildable_diff_ref(self):
        new_versions = check.get_new_versions(self.mock_obj, self.previous_version_payload)

        self.assertIsNone(self.mock_obj.harbourmaster.build.search.assert_called_with(constraints={'phids':["PHID-HMBD-roipk7qjjmwgbtvmzg3c"]}))
        self.assertIsNone(self.mock_obj.harbourmaster.buildable.search.assert_called_with(constraints={'phids':["PHID-HMBB-en7qg4hzo7gg2fuqlmry"]}))
        self.assertIsNone(self.mock_obj.differential.diff.search.assert_called_with(constraints={'phids':["PHID-DIFF-ya5b4a5urnyikincj6e5"]}))
        self.assertIsNone(self.mock_obj.differential.revision.search.assert_called_with(constraints={'phids':["PHID-DREV-d2s436jqt4pqsfucs6pm"]}))

    def test_correct_version_constructed(self):
        new_version = check.get_new_versions(self.mock_obj, self.previous_version_payload)[0]
        self.assertEqual(new_version.target, 2)
        self.assertEqual(new_version.diff, 932)
        self.assertEqual(new_version.branch, "arcpatch-D225_3")
        self.assertEqual(new_version.revision, "D225")

if __name__ == '__main__':
    unittest.main()
