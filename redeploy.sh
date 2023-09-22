#!/bin/bash

# Default values
ALERT_TOKEN=""
WEATHER_TOKEN=""
ETRYVOGA_HOST=""

# Check for arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -a|--alert-token)
            ALERT_TOKEN="$2"
            shift 2
            ;;
        -w|--weather-token)
            WEATHER_TOKEN="$2"
            shift 2
            ;;
        -e|--etryvoga-host)
            ETRYVOGA_HOST="$2"
            shift 2
            ;;
        *)
            echo "Unknown argument: $1"
            exit 1
            ;;
    esac
done

echo "BOT_TOKEN: $BOT_TOKEN"
echo "WEATHER_TOKEN: $WEATHER_TOKEN"
echo "ETRYVOGA_HOST: $ETRYVOGA_HOST"

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
docker run --name rutracker_parser --restart unless-stopped -d --env BOT_TOKEN="$BOT_TOKEN" --env CHANNEL_ID="$CHANNEL_ID" --env FEED_URLS="$FEED_URLS" rutracker_parser

echo "Container deployed successfully!"

