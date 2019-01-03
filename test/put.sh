#!/bin/bash

set -e

# create test_gitconfig
echo '[phabricator]' > test_gitconfig
echo 'targetPHID = target-phid-config' >> test_gitconfig

# run tests
python /opt/resource/commands/test_out.py

echo -e "check tests passed!"
echo -e "--------------------------------------------"
