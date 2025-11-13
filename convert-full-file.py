#!/usr/bin/env python3
"""
Convert the original styling test page to Elementor-compatible version
with CLS fixes while preserving ALL content
"""

import re

# Read the original file
with open('styling test page', 'r', encoding='utf-8') as f:
    content = f.read()

# Remove <head> section and body tags (lines 1-7)
content = re.sub(r'<head>.*?</head>', '', content, flags=re.DOTALL)
content = content.replace('<body>', '').replace('</body>', '')

# Remove the [elementor-template] shortcode as it won't work in HTML widget
content = content.replace('[elementor-template id="1128"]', '<!-- Elementor template removed - not needed in HTML widget -->')

# Wrap everything in crypto-betting-widget div
content = '<div class="crypto-betting-widget">\n' + content.strip() + '\n</div>'

# Add explicit width/height to images (90x90 for logos, 120x120 for card headers)
# Platform logos in quick verdict
content = re.sub(
    r'(<div class="qv-platform-logo">\s*<img[^>]+)loading="lazy"',
    r'\1width="90" height="90" loading="eager"',
    content
)

# Platform logos in platform cards
content = re.sub(
    r'(<div class="platform-logo">\s*<img[^>]+alt="[^"]*"[^>]*)/?>',
    r'\1 width="120" height="120" loading="lazy" />',
    content
)

# Content images
content = re.sub(
    r'(<div class="content-image-wrapper">\s*<img[^>]+)loading="lazy"',
    r'\1width="800" height="450" loading="lazy"',
    content
)

# Add missing closing img tags
content = re.sub(r'<img([^>]+)>(?!</)', r'<img\1 />', content)

# Replace onclick with data-tab
content = re.sub(
    r'onclick="showTab\(\'([^\']+)\',\s*this\)"',
    r'data-tab="\1"',
    content
)

# Add security attributes to external links
content = re.sub(
    r'(<a[^>]+target="_blank"[^>]+rel=")nofollow(")',
    r'\1nofollow noopener noreferrer\2',
    content
)
content = re.sub(
    r'(<a[^>]+target="_blank")([^>]*>)',
    lambda m: m.group(1) + (' rel="nofollow noopener noreferrer"' if 'rel=' not in m.group(2) else '') + m.group(2),
    content
)

# Fix the JavaScript - remove the old function and replace with IIFE
old_js = r'''    <script>
        // FAQ Toggle Functionality
        document\.querySelectorAll\('\.faq-question'\)\.forEach\(button => \{
            button\.addEventListener\('click', \(\) => \{
                const faqItem = button\.closest\('\.faq-item'\);
                faqItem\.classList\.toggle\('active'\);
            \}\);
        \}\);

        // Tab functionality for platform cards
        function showTab\(tabName, button\) \{
            // Get the parent platform card
            const platformCard = button\.closest\('\.platform-card'\);

            // Hide all panes in this card
            const panes = platformCard\.querySelectorAll\('\.tab-pane'\);
            panes\.forEach\(pane => pane\.classList\.remove\('active'\)\);

            // Remove active from all buttons in this card
            const buttons = platformCard\.querySelectorAll\('\.tab-button'\);
            buttons\.forEach\(btn => btn\.classList\.remove\('active'\)\);

            // Show selected pane and mark button active
            document\.getElementById\(tabName\)\.classList\.add\('active'\);
            button\.classList\.add\('active'\);
        \}
    </script>'''

new_js = '''    <!-- JavaScript for tab functionality - Elementor compatible -->
    <script>
    (function() {
        'use strict';

        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', init);
        } else {
            init();
        }

        function init() {
            initFAQs();
            initTabs();
        }

        // FAQ Toggle Functionality
        function initFAQs() {
            document.querySelectorAll('.crypto-betting-widget .faq-question').forEach(button => {
                button.addEventListener('click', () => {
                    const faqItem = button.closest('.faq-item');
                    if (faqItem) {
                        faqItem.classList.toggle('active');
                    }
                });
            });
        }

        // Tab functionality - using event delegation
        function initTabs() {
            const widget = document.querySelector('.crypto-betting-widget');
            if (!widget) return;

            widget.addEventListener('click', function(e) {
                const button = e.target.closest('.tab-button');
                if (!button) return;

                e.preventDefault();
                const tabName = button.getAttribute('data-tab');
                const platformCard = button.closest('.platform-card');

                if (!tabName || !platformCard) return;

                // Hide all panes in this card
                const panes = platformCard.querySelectorAll('.tab-pane');
                panes.forEach(pane => pane.classList.remove('active'));

                // Remove active from all buttons in this card
                const buttons = platformCard.querySelectorAll('.tab-button');
                buttons.forEach(btn => {
                    btn.classList.remove('active');
                    btn.setAttribute('aria-selected', 'false');
                });

                // Show selected pane and mark button active
                const targetPane = platformCard.querySelector('#' + tabName);
                if (targetPane) {
                    targetPane.classList.add('active');
                    button.classList.add('active');
                    button.setAttribute('aria-selected', 'true');
                }
            });
        }
    })();
    </script>'''

content = re.sub(old_js, new_js, content, flags=re.DOTALL)

# Add ARIA attributes to tab buttons
content = re.sub(
    r'(<button class="tab-button)(.*?)"',
    r'\1\2" role="tab"',
    content
)

# Add aria-selected to active tab buttons
content = re.sub(
    r'(<button class="tab-button active"[^>]*)(>)',
    r'\1 aria-selected="true"\2',
    content
)

# Add aria-selected=false to inactive tab buttons
content = re.sub(
    r'(<button class="tab-button"(?! active)[^>]*role="tab")(>)',
    r'\1 aria-selected="false"\2',
    content
)

# Add role="tabpanel" to tab panes
content = re.sub(
    r'(<div class="tab-pane)',
    r'\1 role="tabpanel"',
    content
)

# Add tablist role to tab nav
content = re.sub(
    r'(<div class="tab-nav">)',
    r'<div class="tab-nav" role="tablist">',
    content
)

# Add aria-labels to rating stars
content = re.sub(
    r'(<span class="qv-rating-stars">)',
    r'<span class="qv-rating-stars" aria-label="Rating">',
    content
)

# Write the output
with open('styling-test-page-COMPLETE.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ COMPLETE file created: styling-test-page-COMPLETE.html")
print(f"📊 Total lines: {len(content.splitlines())}")
print(f"📏 Total size: {len(content)} characters")
