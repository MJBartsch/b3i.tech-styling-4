#!/usr/bin/env python3
"""
Properly scope ALL CSS selectors including those in @media queries
"""

import re

def scope_css_line(line, in_at_rule=False):
    """Scope a single CSS selector line"""
    # Skip if already scoped
    if '.crypto-betting-widget' in line:
        return line

    # Skip comments, empty lines, closing braces
    stripped = line.strip()
    if not stripped or stripped.startswith('/*') or stripped.startswith('*/') or stripped == '}' or stripped.startswith('@'):
        return line

    # Check if this is a selector line (ends with { or is part of multi-selector)
    if '{' not in line and ',' not in line:
        return line

    # Extract indent
    indent = len(line) - len(line.lstrip())
    indent_str = ' ' * indent

    # Split line into selector part and rest
    if '{' in line:
        parts = line.split('{', 1)
        selector_part = parts[0]
        rest = '{' + parts[1] if len(parts) > 1 else '{'
    else:
        selector_part = line.rstrip(',\n')
        rest = ','

    # Split multiple selectors
    selectors = [s.strip() for s in selector_part.split(',')]
    scoped_selectors = []

    for sel in selectors:
        if sel and not sel.startswith('@'):
            scoped_sel = f'.crypto-betting-widget {sel}'
            scoped_selectors.append(scoped_sel)
        elif sel:
            scoped_selectors.append(sel)

    if scoped_selectors:
        # Reconstruct line
        if rest == ',':
            return indent_str + (',\n' + indent_str).join(scoped_selectors) + rest + '\n'
        else:
            return indent_str + (',\n' + indent_str).join(scoped_selectors) + ' ' + rest + '\n'

    return line

# Read original CSS
with open('styling test page.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

output_lines = []
in_keyframes = False

for i, line in enumerate(lines):
    stripped = line.strip()

    # Track @keyframes blocks (don't scope inside these)
    if stripped.startswith('@keyframes'):
        in_keyframes = True
        output_lines.append(line)
        continue

    # Exit @keyframes
    if in_keyframes and line.startswith('}'):
        in_keyframes = False
        output_lines.append(line)
        continue

    # Don't scope inside @keyframes
    if in_keyframes:
        output_lines.append(line)
        continue

    # Don't scope @-rules themselves
    if stripped.startswith('@'):
        output_lines.append(line)
        continue

    # Scope selector lines
    scoped_line = scope_css_line(line)
    output_lines.append(scoped_line)

# Join and write
output = ''.join(output_lines)

# Fix any double scoping
output = output.replace('.crypto-betting-widget .crypto-betting-widget', '.crypto-betting-widget')

with open('styling-test-page-fixed.css', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"✅ CSS properly scoped!")
print(f"   Lines: {len(output_lines)}")
print(f"   Size: {len(output)} bytes")

# Verify scoping in media queries
media_lines = [l for l in output_lines if '@media' in l or (i > 0 and '@media' in output_lines[max(0,output_lines.index(l)-20):output_lines.index(l)])]
scoped_in_media = len([l for l in output_lines if '.crypto-betting-widget' in l])

print(f"   Total scoped selectors: {scoped_in_media}")

# Check a few @media blocks
import re
media_blocks = re.findall(r'@media[^{]+\{[^@]+?\n\}', output, re.DOTALL)
print(f"   Media blocks found: {len(media_blocks)}")
if media_blocks:
    scoped_media = sum(1 for block in media_blocks if '.crypto-betting-widget' in block)
    print(f"   Media blocks with scoping: {scoped_media}")
