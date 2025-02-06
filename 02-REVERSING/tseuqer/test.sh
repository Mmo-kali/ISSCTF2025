#!/bin/bash

# Check if the user provided a file as argument
if [ -z "$1" ]; then
  echo "Usage: $0 <base64_file>"
  exit 1
fi

# Decode the base64 file and copy it to the clipboard
cat "$1" | base64 --decode | xclip -selection clipboard

echo "Decoded contents copied to clipboard!"
