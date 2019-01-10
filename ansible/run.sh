#!/bin/bash

set -eu

KOJI_PROFILE=cbs PYTHONPATH=library/ ansible-playbook -v cbs-nautilus.yml
