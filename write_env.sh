#!/bin/bash

DIR=src/.env.spotify
# Write environment variables to .env file
echo "CLIENT_ID=\"$CLIENT_ID\"" >> $DIR
echo "CLIENT_SECRET=\"$CLIENT_SECRET\"" >> $DIR
echo "TITLE=\"$TITLE\"" >> $DIR
echo "FAVICON_URL=\"$FAVICON_URL\"" >> $DIR
echo "PLAYLIST_ID=\"$PLAYLIST_ID\"" >> $DIR
echo "LINKEDIN=\"$LINKEDIN\"" >> $DIR
echo "GITHUB=\"$GITHUB\"" >> $DIR