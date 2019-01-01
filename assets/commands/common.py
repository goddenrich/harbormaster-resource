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

def get_version_from_payload(payload):
    version = payload.get('version', {}) or {}
    target_id = version.get('target')
    diff_id = version.get('diff')
    branch = version.get('branch')
    revision_id = version.get('revision_id')
    return Version(target_id, diff_id, branch, revision_id)

class Version:
    def __init__(self, target_id, diff_id, branch, revision_id):
        self.target = target_id
        self.diff = diff_id
        self.branch = branch
        self.revision = 'D' + str(revision_id)

    def dict(self):
        return self.__dict__

def versions_to_json(versions):
    return [version.dict() for version in versions]

class Diff:
    def __init__(self, data):
        self.id = data.get('id')
        self.revisionPHID = data.get('fields',{}).get('revisionPHID')
        
        def get_branch(refs):
            for ref in refs:
                if ref.get('type') == "branch":
                    return ref.get('name')

        self.branch = get_branch(data.get('fields', {}).get('refs', []))

class Rev:
    def __init__(self, data):
        self.id = data.get('id')

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
