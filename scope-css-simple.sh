#!/bin/bash
# Simple but reliable CSS scoping using sed

input="styling test page.css"
output="styling-test-page-fixed-FULL.css"

# Copy original file
cp "$input" "$output"

# Use sed to add .crypto-betting-widget prefix to selectors
# This matches lines that look like CSS selectors (don't start with spaces/special chars and contain {)
sed -i 's/^\([a-zA-Z\.#\[].*\){$/.crypto-betting-widget \1{/g' "$output"
sed -i 's/^\([a-zA-Z\.#\[].*\),$/.crypto-betting-widget \1,/g' "$output"

# Fix double scoping
sed -i 's/\.crypto-betting-widget \.crypto-betting-widget/.crypto-betting-widget/g' "$output"

# Don't scope @-rules
sed -i 's/\.crypto-betting-widget @/@/g' "$output"

echo "✅ CSS scoped to: $output"
wc -l "$output"
