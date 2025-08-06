#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"


if [ -n "$1" ]; then
    SOURCE_FILE="$1"

fi
DEST_DIR="$SCRIPT_DIR/../temp/observation_input"

rm -rf "$DEST_DIR"/*

    cp "$SOURCE_FILE" "$DEST_DIR/"
    echo "✅ Copied: $SOURCE_FILE to $DEST_DIR"


