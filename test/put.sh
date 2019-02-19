#!/bin/bash

set -e

# create test_gitconfig
echo '[phabricator]' > test_gitconfig
echo 'targetPHID = target-phid-config' >> test_gitconfig
echo 'base = test-base' >> test_gitconfig
echo 'branch = test-branch' >> test_gitconfig
echo 'diff = 123' >> test_gitconfig
echo 'target = 1' >> test_gitconfig


# run tests
python /opt/resource/commands/test_out.py

echo -e "check tests passed!"
echo -e "--------------------------------------------"
