#!/bin/bash

LIST_CHANGED_FILES=()

# Fetch the base branch

function changes() {
    # See if anything changed when pull request
    CHANGES=$(git diff --name-only $GITHUB_BASE_REF..$GITHUB_HEAD_REF)
    echo "$CHANGES"
}

# SHOW CHANGED FILES THAT CAME FROM THE PULL REQUEST WHEN MERGING
function merged_changes() {
    # Run only when merged
    if [[ "$GITHUB_EVENT_NAME" != "push" ]]; then
        echo "Not merged. Skipping."
        exit 0
    fi
    # Get the reference of the branch that was merged
    MERGED_REF=$(jq -r '.pull_request.base.ref' < "$GITHUB_EVENT_PATH")

    # See if anything changed when pull request
    CHANGES=$(git diff --name-only $MERGED_REF..$GITHUB_HEAD_REF)
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