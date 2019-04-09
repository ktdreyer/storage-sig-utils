#!/bin/bash

set -eu

KOJI_PROFILE=cbs ansible-playbook --check -v cbs-nautilus.yml
