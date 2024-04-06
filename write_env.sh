#!/bin/bash
# For some reason I decided to keep loading the environment from a file in production
# But you can omit this and define dotenv as a dev dependency
# Load it and invoke it only if the environment is not prod

DIR=src/.env.spotify
# Write environment variables to .env file
echo "CLIENT_ID=\"$CLIENT_ID\"" >> $DIR
echo "CLIENT_SECRET=\"$CLIENT_SECRET\"" >> $DIR
echo "TITLE=\"$TITLE\"" >> $DIR
echo "FAVICON_URL=\"$FAVICON_URL\"" >> $DIR
echo "PLAYLIST_IDS=\"$PLAYLIST_IDS\"" >> $DIR
echo "LINKEDIN=\"$LINKEDIN\"" >> $DIR
echo "GITHUB=\"$GITHUB\"" >> $DIR
echo "SOUNDCLOUD=\"$SOUNDCLOUD\"" >> $DIR
