#!/bin/sh
# Blocks a commit or push that would publish private details.
# Checks text AND binary files (Blender files and PNG metadata can hold local paths).
# Usage: sh scripts/check-public.sh   (exit 1 = something found)
cd "$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
PAT='\.slack\.com/archives|/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/|/private/tmp/|gho_[A-Za-z0-9]{20}|ghp_[A-Za-z0-9]{20}|xox[bpas]-[A-Za-z0-9-]+|sk-[A-Za-z0-9]{20}|AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH|EC|DSA) PRIVATE KEY'
FILES=$( (git ls-files 2>/dev/null || find . -type f -not -path './.git/*') | grep -v '^scripts/check-public.sh$')
HITS=$(echo "$FILES" | tr '\n' '\0' | xargs -0 grep -laE "$PAT" 2>/dev/null)
if [ -n "$HITS" ]; then
  echo "check-public: private details found in:"; echo "$HITS"; exit 1
fi
echo "check-public: clean"
