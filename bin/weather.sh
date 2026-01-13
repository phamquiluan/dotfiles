#!/bin/bash
# Weather script for tmux status bar
CACHE="/tmp/tmux_weather_cache"
MAX_AGE=600  # 10 minutes in seconds
LOCATION="${WEATHER_LOCATION:-Melbourne}"  # Configurable via env var

# Check if cache exists and is fresh
if [ -f "$CACHE" ]; then
    AGE=$(($(date +%s) - $(stat -f %m "$CACHE")))
    if [ $AGE -lt $MAX_AGE ]; then
        cat "$CACHE"
        exit 0
    fi
fi

# Fetch new weather data
WEATHER=$(curl -s --max-time 5 "wttr.in/${LOCATION}?format=%t" 2>/dev/null)

if [ -n "$WEATHER" ] && [ "$WEATHER" != "Unknown location" ]; then
    echo "$WEATHER" > "$CACHE"
    echo "$WEATHER"
else
    # Return cached data if available, otherwise N/A
    [ -f "$CACHE" ] && cat "$CACHE" || echo "N/A"
fi
