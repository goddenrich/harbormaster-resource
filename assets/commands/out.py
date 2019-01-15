from phabricator import Phabricator
import configparser
import json
from common import Source, Version, Diff, Rev, Target, Build, Buildable
from common import get_version_from_payload, versions_to_json

GIT_CONFIG_FILE = '.git/config'

def get_version_from_git_config(git_config):
    config = configparser.ConfigParser()
    config.read(git_config)
    base = config.get('phabricator', option='base')
    branch = config.get('phabricator', option='branch')
    diff = config.get('phabricator', option='diff')
    revision = config.get('phabricator', option='revision')[1:] # remove D from start
    target = config.get('phabricator', option='target')
    targetPHID = config.get('phabricator', option='targetphid')
    return Version(target, targetPHID, diff, branch, base, revision)

def get_build_status_from_payload(payload):
    params = payload.get('params', {}) or {}
    return params.get('build_status')

def update_phabricator_with_build_status(phab, targetPHID, build_status):
    phab.harbormaster.sendmessage(buildTargetPHID=targetPHID, type = build_status)

def out_output_from_version(version):
    return {"version": version.dict()}

if __name__ == "__main__":
    payload = json.loads(input())
    source = Source(payload)
    phab = Phabricator(host=source.conduit_uri, token=source.conduit_token)
    phab.update_interfaces()
    build_status = get_build_status_from_payload(payload)
    version = get_version_from_git_config(GIT_CONFIG_FILE)
    update_phabricator_with_build_status(phab, version.targetPHID, build_status)
    print(json.dumps(out_output_from_version(version)))
