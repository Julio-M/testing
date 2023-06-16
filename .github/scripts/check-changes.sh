#!/bin/bash

LIST_CHANGED_FILES=()

# Fetch the base branch

function changes() {
  local CHANGES=$(git diff --name-only --diff-filter=d origin/$GITHUB_BASE_REF..origin/$GITHUB_HEAD_REF)
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