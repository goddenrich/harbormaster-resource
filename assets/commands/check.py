from phabricator import Phabricator
import phabricator
import json
from common import Source, Version, Diff, Rev, Target, Build, Buildable
from common import get_version_from_payload


# TODO(goddenrich) make this work if over max number returned by conduit
def get_targets_since(phab, target_id):
    if target_id:
        search = phab.harbormaster.target.search(order=['-id'], after=int(target_id)-1).get('data')
    else:
        search = phab.harbormaster.target.search(limit=1).get('data')
    return [Target(target_data) for target_data in search]

def get_build_from_PHID(phab, phid):
    return Build(phab.harbormaster.build.search(constraints={'phids': [phid]}).get('data')[0])

def get_buildable_from_PHID(phab, phid):
    return Buildable(phab.harbormaster.buildable.search(constraints={'phids': [phid]}).get('data')[0])

def get_diff_from_PHID(phab, phid):
    return Diff(phab.differential.diff.search(constraints={'phids': [phid]}).get('data')[0])

def get_rev_from_PHID(phab, phid):
    return Rev(phab.differential.revision.search(constraints={'phids': [phid]}).get('data')[0])

def get_build_from_target(phab, target):
    return get_build_from_PHID(phab, target.buildPHID)

def get_buildable_from_build(phab, build):
    return get_buildable_from_PHID(phab, build.buildablePHID)

def get_diff_from_buildable(phab, buildable):
    return get_diff_from_PHID(phab, buildable.objectPHID)

def get_rev_from_buildable(phab, buildable):
    return get_rev_from_PHID(phab, buildable.containerPHID)

def version_from_target(phab, target):
    build = get_build_from_target(phab, target)
    buildable = get_buildable_from_build(phab, build)
    diff = get_diff_from_buildable(phab, buildable)
    rev = get_rev_from_buildable(phab, buildable)
    return Version(target.id, diff.id, diff.branch, rev.id)

def get_new_versions(phab, payload):
    last_version = get_version_from_payload(payload)
    new_targets = get_targets_since(phab, last_version.target)
    return [version_from_target(phab, target) for target in new_targets]

if __name__ == "__main__":
    payload = json.loads(input())
    source = Source(payload)
    phab = Phabricator(host=source.conduit_uri, token=source.conduit_token)
    phab.update_interfaces()
    new_versions = get_new_versions(phab, payload)
    print(json.dumps(new_versions))
