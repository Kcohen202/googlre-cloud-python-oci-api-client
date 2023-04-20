#!/bin/bash
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# This script was written as part of a project to migrate
# split repositories to the mono-repository google-cloud-python.
#
# This script will update the various metadata files migrated from the split
# repo into formats and locations suitable for the mono-repo.
#
# Pre-condition: the split repo has been copied to the path indicated when
# calling this function.
#
# INVOCATION from the mono-repo root directory:
#   split-repo-post-process.sh PACKAGE_PATH
# where PACKAGE_PATH is the path (absolute or relative) from pwd to the
# directory in google-cloud-python holding the copied split repo. Typically, if
# running from the top level of google-cloud-python, this is something like
# "packages/google-cloud-APINAME"
# EXAMPLE from the root directory of the monorepo:
#   ./scripts/split_repo_migration/split-repo-post-process.sh packages/google-cloud-speech
#
# For debugging/developing this script, you can have additional parameters:
#  ./split-repo-post-process.sh SPLIT_REPO_DIR MONOREPO_DIR MONOREPO_PACKAGE_NAME
# Example from this script's directory:
#  ./split-repo-post-process.sh ../../../python-speech ../../ google-cloud-speech

# sourced vs execution detection obtained from https://stackoverflow.com/a/28776166
local SOURCED=0
if [ -n "$ZSH_VERSION" ]; then 
  case $ZSH_EVAL_CONTEXT in *:file) SOURCED=1;; esac
elif [ -n "$KSH_VERSION" ]; then
  [ "$(cd -- "$(dirname -- "$0")" && pwd -P)/$(basename -- "$0")" != "$(cd -- "$(dirname -- "${.sh.file}")" && pwd -P)/$(basename -- "${.sh.file}")" ] && SOURCED=1
elif [ -n "$BASH_VERSION" ]; then
  (return 0 2>/dev/null) && SOURCED=1 
