import unittest
import check
from unittest import mock


class TestPhabricator(unittest.TestCase):
    @mock.patch('check.Phabricator')
    def setUp(self, mock_phab):
        self.mock_obj = mock_phab.return_value = mock.Mock()
        target_response = {
            'data':
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
        build_response = {
            'data':
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
        buildable_response = {
            'data':
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
        diff_response = {
            'data':
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
                                {
                                    "type": "base",
                                    "identifier": "base_ref"
                                },
                            ],
                        },
                    }
                ]
        }
        rev_response = {
            'data':
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
        self.none_version_payload = {
            'source': {
                "conduit_uri": "https://test.conduit.uri/api/",
                "conduit_token": "test-conduit-token",
            },
            'version': None
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
        self.mock_obj.harbormaster.target.search.return_value = target_response
        self.mock_obj.harbormaster.build.search.return_value = build_response
        self.mock_obj.harbormaster.buildable.search.return_value = buildable_response
        self.mock_obj.differential.diff.search.return_value = diff_response
        self.mock_obj.differential.revision.search.return_value = rev_response


    def test_get_latest_if_no_version_in_payload(self):
        new_versions = check.get_new_versions(self.mock_obj, self.no_version_payload)
        self.assertIsNone(self.mock_obj.harbormaster.target.search.assert_called_with(limit=1))

    def test_get_latest_if_empty_version_in_payload(self):
        new_versions = check.get_new_versions(self.mock_obj, self.empty_version_payload)
        self.assertIsNone(self.mock_obj.harbormaster.target.search.assert_called_with(limit=1))

    def test_get_latest_if_none_version_in_payload(self):
        new_versions = check.get_new_versions(self.mock_obj, self.none_version_payload)
        self.assertIsNone(self.mock_obj.harbormaster.target.search.assert_called_with(limit=1))

    def test_get_versions_since_if_version_in_payload(self):
        new_versions = check.get_new_versions(self.mock_obj, self.previous_version_payload)
        self.assertIsNone(self.mock_obj.harbormaster.target.search.assert_called_with(after=4, order=['-id']))

    def test_get_versions_since_filters_build_step_phid(self):
        target_response = {
            'data':
                [
                    {
                        "id": 2,
                        "phid": "should-get-this-PHID",
                        "fields": {
                            "buildPHID": "PHID-HMBD-roipk7qjjmwgbtvmzg3c",
                            "buildStepPHID": "should-remain",
                        },
                    },
                    {
                        "id": 3,
                        "phid": "should-not-get-this-PHID",
                        "fields": {
                            "buildPHID": "PHID-HMBD-roipk7qjjmwgbtvmzg3c",
                            "buildStepPHID": "should-be-filtered-out",
                        },
                    }
                ]
        }
        self.mock_obj.harbormaster.target.search.return_value = target_response
        new_versions = check.get_new_versions(self.mock_obj, self.previous_version_payload, 'should-remain')
        target_ids = [version.target for version in new_versions]
        self.assertListEqual(target_ids, ['2'])
    
    def test_correct_call_for_build_buildable_diff_ref(self):
        new_versions = check.get_new_versions(self.mock_obj, self.previous_version_payload)

        self.assertIsNone(self.mock_obj.harbormaster.build.search.assert_called_with(constraints={'phids':["PHID-HMBD-roipk7qjjmwgbtvmzg3c"]}))
        self.assertIsNone(self.mock_obj.harbormaster.buildable.search.assert_called_with(constraints={'phids':["PHID-HMBB-en7qg4hzo7gg2fuqlmry"]}))
        self.assertIsNone(self.mock_obj.differential.diff.search.assert_called_with(constraints={'phids':["PHID-DIFF-ya5b4a5urnyikincj6e5"]}))
        self.assertIsNone(self.mock_obj.differential.revision.search.assert_called_with(constraints={'phids':["PHID-DREV-d2s436jqt4pqsfucs6pm"]}))

    def test_correct_version_constructed(self):
        new_version = check.get_new_versions(self.mock_obj, self.previous_version_payload)[0]
        self.assertEqual(new_version.target, "2")
        self.assertEqual(new_version.targetPHID, "PHID-HMBT-n6rbr4r5djx2o4wii7fm")
        self.assertEqual(new_version.diff, "932")
        self.assertEqual(new_version.branch, "arcpatch-D225_3")
        self.assertEqual(new_version.revision, "D225")
        self.assertEqual(new_version.base, "base_ref")

    def test_check_and_return_one_item_from_phid_search(self):
        empty_response = {}
        data_empty = {'data': []}
        one_item = {'data': [{'one_item': 'value'}]}
        two_items = {'data': [{'1':'value1'}, {'2':'value2'}]}
        self.assertDictEqual(check._check_and_return_one_item_from_phid_search(empty_response), {})
        self.assertDictEqual(check._check_and_return_one_item_from_phid_search(data_empty), {})
        self.assertDictEqual(check._check_and_return_one_item_from_phid_search(one_item), {'one_item': 'value'})
        with self.assertRaises(ValueError):
            check._check_and_return_one_item_from_phid_search(two_items)

    def test_phids_none_in_search(self):
        self.assertDictEqual(check.get_build_from_PHID(self.mock_obj, None).__dict__, check.Build({}).__dict__)
        self.assertDictEqual(check.get_buildable_from_PHID(self.mock_obj, None).__dict__, check.Buildable({}).__dict__)
        self.assertDictEqual(check.get_rev_from_PHID(self.mock_obj, None).__dict__, check.Rev({}).__dict__)
        self.assertDictEqual(check.get_diff_from_PHID(self.mock_obj, None).__dict__, check.Diff({}).__dict__)


if __name__ == '__main__':
    unittest.main()
