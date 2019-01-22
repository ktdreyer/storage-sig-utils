#!/bin/bash

set -eu

KOJI_PROFILE=cbs ansible-playbook -v cbs-nautilus.yml
