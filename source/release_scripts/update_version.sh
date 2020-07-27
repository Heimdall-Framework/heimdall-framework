VERSION=$((curl -sb -H "Accept: application/json" "$VERSIONING_CONTROLLER_GET_URL") | jq -r '.version')

MAJOR=$(cut -d'.' -f1 <<<$VERSION)
MINOR=$(cut -d'.' -f2 <<<$VERSION)
PATCH=$(cut -d'.' -f3 <<<$VERSION)

function update_versioning_controller_data ()
{
    echo $MAJOR"."$MINOR"."$PATCH 
    echo $VERSION
    (curl --header "Content-Type: application/json" --request POST --data '{"ci_secret":"'$CI_SECRET'","old_version":"'$VERSION'","new_version":"'$MAJOR'.'$MINOR'.'$PATCH'"}' "$VERSIONING_CONTROLLER_UPDATE_URL")
}

echo $VERSION
echo $MAJOR"."$MINOR"."$PATCH
build_version
echo "Uploading new version back to the controller..."
update_versioning_controller_data