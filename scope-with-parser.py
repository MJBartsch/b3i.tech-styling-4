#!/usr/bin/env python3
"""
Use proper CSS parser to scope selectors correctly
"""

import tinycss2
import re

# Read original CSS
with open('styling test page.css', 'r', encoding='utf-8') as f:
    original_css = f.read()

def scope_selector(selector):
    """Add .crypto-betting-widget prefix to a selector"""
    selector = selector.strip()
    if not selector or selector.startswith('@'):
        return selector
    if '.crypto-betting-widget' in selector:
        return selector
    return f'.crypto-betting-widget {selector}'

def process_stylesheet(css_text):
    """Process CSS and scope all selectors"""
    # Parse CSS
    rules = tinycss2.parse_stylesheet(css_text, skip_comments=False, skip_whitespace=False)

    result = []

    for rule in rules:
        if rule.type == 'qualified-rule':
            # This is a CSS rule with selectors
            # Get the selector (prelude)
            selector_tokens = rule.prelude
            selector_text = tinycss2.serialize(selector_tokens).strip()

            # Scope each selector (handle comma-separated)
            selectors = [s.strip() for s in selector_text.split(',')]
            scoped_selectors = [scope_selector(s) for s in selectors if s]
            scoped_selector_text = ',\n'.join(scoped_selectors)

            # Get the content
            content_text = tinycss2.serialize(rule.content)

            # Reconstruct rule
            result.append(f'{scoped_selector_text} {{{content_text}}}')

        elif rule.type == 'at-rule':
            # Handle @media, @keyframes, etc.
            at_rule_name = rule.at_keyword
            prelude_text = tinycss2.serialize(rule.prelude) if rule.prelude else ''

            if rule.content:
                # Process content recursively for @media
                if at_rule_name in ['media', 'supports']:
                    # Process nested rules
                    nested_result = []
                    nested_rules = tinycss2.parse_rule_list(rule.content)

                    for nested_rule in nested_rules:
                        if nested_rule.type == 'qualified-rule':
                            selector_text = tinycss2.serialize(nested_rule.prelude).strip()
                            selectors = [s.strip() for s in selector_text.split(',')]
                            scoped_selectors = [scope_selector(s) for s in selectors if s]
                            scoped_selector_text = ',\n    '.join(scoped_selectors)
                            content_text = tinycss2.serialize(nested_rule.content)
                            nested_result.append(f'    {scoped_selector_text} {{{content_text}}}')
                        else:
                            # Other token in media query
                            nested_result.append('    ' + tinycss2.serialize([nested_rule]))

                    result.append(f'@{at_rule_name} {prelude_text} {{\n' + '\n'.join(nested_result) + '\n}')
                else:
                    # @keyframes or other - don't scope
                    content_text = tinycss2.serialize(rule.content)
                    result.append(f'@{at_rule_name} {prelude_text} {{{content_text}}}')
            else:
                result.append(f'@{at_rule_name} {prelude_text};')
        else:
            # Whitespace, comments, etc.
            result.append(tinycss2.serialize([rule]))

    return '\n\n'.join(result)

# Process
try:
    scoped_css = process_stylesheet(original_css)

    # Write output
    with open('styling-test-page-fixed.css', 'w', encoding='utf-8') as f:
        f.write(scoped_css)

    print("✅ CSS properly scoped using parser!")
    print(f"   Size: {len(scoped_css)} bytes")
    print(f"   Lines: {len(scoped_css.splitlines())}")

    # Verify
    scoped_count = scoped_css.count('.crypto-betting-widget')
    print(f"   Scoped selectors: {scoped_count}")

    # Check media queries
    media_count = scoped_css.count('@media')
    print(f"   Media queries: {media_count}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
