#!/bin/bash

# Check if at least one argument is provided
if [ $# -lt 1 ]; then
    echo "Usage: $0 [url] [optional: proxy_url]"
    exit 1
fi

# Assign the first argument to URL variable
URL=$1

# Check if the second argument is provided (proxy_url)
if [ $# -ge 2 ]; then
    PROXY_URL=$2
    python wikipedia_scraper_bash.py "$URL" "$PROXY_URL"
else
    python wikipedia_scraper_bash.py "$URL"
fi
