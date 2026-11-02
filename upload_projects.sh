#!/usr/bin/env bash
# Run this from INSIDE the unzipped robotics-projects folder.
# 1. Create an EMPTY repo on github.com first (no README, no .gitignore).
# 2. Paste its URL below, then run:  bash upload_projects.sh

REPO_URL="https://github.com/agbani885/robotics-projects.git"

set -e

if [[ "$REPO_URL" == *YOUR-USERNAME* ]]; then
  echo "Edit this script first and put your real repo URL in REPO_URL."
  exit 1
fi

git init
git branch -M main
git remote add origin "$REPO_URL"

git add README.md .gitignore
git commit -m "Initial commit: README and .gitignore"
git push -u origin main

add_project () {
  git add "$1"/
  git commit -m "$2"
  git push
}

add_project lie-algebra            "Add Lie algebra project"
add_project recursive-bayes-filter "Add recursive Bayes filter project"
add_project mapping                "Add occupancy grid mapping project"
add_project particle-filters       "Add Monte Carlo localization project"
add_project icp                    "Add ICP project"
add_project bundle-adjustment      "Add bundle adjustment project"
add_project python3-for-robotics   "Add Python3 for Robotics project"

echo "Done. Check your repo on GitHub."
