#!/bin/bash

# Default values
BOT_TOKEN=""
CHANNEL_ID=""
FEED_URLS=""

# Check for arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -b|--alert-token)
            BOT_TOKEN="$2"
            shift 2
            ;;
        -c|--weather-token)
            CHANNEL_ID="$2"
            shift 2
            ;;
        -f|--etryvoga-host)
            FEED_URLS="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

echo "BOT_TOKEN: $BOT_TOKEN"
echo "CHANNEL_ID: $CHANNEL_ID"
echo "FEED_URLS: $FEED_URLS"

# Updating the Git repo
echo "Updating Git repo..."
#cd /path/to/your/git/repo
git pull

# Moving to the deployment directory
echo "Moving to deployment directory..."
#cd /deploy/tcp_server

# Building Docker image
echo "Building Docker image..."
docker build -t rutracker_parser -f Dockerfile .

# Stopping and removing the old container (if exists)
echo "Stopping and removing old container..."
docker stop rutracker_parser || true
docker rm rutracker_parser || true

# Deploying the new container
echo "Deploying new container..."
docker run --name rutracker_parser --restart unless-stopped -d -v rutracker_parser_data:/ --env BOT_TOKEN="$BOT_TOKEN" --env CHANNEL_ID="$CHANNEL_ID" --env FEED_URLS="$FEED_URLS" rutracker_parser

echo "Container deployed successfully!"

