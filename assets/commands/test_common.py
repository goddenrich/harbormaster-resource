import unittest
import common

class TestPayload(unittest.TestCase):
    def setUp(self):
        self.payload = {
            "source": {
                "conduit_uri": "https://test.conduit.uri/api/",
                "conduit_token": "test-conduit-token",
                "buildStepPHID": "test-step",
            },
            "version": {
                "target": "5",
                "targetPHID": "BTID",
                "diff": "diffID",
                "branch": "test-branch",
                "base": "baseref"
            }
        }
        self.version = common.get_version_from_payload(self.payload)
        self.source = common.Source(self.payload)

    def test_get_from_source(self):
        self.assertEqual(self.source.conduit_token, "test-conduit-token")
        self.assertEqual(self.source.conduit_uri, "https://test.conduit.uri/api/")
        self.assertEqual(self.source.buildStepPHID, "test-step")

    def test_get_version_from_payload(self):
        self.assertEqual(self.version.target, "5")
        self.assertEqual(self.version.targetPHID, "BTID")
        self.assertEqual(self.version.diff, "diffID")
        self.assertEqual(self.version.branch, "test-branch")
        self.assertEqual(self.version.base, "baseref")

class TestVersion(unittest.TestCase):
    def setUp(self):
        self.version = common.Version('t', 'p', 'd', 'b', 'ba')
        self.one_return = {'branch': 'b', 'base': 'ba', 'diff': 'd', 'target': 't', 'targetPHID': 'p'}

    def test_repr(self):
        self.assertDictEqual(self.version.dict(), self.one_return)
    def test_one_version_to_json(self):
        self.assertListEqual(common.versions_to_json([self.version]), [self.one_return])

    def test_multiple_versions_to_json(self):
        self.assertListEqual(common.versions_to_json([self.version, self.version]), [self.one_return, self.one_return])

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
        self.target = common.Target(self.target_data)
    
    def test_init(self):
        self.assertEqual(self.target.id, 2)
        self.assertEqual(self.target.phid, "PHID-HMBT-n6rbr4r5djx2o4wii7fm")
        self.assertEqual(self.target.buildPHID, "PHID-HMBD-roipk7qjjmwgbtvmzg3c")
        self.assertDictEqual(self.target.status, {"value": "target/failed", "name": "Failed"})
        self.assertEqual(self.target.buildStepPHID, "PHID-HMCS-kzlrqdivjddl6ervz7zu")

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
        self.build = common.Build(self.build_data)

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
        self.buildable = common.Buildable(self.buildable_data)

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
        self.diff = common.Diff(self.diff_data)

    def test_init(self):
        self.assertEqual(self.diff.id, 932)
        self.assertEqual(self.diff.branch, "arcpatch-D225_3")
        self.assertEqual(self.diff.base, "5666cdb29e45042565d921b0672f07814aacc06f")


if __name__ == '__main__':
    unittest.main()
