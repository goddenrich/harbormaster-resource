from phabricator import Phabricator
import phabricator
import json
from common import Source, Version, Diff, Target, Build, Buildable
from common import get_version_from_payload, versions_to_json


def _search_all_since(phab, target_id):
    after = int(target_id)-1
    data = []
    while after:
        result = phab.harbormaster.target.search(order=['-id'], after=int(after))
        data += result.get('data', [])
        after = result.get('cursor', {}).get('after')
    return data

def get_targets_since(phab, target_id):
    if target_id:
        search = _search_all_since(phab, target_id)
    else:
        #TODO(goddenrich) due to filtering on the buildStepPHID we may filter this out
        # need to handle this case to get the last target with the corect buildStepPHID
        search = phab.harbormaster.target.search(limit=1).get('data', [])
    return [Target(target_data) for target_data in search]

def _check_and_return_phid_search(response):
    data = response.get('data', [{}])
    return data if data else [{}]

# TODO(goddenrich) make these work when over 200 limit
def get_builds_from_PHIDs(phab, phids):
    none_stripped = [phid for phid in phids if phid is not None]
    response = phab.harbormaster.build.search(constraints={'phids': none_stripped}) if none_stripped else {}
    return [Build(build_data) for build_data in _check_and_return_phid_search(response)]

def get_buildables_from_PHIDs(phab, phids):
    none_stripped = [phid for phid in phids if phid is not None]
    response = phab.harbormaster.buildable.search(constraints={'phids': none_stripped}) if none_stripped else {}
    return [Buildable(buildable_data) for buildable_data in _check_and_return_phid_search(response)]

def get_diffs_from_PHIDs(phab, phids):
    none_stripped = [phid for phid in phids if phid is not None]
    response = phab.differential.diff.search(constraints={'phids': none_stripped}) if none_stripped else {}
    return [Diff(diff_data) for diff_data in _check_and_return_phid_search(response)]

def get_builds_from_targets(phab, targets):
    return get_builds_from_PHIDs(phab, [target.buildPHID for target in targets])

def get_buildables_from_builds(phab, builds):
    return get_buildables_from_PHIDs(phab, [build.buildablePHID for build in builds])

def get_diffs_from_buildables(phab, buildables):
    return get_diffs_from_PHIDs(phab, [buildable.objectPHID for buildable in buildables])

def versions_from_targets(phab, targets):
    builds = get_builds_from_targets(phab, targets)
    buildables = get_buildables_from_builds(phab, builds)
    diffs = get_diffs_from_buildables(phab, buildables)
    return [Version(target.id, target.phid, diff.id, diff.branch, diff.base) for target, diff in zip(targets, diffs)]

def get_new_versions(phab, payload, step=None):
    last_version = get_version_from_payload(payload)
    new_targets = get_targets_since(phab, last_version.target)
    if step:
        filtered_targets = [target for target in new_targets if target.buildStepPHID == step]
    else:
        filtered_targets = new_targets
    return versions_from_targets(phab, filtered_targets)

if __name__ == "__main__":
    payload = json.loads(input())
    source = Source(payload)
    phab = Phabricator(host=source.conduit_uri, token=source.conduit_token)
    phab.update_interfaces()
    new_versions = get_new_versions(phab, payload, source.buildStepPHID)
    print(json.dumps(versions_to_json(new_versions)))
