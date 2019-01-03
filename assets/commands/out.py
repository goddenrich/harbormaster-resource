from phabricator import Phabricator
import phabricator
import json
from common import Source, Version, Diff, Rev, Target, Build, Buildable
from common import get_version_from_payload, versions_to_json

def get_build_status_from_payload(payload):
    params = payload.get('params', {}) or {}
    return params.get('build_status')

def update_phabricator_with_build_status(phab, targetPHID, build_status):
    phab.harbormaster.sendmessage(buildTargetPHID=targetPHID, type = build_status)

def get_target_phid_from_git_config():
    pass

if __name__ == "__main__":
    payload = json.loads(input())
    source = Source(payload)
    phab = Phabricator(host=source.conduit_uri, token=source.conduit_token)
    phab.update_interfaces()
    build_status = get_build_status_from_payload(payload)
    targetPHID = get_target_phid_from_git_config()
    update_phabricator_with_build_status(phab, build_status)
    print(json.dumps(versions_to_json(version)))

