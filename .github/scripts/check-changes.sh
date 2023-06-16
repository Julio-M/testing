#!/bin/bash

LIST_CHANGED_FILES=()

# Fetch the base branch

function changes() {
    # See if anything changed when pull request
    CHANGES=$(git diff --name-only $GITHUB_BASE_REF..$GITHUB_HEAD_REF)
    echo "$CHANGES"
}


function check_changes() {
  local CHANGES=$(changes)
  if [[ -z "$CHANGES" ]]; then
    echo "No changes detected"
    exit 0
  fi
  echo "Changes detected"
  echo "$CHANGES"
  LIST_CHANGED_FILES=($CHANGES)
}

check_changes