else # All other shells: examine $0 for known shell binary filenames.
     # Detects `sh` and `dash`; add additional shell filenames as needed.
  case ${0##*/} in sh|-sh|dash|-dash) SOURCED=1;; esac
fi

(( SOURCED != 1 )) || { \
  echo "Please do not source this script, but execute it directly."
  return -10
}

# We require executing the script so that an early exit (explicitly or via -e)
# does not kill the user's shell.
                                     
# `-e` enables the script to automatically fail when a command fails
set -e


NOP="echo -n"
DEBUG=""  # "yes"  # set to blank for a real run, or non-blank to prevent modifying the split-repo
MESSAGE=""

[[ -n ${DEBUG} ]] && {
  # Comment out some commands for development/debugging
  RM='echo "*** would run:" rm'
  GIT='echo "*** would run:" git'

  # It's easier to debug if keys don't get reordered
  SORT_JSON_KEYS="" 
} || {
  # Real commands for actual runs
  RM='rm'
  GIT='git'

  # Sort keys for easier look-up.
  SORT_JSON_KEYS="--sort-keys"
}

if [ $# -lt 1 ]
then
  echo "Usage: $0 PATH/TO/PACKAGE_NAME"
  exit 1
fi

# variable naming convention
#   PATH_* are absolute system paths
#   MONOREPO_PATH_* are paths relative to the root of the monorepo
#   MONOREPO_* are values used in the monorepo

# In a real run for a split repo already copied to the mono-repo, $1 would be
# specified as `packages/PACKAGE_NAME`. For developing this script, it's useful
# to specify $1 as the name of a completely separate split repo, in which case
# specifying $2 and $3 is also useful (see below).
PATH_PACKAGE="$(realpath "$1")"

# The optional second argument is useful for development: it specifies a different
# directory for the monorepo (rather than deriving it from $1).
PATH_MONOREPO="${2:-$(dirname $(dirname $PATH_PACKAGE))}"
PATH_MONOREPO="$(realpath "${PATH_MONOREPO}")"

# The optional third argument is useful for development: it specifies what the the
# package name should be for this API once migrated to the monorepo. This can be
# inferred if we've already migrated the split repo to the correct location, but
# otherwise needs to be specified, since it differs from the split repo name
# (for example, the repo "python-speech" defines a package
# "google-cloud-speech").
MONOREPO_PACKAGE_NAME="${3:-$(basename ${PATH_PACKAGE})}"

MONOREPO_PATH_PACKAGE="packages/${MONOREPO_PACKAGE_NAME}"

cat <<EOF
Post-processing ${MONOREPO_PACKAGE_NAME}
  PATH_PACKAGE:          ${PATH_PACKAGE}
  PATH_MONOREPO:         ${PATH_MONOREPO}
  MONOREPO_PACKAGE_NAME: ${MONOREPO_PACKAGE_NAME}
  MONOREPO_PATH_PACKAGE: ${MONOREPO_PATH_PACKAGE}
EOF

pushd "${PATH_MONOREPO}" >& /dev/null

## START system tests check ########################################
# variable prefix: TST_*

# If there are integration tests, do not proceed with the script.

TST_MONO_TESTDIR="${MONOREPO_PATH_PACKAGE}/tests/"
TST_MONO_SYSTEM_DIR="${TST_MONO_TESTDIR}system"
TST_MONO_SYSTEM_FILE="${TST_MONO_TESTDIR}system.py"
echo "Checking for system tests in ${TST_MONO_TESTDIR}"

[[ ! -f ${TST_MONO_SYSTEM_FILE} ]] || \
  { echo "ERROR: ${TST_MONO_SYSTEM_FILE} exists. Need to manually deal with that." ; return -10 ; }
[[ ! -d ${TST_MONO_SYSTEM_DIR} ]] || \
  { echo "ERROR: ${TST_MONO_SYSTEM_DIR} exists. Need to manually deal with that." ; return -11 ; }
## END system tests check

## START owlbot.yaml migration ########################################
# variable prefix: OWY_*
# FIXME: KEEP?
OWY_MONO_PATH="${MONOREPO_PATH_PACKAGE}/.OwlBot.yaml"
echo "Migrating: ${OWY_MONO_PATH}"
mkdir -p $(dirname ${OWY_MONO_PATH})

OWY_SPLIT_PATH="${PATH_PACKAGE}/.github/.OwlBot.yaml"
cp ${OWY_SPLIT_PATH} ${OWY_MONO_PATH}

# remove `docker:` line
sed -i "/docker:/d" "${OWY_MONO_PATH}"
# remove `image:` line
sed -i "/image:/d" "${OWY_MONO_PATH}"

# In the nodejs case, lines #1 and #2 below are treated as a disjoint case from
# line #3. However, in Python we see cases (eg aiplatform) where there are
# multiple entries in the same file that satisfy either of the criteria. As a
# result, we search for both cases. In doing that, to prevent #3 from altering
# lines already modified by #2, we temporarily insert ${TMP_MARKER} and remove
# it in #4
TMP_MARKER="<<__tmp__>>>"
sed -i 's|\.\*-py/(.*)|.*-py|' "${OWY_MONO_PATH}"   #1
sed -i "s|dest: /owl-bot-staging/\$1/\$2|dest: /owl-bot-${TMP_MARKER}staging/${MONOREPO_PACKAGE_NAME}/\$1|" "${OWY_MONO_PATH}" #2
sed -i "s|dest: /owl-bot-staging|dest: \/owl-bot-staging\/${MONOREPO_PACKAGE_NAME}/|" "${OWY_MONO_PATH}" #3
sed -i "s|${TMP_MARKER}||" "${OWY_MONO_PATH}"  #4

# TODO: Review the following: For consistency with NodeJS migration script:
# - we are not removing `begin-after-commit-hash`
# - we are not removing `deep-remove-regex`, even though it refers to a non-API-specific directory.

$RM ${OWY_SPLIT_PATH}
## END owlbot.yaml migration


## START owlbot.py migration ########################################
# variable prefix: OWP_*
OWP_MONO_PATH="${MONOREPO_PATH_PACKAGE}/owlbot.py"
echo "Migrating: ${OWP_MONO_PATH}"

[[ -z ${DEBUG} ]] || { \
  OWP_SPLIT_PATH="${PATH_PACKAGE}/owlbot.py"
  [[ ! -f "${OWP_SPLIT_PATH}" ]] || cp -u ${OWP_SPLIT_PATH} ${OWP_MONO_PATH}
}

[[ ! -f "${OWP_MONO_PATH}" ]] || {
  MESSAGE="${MESSAGE}\n\nWARNING: Deleted ${OWP_MONO_PATH}"
  rm -rf "${OWP_MONO_PATH}"
}
## END owlbot.py migration

## START delete doc/changelog.md ###################################
rm -f "${MONOREPO_PATH_PACKAGE}/docs/changelog.md"
## END delete doc/changelog.md #####################################


## START commit changes #############################################
echo "Committing changes locally"
${GIT} add .
${GIT} commit -am "build: ${MONOREPO_PACKAGE_NAME} migration: adjust owlbot-related files"
## END commit changes

popd >& /dev/null # "${PATH_MONOREPO}"

[[ -z ${MESSAGE} ]] && echo "Done." || echo -e "Done, with a message:\n\n${MESSAGE}\n"



