#!/bin/bash
# Complete CSS scoping that handles @media queries correctly

input="styling test page.css"
output="styling-test-page-fixed.css"

# Use awk to scope ALL selectors, including those inside @media queries
awk '
BEGIN { in_media = 0; in_keyframes = 0; }

# Track when entering @media or @keyframes
/@media/ { in_media = 1; print; next }
/@keyframes/ { in_keyframes = 1; print; next }

# Exit media/keyframes on closing brace at start of line
/^}/ {
    if (in_media == 1 || in_keyframes == 1) {
        in_media = 0
        in_keyframes = 0
    }
    print
    next
}

# Skip @font-face and other @ rules
/@font-face/ { print; next }
/^@/ && !/@media/ && !/@keyframes/ { print; next }

# Process selector lines (contain { at end or start multi-line selector)
/{$/ && !/@/ {
    # Skip if already scoped
    if (/.crypto-betting-widget/) {
        print
        next
    }
    # Skip comments
    if (/^[\s]*\/\*/) {
        print
        next
    }
    # Skip empty lines or just whitespace
    if (/^[\s]*$/) {
        print
        next
    }
    # Scope the selector
    # Match patterns like: .classname { or #id { or element {
    if (match($0, /^([\s]*)([a-zA-Z0-9._#:[\]> \t,+-]+)[\s]*{/, arr)) {
        indent = arr[1]
        selector = arr[2]
        # Split multiple selectors by comma
        n = split(selector, parts, /,/)
        scoped = ""
        for (i = 1; i <= n; i++) {
            part = parts[i]
            gsub(/^[\s]+|[\s]+$/, "", part)  # trim
            if (part != "") {
                if (scoped != "") scoped = scoped ",\n" indent
                scoped = scoped ".crypto-betting-widget " part
            }
        }
        print indent scoped " {"
        next
    }
}

# Default: print line as-is
{ print }
' "$input" > "$output"

echo "✅ CSS scoped with media query support"
wc -l "$output"

# Verify scoping in media queries
echo "Checking @media scoping..."
grep -A 3 "@media" "$output" | grep ".crypto-betting-widget" | wc -l
echo "scoped selectors found in @media blocks"
