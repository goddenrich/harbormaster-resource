import unittest
import check
from unittest.mock import patch

class TestPayload(unittest.TestCase):
    def setUp(self):
        self.payload = {
            "source": {
                "conduit_uri": "https://test.conduit.uri/api/",
                "conduit_token": "test-conduit-token",
            },
            "version": {
                "target": "BTID",
                "diff": "diffID",
                "branch": "test-branch",
                "revision_id": "testrev",
            }
        }
        self.version = check.get_version_from_payload(self.payload)
        self.source = check.Source(self.payload)

    def test_get_from_source(self):
        self.assertEqual(self.source.conduit_token, "test-conduit-token")
        self.assertEqual(self.source.conduit_uri, "https://test.conduit.uri/api/")

    def test_get_version_from_payload(self):
        self.assertEqual(self.version.target, "BTID")
        self.assertEqual(self.version.diff, "diffID")
        self.assertEqual(self.version.branch, "test-branch")
        self.assertEqual(self.version.revision, "Dtestrev")

class TestVersion(unittest.TestCase):
    def setUp(self):
        self.version = check.Version('t', 'd', 'b', 'r')
    
    def test_repr(self):
        self.assertDictEqual(self.version.__repr__(), {'target': 't', 'diff': 'd', 'branch': 'b', 'revision': 'Dr'})

class TestTarget(unittest.TestCase):
    def setUp(self):
        self.target_data = {
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
        }
        self.target = check.Target(self.target_data)
    
    def test_init(self):
        self.assertEqual(self.target.id, 2)
        self.assertEqual(self.target.phid, "PHID-HMBT-n6rbr4r5djx2o4wii7fm")
        self.assertEqual(self.target.buildPHID, "PHID-HMBD-roipk7qjjmwgbtvmzg3c")
        self.assertDictEqual(self.target.status, {"value": "target/failed", "name": "Failed"})

class TestBuild(unittest.TestCase):
    def setUp(self):
        self.build_data = {
            "id": 1,
            "type": "HMBD",
            "phid": "PHID-HMBD-roipk7qjjmwgbtvmzg3c",
            "fields": {
                "buildablePHID": "PHID-HMBB-en7qg4hzo7gg2fuqlmry",
                "buildPlanPHID": "PHID-HMCP-4aa3uulqroxhzdkl7nxc",
                "buildStatus": {
                    "value": "failed",
                    "name": "Failed",
                    "color.ansi": "red"
                },
                "initiatorPHID": "PHID-HRUL-dquvj55z6gjmde6hvted",
                "name": "concourse",
                "dateCreated": 1545663372,
                "dateModified": 1545663456,
                "policy": {
                    "view": "users",
                    "edit": "users"
                }
            },
            "attachments": {}
        }
        self.build = check.Build(self.build_data)

    def test_init(self):
        self.assertEqual(self.build.id, 1)
        self.assertEqual(self.build.phid, "PHID-HMBD-roipk7qjjmwgbtvmzg3c")
        self.assertEqual(self.build.buildablePHID, "PHID-HMBB-en7qg4hzo7gg2fuqlmry")

class TestBuildable(unittest.TestCase):
    def setUp(self):
        self.buildable_data = {
            "id": 1,
            "type": "HMBB",
            "phid": "PHID-HMBB-en7qg4hzo7gg2fuqlmry",
            "fields": {
                "objectPHID": "PHID-DIFF-ya5b4a5urnyikincj6e5",
                "containerPHID": "PHID-DREV-d2s436jqt4pqsfucs6pm",
                "buildableStatus": {
                    "value": "failed"
                },
                "isManual": False,
                "dateCreated": 1545663372,
                "dateModified": 1545663456,
                "policy": {
                    "view": "users",
                    "edit": "users"
                }
            },
            "attachments": {}
        }
        self.buildable = check.Buildable(self.buildable_data)

    def test_init(self):
        self.assertEqual(self.buildable.id, 1)
        self.assertEqual(self.buildable.phid, "PHID-HMBB-en7qg4hzo7gg2fuqlmry")
        self.assertEqual(self.buildable.objectPHID, "PHID-DIFF-ya5b4a5urnyikincj6e5")
        self.assertEqual(self.buildable.containerPHID, "PHID-DREV-d2s436jqt4pqsfucs6pm")


class TestDiff(unittest.TestCase):
    def setUp(self):
        self.diff_data = {
            "id": 932,
            "type": "DIFF",
            "phid": "PHID-DIFF-zbyph2rdona74vcgsu2g",
            "fields": {
                "revisionPHID": "PHID-DREV-lyl4plyiheajccqjkmo6",
                "authorPHID": "PHID-USER-oyjs33qezlnmaakylm3q",
                "repositoryPHID": "PHID-REPO-ayaleo55nfry53ns7x4m",
                "refs": [
                    {
                        "type": "branch",
                        "name": "arcpatch-D225_3"
                    },
                    {
                        "type": "base",
                        "identifier": "5666cdb29e45042565d921b0672f07814aacc06f"
                    }
                ],
                "dateCreated": 1544961500,
                "dateModified": 1544961502,
                "policy": {
                    "view": "public"
                }
            },
            "attachments": {}
        }
        self.diff = check.Diff(self.diff_data)

    def test_init(self):
        self.assertEqual(self.diff.id, 932)
        self.assertEqual(self.diff.revisionPHID, "PHID-DREV-lyl4plyiheajccqjkmo6")
        self.assertEqual(self.diff.branch, "arcpatch-D225_3")

class TestRev(unittest.TestCase):
    def setUp(self):
        self.rev_data = {
                "id": 225,
                "type": "DREV",
                "phid": "PHID-DREV-lyl4plyiheajccqjkmo6",
                "fields": {
                    "title": "Upgrade from php 5 to php 7",
                    "authorPHID": "PHID-USER-oyjs33qezlnmaakylm3q",
                    "status": {
                        "value": "needs-review",
                        "name": "Needs Review",
                        "closed": False,
                        "color.ansi": "magenta"
                    },
                    "repositoryPHID": "PHID-REPO-ayaleo55nfry53ns7x4m",
                    "diffPHID": "PHID-DIFF-btkzxcucrjcz5feorcuv",
                    "summary": "As PHP5 gets EOL in 2018, see T2366",
                    "dateCreated": 1544179006,
                    "dateModified": 1544965192,
                    "policy": {
                        "view": "users",
                        "edit": "users"
                    }
                },
                "attachments": {}
        }
        self.rev = check.Rev(self.rev_data)
            
    def test_init(self):
        self.assertEqual(self.rev.id, 225)


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