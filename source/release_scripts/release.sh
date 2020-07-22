DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )
VERSIONS_FILE="$DIR/../../version.txt"
echo "$DIR/../../version.txt"
MAJOR=$(cut -d "=" -f2 <<< $(sed -n '1p' < "$DIR/../../version.txt"))
MINOR=$(cut -d "=" -f2 <<< $(sed -n '2p' < "$DIR/../../version.txt"))
PATCH=$(cut -d "=" -f2 <<< $(sed -n '3p' < "$DIR/../../version.txt"))

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

    echo $MAJOR"."$MINOR"."$PATCH 
    echo -e $"MAJOR=$MAJOR\nMINOR=$MINOR\nPATCH=$PATCH" > VERSIONS_FILE
}

function create_release_archive ()
{
    archive_name="core-$MAJOR.$MINOR.$PATCH.tar.gz"
    cd $DIR
    ls
    echo "dir"
}

function main ()
{
    echo "Building version number..."
    build_version
    echo "Building release archive..."
    create_release_archive
}

main