#!/bin/bash

echo "Building plugin..."


PLUGIN_NAME="getcontacts-flareplot"

rm -rf *.hp

# Build the flare plot view
npm run build

# If we are on a tag use the tag, if not use branch
BRANCH_NAME=$(git rev-parse --abbrev-ref HEAD)

TAG=$(git tag --points-at HEAD)

if [ -z "$TAG" ]; then
    VERSION=$(echo $BRANCH_NAME | sed 's/[^a-zA-Z0-9]/_/g')
    # Find the latest tag available, even if we ar enot inside one
    LATEST_TAG=$(git describe --tags $(git rev-list --tags --max-count=1))

    # If no latest tag, use 0.0.0
    if [ -z "$LATEST_TAG" ]; then
        LATEST_TAG="1.0"
    fi

    VERSION="${LATEST_TAG}-${VERSION}"
else
    VERSION=$(echo $TAG | sed 's/[^a-zA-Z0-9.]/_/g')
fi

# Update the plugin.meta
META_FILE="${PLUGIN_NAME}/plugin.meta"
echo "Updating plugin.meta with version $VERSION..."
jq '.version = "'$VERSION'"' $META_FILE > tmp.$$.json && mv tmp.$$.json $META_FILE

ZIP_FILE="${PLUGIN_NAME}_${VERSION}.hp"

zip -r $ZIP_FILE $PLUGIN_NAME

# Restore the plugin.meta back to version 0.0.0
jq '.version = "0.0.0"' $META_FILE > tmp.$$.json && mv tmp.$$.json $META_FILE