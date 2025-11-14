# WordPress/Elementor Conflict Fixes

Since the tabs work perfectly **outside WordPress** but not **inside Elementor**, we have a WordPress/Elementor-specific conflict.

---

## 🔍 Common WordPress/Elementor Issues

### 1. **CSS Specificity War**

Elementor and WordPress themes have their own CSS that might override yours.

**Solution:** Add `!important` to critical tab display rules.

Add this CSS to **Elementor → Settings → Custom CSS**:

```css
/* Force tab display rules */
.crypto-betting-widget .tab-pane {
    display: none !important;
}

.crypto-betting-widget .tab-pane.active {
    display: block !important;
}

/* Ensure buttons are clickable */
.crypto-betting-widget .tab-button {
    cursor: pointer !important;
    pointer-events: auto !important;
    position: relative !important;
    z-index: 10 !important;
}

/* Ensure tab content container is visible */
.crypto-betting-widget .tab-content {
    display: block !important;
    min-height: 200px !important;
}

/* Prevent Elementor from hiding content */
.crypto-betting-widget .tabs-container {
    display: block !important;
    opacity: 1 !important;
    visibility: visible !important;
}
```

---

### 2. **jQuery Conflict**

WordPress loads jQuery in "no conflict" mode, which can break JavaScript.

**Solution:** Wrap JavaScript in jQuery ready function.

Replace the `<script>` section in your HTML with this:

```html
<script>
jQuery(document).ready(function($) {
    'use strict';

    console.log('Crypto widget tabs initializing...');

    // Initialize FAQs
    $('.crypto-betting-widget .faq-question').on('click', function() {
        $(this).closest('.faq-item').toggleClass('active');
    });

    // Initialize Tabs
    $('.crypto-betting-widget').on('click', '.tab-button', function(e) {
        e.preventDefault();

        var $button = $(this);
        var tabName = $button.attr('data-tab');
        var $card = $button.closest('.platform-card');

        console.log('Tab clicked:', tabName);

        // Hide all panes in this card
        $card.find('.tab-pane').removeClass('active');

        // Deactivate all buttons
        $card.find('.tab-button').removeClass('active').attr('aria-selected', 'false');

        // Show selected pane
        $card.find('#' + tabName).addClass('active');
        $button.addClass('active').attr('aria-selected', 'true');

        console.log('Tab activated:', tabName);
    });

    console.log('Crypto widget tabs initialized!');
});
</script>
```

---

### 3. **Elementor HTML Widget Sanitization**

Elementor might strip or modify your HTML.

**Check:**
- Go to Elementor → Settings → Features
- Ensure "Improved CSS Loading" is OFF
- Ensure "Improved Asset Loading" is OFF

**Alternative:** Use a **Code Snippet plugin** instead of HTML widget:
1. Install "Code Snippets" plugin
2. Add new snippet with type "Frontend"
3. Paste HTML there
4. Place shortcode in Elementor

---

### 4. **Theme CSS Override**

Your theme might have CSS that hides or breaks tabs.

**Diagnostic CSS** - Add to Custom CSS:

```css
/* Diagnostic - makes hidden tabs visible with red border */
.crypto-betting-widget .tab-pane {
    border: 3px solid red !important;
    background: yellow !important;
    min-height: 100px !important;
}

.crypto-betting-widget .tab-pane.active {
    border: 3px solid green !important;
    background: lightgreen !important;
}

/* If you see ALL tabs with red borders, CSS is broken */
/* If you see ONE tab with green border, CSS is working */
/* If you see NO tabs at all, they're being hidden by something else */
```

Add this temporarily, then reload. You should see:
- ✅ **ONE tab with GREEN border** = CSS working
- ❌ **ALL tabs with RED borders** = .active class not working
- ❌ **NO tabs visible** = Content is being hidden

---

### 5. **JavaScript Not Loading**

Elementor might not execute your JavaScript.

**Test:** Add this at the TOP of your `<script>` tag:

```javascript
alert('JavaScript is loading!');
console.log('Tab script loaded');
```

- **If you see alert:** JavaScript loads, but tabs logic has issue
- **If NO alert:** JavaScript isn't loading at all

**Fix for no loading:**
Move JavaScript to **Elementor → Custom CSS → Custom JavaScript** section:

```javascript
( function( $ ) {
    $(window).on('elementor/frontend/init', function() {
        console.log('Elementor frontend initialized');

        // Your tab code here
        $('.crypto-betting-widget').on('click', '.tab-button', function(e) {
            e.preventDefault();
            var tabName = $(this).attr('data-tab');
            var $card = $(this).closest('.platform-card');
            $card.find('.tab-pane').removeClass('active');
            $card.find('.tab-button').removeClass('active');
            $card.find('#' + tabName).addClass('active');
            $(this).addClass('active');
        });
    });
} )( jQuery );
```

---

### 6. **Content Security Policy**

WordPress might block inline scripts.

**Fix:** Use external JavaScript file:

1. Upload JavaScript as `/wp-content/uploads/crypto-tabs.js`
2. Remove `<script>` from HTML
3. Add this to **functions.php** or use plugin:

