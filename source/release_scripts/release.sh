#!/bin/bash

DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

VERSION=$((curl -sb -H "Accept: application/json" "$VERSIONING_CONTROLLER_GET_URL") | jq -r '.version')

MAJOR=$(cut -d'.' -f1 <<<$VERSION)
MINOR=$(cut -d'.' -f2 <<<$VERSION)
PATCH=$(cut -d'.' -f3 <<<$VERSION)

function build_version ()
{
    if ((PATCH < 20)); then
        PATCH=$((PATCH+1))
    elif ((MINOR < 20)); then
        MINOR=$((MINOR+1))
        PATCH=0
    else
        MAJOR=$((MAJOR+1))
        MINOR=0
        PATCH=0
    fi
}

function create_release_archive ()
{
    echo "core-$MAJOR.$MINOR.$PATCH.tar.gz"
    archive_name="core-$MAJOR.$MINOR.$PATCH.tar.gz"
    tar -czf $DIR/release/$archive_name $DIR/../../../heimdall-framework
}

function main ()
{
    echo "Building version number..."
    build_version
    echo "Building release archive..."
    create_release_archive
    echo "Exporting old version number..."
    export VERSION=$VERSION
}

main
