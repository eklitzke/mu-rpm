#!/bin/bash
#
# Script to automatically update the mu.spec specfile with changes from git
# master.

set -eu

# path to the mu git directory
mudir=../mu

# the specfile
specfile=mu.spec

# the base mu version
muversion='1.1.0'

# prevent no-op changes
force=0

usage() { echo "usage: $(basename "$0") [-f] [-d DIRNAME] [-s SPECFILE] [-v MUVERSION]"; }

while getopts ":d:fhs:v:x" opt; do
  case $opt in
    d) mudir="$OPTARG" ;;
    f) force=1;;
    h) usage; exit 0 ;;
    s) specfile="$OPTARG" ;;
    v) muversion="$OPTARG" ;;
    x) set -x ;;
    \?) echo "Invalid option: -$OPTARG" >&2 ;;
  esac
done
shift "$((OPTIND-1))"

if ! pushd "$mudir" &>/dev/null; then
  echo "error: Failed to cd to dir $mudir" >&2
  exit 1
fi

# pull upstream changes
git pull -q

# get the long commit
gitcommit=$(git rev-parse HEAD)

# get the long date
gitdate=$(git log -1 --date=short --pretty=format:%cd | tr -d '-')

popd &>/dev/null

# reset spec file
git checkout -q "$specfile"

if [[ "$force" -eq 0 ]]; then
  oldversion=$(awk '/^%define gitcommit/ {print $3}' "$specfile")
  if [[ "$oldversion" = "$gitcommit" ]]; then
    echo "git commit is still ${gitcommit}, no changes necessary"
    exit
  fi
fi

# calculate a file checksum
cksum() { sha1sum "$specfile"; }

dosed() { sed -Ei "$1" "$specfile"; }

# run sed and ensure the file changed
runsed() {
  if [[ "$force" -eq 1 ]]; then
     dosed "$1"
     return
  fi
  orig=$(cksum)
  dosed "$1"
  if [[ $(cksum) == "$orig" ]]; then
    echo "error: after running sed $1 spec file did not change" >&2
    return 1
  fi
}

# run sed
runsed "s/^(%define gitcommit\s+)[0-9a-f]+$/\1${gitcommit}/"
runsed "s/^(%define gitdate\s+)[0-9]+$/\1${gitdate}/"

# Create a new version of the specfile with a new changelog entry. This is kind
# of gross as rpmdev-bumpspec should be able to do this, but I had some issues
# with how it interpreted the existing macros in the file, so this is what we
# have.
rewrite-specfile() {
  local IFS='' dateline commentline
  declare -i lineno=1
  dateline="* $(date '+%a %b %d %Y') $(rpmdev-packager) - ${muversion}-git${gitdate}.1"
  commentline="- Auto update with changes in master, new git commit ${gitcommit:0:8}"
  while read -r line; do
    printf '%s\n' "$line"
    if [[ "$line" == '%changelog' ]]; then
      echo "$dateline"
      echo "$commentline"
      echo
    elif [[ "$line" = "$dateline" ]]; then
      echo "error: found duplicate date line ${lineno}: ${dateline}" >&2
      return 1
    elif [[ "$line" = "$commentline" ]]; then
      echo "error: found duplicate commentline line ${lineno}: ${commentline}" >&2
      return 1
    fi
    ((lineno++))
  done <"$specfile"
}

tmpfile=$(mktemp)
trap 'rm -f ${tmpfile}' EXIT
if ! rewrite-specfile >"$tmpfile"; then
   echo "error: failed to rewrite spec file" >&2
   exit 1
fi
mv "$tmpfile" "$specfile"

echo "Showing output of git diff"
echo "---- START DIFF ----"
git diff "$specfile"
echo "---- END DIFF ----"
echo
echo "Please review the changes above before committing these changes."
