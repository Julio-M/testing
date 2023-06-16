#!/bin/bash

# Check if now that is merged what files were changed
function changes() {
    # Check what changes were made in the latest commit
    local CHANGES=$(git diff-tree --no-commit-id --name-only -r $GITHUB_SHA)
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