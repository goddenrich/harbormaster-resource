import unittest
import check

class TestPayload(unittest.TestCase):
    def setUp(self):
        self.payload = {
            "source": {
                "conduit_uri": "https://test.conduit.uri/api/",
                "conduit_token": "test-conduit-token",
            },
            "version": {
                "build_target": "BTID",
                "diff": "diffID",
                "branch": "test-branch",
                "rev": "Dtestrev",
            }
        }
        self.version = check.Version(self.payload)
        self.source = check.Source(self.payload)

    def test_get_from_source(self):
        self.assertEqual(self.source.conduit_token, "test-conduit-token")
        self.assertEqual(self.source.conduit_uri, "https://test.conduit.uri/api/")

    def test_get_from_version(self):
        self.assertEqual(self.version.last_checked_target, "BTID")

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

if __name__ == '__main__':
    unittest.main()
