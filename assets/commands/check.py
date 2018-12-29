from phabricator import Phabricator
import sys
import json
from common import Source, Version, Diff, Rev, Target, Build, Buildable
from common import get_version_from_payload


class Phabricator(Phabricator):
    def __init__(self, conduit_url, conduit_token):
        self.__init__(host=conduit_uri, token=conduit_token)
        self.update_interfaces()

    def get_latest_target(self):
        return Target(self.harbourmaster.target.search(limit=1).get('data'))

    # TODO(goddenrich) make this work if over max number returned by conduit
    def get_targets_since(self, target_id):
        return [Target(target_data) for target_data in self.harbourmaster.target.search(order=['-id'], after=int(target_id)-1).get('data')]

    def get_build_from_PHID(self, phid):
        return Build(self.harbourmaster.build.search(constraints={'phids': [phid]}).get('data')[0])

    def get_buildable_from_PHID(self, phid):
        return Buildable(self.harbourmaster.buildable.search(constraints={'phids': [phid]}).get('data')[0])

    def get_diff_from_PHID(self, phid):
        return Diff(self.differential.diff.search(constraints={'phids': [phid]}).get('data')[0])

    def get_rev_from_PHID(self, phid):
        return Rev(self.differential.revision.search(constraints={'phids': [phid]}).get('data')[0])

    def get_build_from_target(self, target):
        return self.get_build_from_PHID(target.buildPHID)

    def get_buildable_from_build(self, build):
        return self.get_buildable_from_PHID(build.buildablePHID)

    def get_diff_from_buildable(self, buildable):
        return self.get_diff_from_PHID(buildable.objectPHID)

    def get_rev_from_buildable(self, buildable):
        return self.get_rev_from_PHID(buildable.containerPHID)

    def get_diff_rev_from_target(self, target):
        build = self.get_build_from_target(target)
        buildable = self.get_buildable_from_build(build)
        return target, self.get_diff_from_buildable(buildable), self.get_rev_from_buildable(buildable)

def version_from_target_diff_rev(target, diff, rev):
    return Version(target.id, diff.id, diff.branch, rev.id)

def get_new_versions(payload, phab):
    last_version = get_version_from_payload(payload)
    if last_version is None:
        new_targets = phab.get_latest_target()
    else:
        new_targets = phab.get_targets_since(last_version.target_id)
    return [version_from_target_diff_rev(get_target_diff_rev_from_target(target)) for target in new_targets]



if __name__ == "__main__":
    payload = json.loads(input())
    source = Source(payload)
    phab = Phabricator(conduit_uri=source.conduit_uri, conduit_token = source.conduit_token)
    new_versions = get_new_versions(payload, phab)
    print(json.dumps(new_versions))
