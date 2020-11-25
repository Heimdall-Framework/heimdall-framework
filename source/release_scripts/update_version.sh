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

function update_versioning_controller_data ()
{
    echo "$MAJOR.$MINOR.$PATCH" 
    echo $VERSION
    (curl --header "Content-Type: application/json" --request POST --data '{"ci_secret":"'$CI_SECRET_KEY'","old_version":"'$VERSION'","new_version":"'$MAJOR'.'$MINOR'.'$PATCH'"}' "$VERSIONING_CONTROLLER_UPDATE_URL")
    rm source/release_scripts/release/*.tar.gz
}

echo $VERSION
echo $MAJOR"."$MINOR"."$PATCH
build_version
echo "Uploading new version back to the controller..."
update_versioning_controller_data
