#!/usr/bin/env python3
"""
Correctly scope CSS by understanding CSS structure
Only scope actual selectors, not property values
"""

import re

def process_css(css_content):
    """Process CSS content and scope selectors properly"""

    # Split CSS into tokens to understand structure
    result = []
    in_rule = False
    in_keyframes = False
    in_media = False
    brace_depth = 0
    buffer = []

    lines = css_content.split('\n')

    for line in lines:
        stripped = line.strip()

        # Track @keyframes (don't scope inside)
        if '@keyframes' in line:
            in_keyframes = True
            result.append(line)
            continue

        # Track @media
        if '@media' in line or '@supports' in line:
            in_media = True
            result.append(line)
            continue

        # Count braces to track depth
        brace_depth += line.count('{')
        brace_depth -= line.count('}')

        # Exit keyframes/media when depth returns to 0
        if brace_depth == 0:
            if in_keyframes:
                in_keyframes = False
            if in_media:
                in_media = False

        # Don't scope inside @keyframes
        if in_keyframes and '@keyframes' not in line:
            result.append(line)
            continue

        # Check if this is a selector line (has { and we're not in a rule)
        # A selector line has { but we're not currently inside a rule
        if '{' in line and not in_rule:
            # This is a selector line
            if '.crypto-betting-widget' not in line and not line.strip().startswith('@'):
                # Need to scope this
                scoped_line = scope_selector_line(line)
                result.append(scoped_line)
            else:
                result.append(line)
            in_rule = True
        elif '}' in line:
            # Exiting a rule
            result.append(line)
            if brace_depth == 0 or (in_media and brace_depth == 1):
                in_rule = False
        else:
            # Regular property line
            result.append(line)

    return '\n'.join(result)

def scope_selector_line(line):
    """Scope a single selector line"""
    # Extract indent
    indent_match = re.match(r'^(\s*)', line)
    indent = indent_match.group(1) if indent_match else ''

    # Split by {
    parts = line.split('{', 1)
    if len(parts) != 2:
        return line

    selector_part = parts[0].strip()
    rest = '{' + parts[1]

    # Split multiple selectors by comma
    selectors = [s.strip() for s in selector_part.split(',')]
    scoped_selectors = []

    for sel in selectors:
        if sel and not sel.startswith('@'):
            scoped_selectors.append(f'.crypto-betting-widget {sel}')
        else:
            scoped_selectors.append(sel)

    # Reconstruct
    scoped_selector = ',\n' + indent.join(scoped_selectors)
    return indent + scoped_selector + ' ' + rest

# Read original
with open('styling test page.css', 'r', encoding='utf-8') as f:
    original = f.read()

# Process
scoped = process_css(original)

# Fix double scoping
scoped = scoped.replace('.crypto-betting-widget .crypto-betting-widget', '.crypto-betting-widget')

# Write
with open('styling-test-page-fixed.css', 'w', encoding='utf-8') as f:
    f.write(scoped)

print("✅ CSS properly scoped with correct structure!")
print(f"   Lines: {len(scoped.splitlines())}")
print(f"   Size: {len(scoped)} bytes")

# Verify
scoped_count = scoped.count('.crypto-betting-widget')
print(f"   Scoped selectors: {scoped_count}")

# Check media queries
media_sections = scoped.split('@media')
media_with_scoping = sum(1 for section in media_sections[1:] if '.crypto-betting-widget' in section)
print(f"   Media queries with scoping: {media_with_scoping}/{len(media_sections)-1}")
