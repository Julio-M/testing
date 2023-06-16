#!/bin/bash

LIST_CHANGED_FILES=()

# Fetch the base branch

function changes() {
    # See what files have changed
    git diff --name-only ${{ github.base_ref }}...${{ github.head_ref }}
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