```php
function enqueue_crypto_tabs_script() {
    wp_enqueue_script(
        'crypto-tabs',
        get_site_url() . '/wp-content/uploads/crypto-tabs.js',
        array('jquery'),
        '1.0',
        true
    );
}
add_action('wp_enqueue_scripts', 'enqueue_crypto_tabs_script');
```

---

### 7. **Elementor Flexbox Container**

If using Elementor Flexbox containers, they can hide overflow.

**Fix:** Wrap HTML in a div:

```html
<div style="overflow: visible !important; position: relative !important;">
    <div class="crypto-betting-widget">
        <!-- your content -->
    </div>
</div>
```

---

### 8. **Lazy Loading Breaking JavaScript**

Elementor lazy loads widgets, which might break timing.

**Fix:** Add delay:

```javascript
setTimeout(function() {
    // Initialize tabs here
    initTabs();
}, 500);
```

---

## 🧪 **Step-by-Step Diagnostic**

Follow these steps IN ORDER:

### Step 1: Check if HTML is rendering
1. Right-click on page → Inspect Element
2. Search for `crypto-betting-widget`
3. ✅ Found? Go to Step 2
4. ❌ Not found? HTML widget is broken - use different method

### Step 2: Check if CSS is loading
1. Inspect Element on a tab pane
2. Check computed styles
3. Look for `display: none` or `display: block`
4. ✅ Correct? Go to Step 3
5. ❌ Wrong? CSS isn't loading properly

### Step 3: Check if JavaScript is loading
1. Open browser console (F12)
2. Type: `jQuery('.crypto-betting-widget').length`
3. Should return `1`
4. ✅ Returns 1? Go to Step 4
5. ❌ Returns 0? Widget not found

### Step 4: Check if clicks work
1. Open console
2. Type:
```javascript
jQuery('.crypto-betting-widget').on('click', '.tab-button', function() {
    console.log('Click detected!', jQuery(this).attr('data-tab'));
});
```
3. Click a tab button
4. ✅ See "Click detected!"? JavaScript works
5. ❌ Nothing? Clicks are blocked

### Step 5: Manually test tab switching
In console, run:
```javascript
jQuery('.tab-pane').removeClass('active');
jQuery('#888-fees').addClass('active');
```

- ✅ **Fees tab appears?** CSS works, JavaScript broken
- ❌ **Nothing happens?** CSS is being overridden

---

## 🔧 **Quick Fixes to Try**

### Quick Fix #1: Nuclear !important
Add to Custom CSS:

```css
.crypto-betting-widget .tab-pane {
    display: none !important;
}
.crypto-betting-widget .tab-pane.active {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    height: auto !important;
    overflow: visible !important;
}
```

### Quick Fix #2: Inline styles
In HTML, add to first tab-pane:
```html
<div class="tab-pane active" id="888-overview" style="display: block !important;">
```

Does it show now?
- ✅ Yes? CSS specificity issue
- ❌ No? Something else hiding it

### Quick Fix #3: jQuery fallback
Replace your script with this simple version:

```html
<script>
jQuery(document).ready(function($) {
    $('.tab-button').click(function() {
        var tab = $(this).data('tab');
        $(this).closest('.platform-card').find('.tab-pane').hide();
        $(this).closest('.platform-card').find('#' + tab).show();
        $(this).siblings().removeClass('active');
        $(this).addClass('active');
    });
});
</script>
```

---

## 📦 **Recommended Solution**

The most reliable approach for WordPress/Elementor:

### Method 1: Shortcode (Most Reliable)

1. Create `crypto-tabs-shortcode.php` in theme:

```php
<?php
function crypto_betting_widget_shortcode($atts) {
    ob_start();
    include get_template_directory() . '/crypto-widget.html';
    return ob_get_clean();
}
add_shortcode('crypto_widget', 'crypto_betting_widget_shortcode');

function crypto_tabs_scripts() {
    wp_enqueue_style('crypto-tabs-css', get_template_directory_uri() . '/styling-test-page-fixed.css');
    wp_enqueue_script('crypto-tabs-js', get_template_directory_uri() . '/crypto-tabs.js', array('jquery'), '1.0', true);
}
add_action('wp_enqueue_scripts', 'crypto_tabs_scripts');
?>
```

2. In Elementor, add Shortcode widget with: `[crypto_widget]`

### Method 2: Custom Elementor Widget

Use a plugin like "Custom Elementor Widgets" to create a proper widget.

---

## 🎯 **What to Check First**

1. **Browser Console** - Any JavaScript errors?
2. **Inspect Element** - Is `.tab-pane.active` present?
3. **Computed Styles** - What's the `display` value?
4. **Click Events** - Do buttons respond to clicks?

Share what you find and I can give you a specific fix!

---

## 📞 **Need Help?**

If tabs still don't work, provide:
1. Screenshot of browser console (F12)
2. Screenshot of inspect element on `.tab-pane.active`
3. Your WordPress theme name
4. Elementor version
5. Any other plugins that might affect CSS/JS

I'll create a custom fix for your specific setup!
