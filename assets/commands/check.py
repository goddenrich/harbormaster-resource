from phabricator import Phabricator
import sys
import json

class Source:
    @staticmethod
    def _get_source_value_from_payload(value, payload):
        try:
            return payload['source'][value]
        except KeyError:
            raise KeyError(f'{value} not found')

    def __init__(self, payload):
        self.conduit_uri = self._get_source_value_from_payload('conduit_uri', payload)
        self.conduit_token = self._get_source_value_from_payload('conduit_token', payload)

class Version:
    @staticmethod
    def _get_version_value_from_payload(value, payload):
        try:
            return payload['version'][value]
        except KeyError:
            return None
    def __init__(self, payload):
        self.last_checked_target = self._get_version_value_from_payload('build_target', payload)

    def get_new_targets(self, phab):
        if self.last_checked_target:
            return phab.get_targets_since(self.last_checked_target)
        else:
            return phab.get_latest_target()

class Target:
    def __init__(self, data):
        self.id = data.get('id')
        self.phid = data.get('phid')
        self.buildPHID = data.get('fields',{}).get('buildPHID')
        self.status = data.get('fields',{}).get('status')

class Build:
    def __init__(self, data):
        self.id = data.get('id')
        self.phid = data.get('phid')
        self.buildablePHID = data.get('fields',{}).get('buildablePHID')

class Buildable:
    def __init__(self, data):
        self.id = data.get('id')
        self.phid = data.get('phid')
        self.objectPHID = data.get('fields', {}).get('objectPHID')
        self.containerPHID = data.get('fields', {}).get('containerPHID')

if __name__ == "__main__":
    payload = json.loads(input())
    phab = get_phabricator(payload)
    last_checked_diff = get_last_diff_checked(payload)
    repo_PHID = get_repo_PHID(payload, phab)
    new_versions = get_new_versions(last_checked_diff, repo_PHID, phab)
    print(json.dumps(new_versions))
