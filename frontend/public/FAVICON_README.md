# AquaVision AI - Favicon Options

## Available Favicons

### 1. **favicon.svg** (Currently Active) 🌊
- **Design:** Water droplet with waves
- **Style:** Clean, professional
- **Colors:** Blue gradient (#0ea5e9 to #0284c7)
- **Best for:** Professional/academic presentations

### 2. **favicon-alt.svg** (Alternative) 💧
- **Design:** Letter 'A' with water waves
- **Style:** Modern, branded
- **Colors:** Cyan gradient (#06b6d4 to #0e7490)
- **Best for:** Branding, portfolio

## How to Change Favicon

### Option 1: Use Alternative Design

Edit `frontend/index.html`:

```html
<!-- Change this line -->
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />

<!-- To this -->
<link rel="icon" type="image/svg+xml" href="/favicon-alt.svg" />
```

### Option 2: Create Your Own

1. Edit `frontend/public/favicon.svg` with any SVG editor
2. Or use online tools:
   - https://favicon.io/
   - https://realfavicongenerator.net/
   - https://www.favicon-generator.org/

### Option 3: Use Custom Image

1. Create a 512x512 PNG image
2. Save as `frontend/public/favicon.png`
3. Update `index.html`:

```html
<link rel="icon" type="image/png" href="/favicon.png" />
```

## Design Guidelines

### Colors (Water Theme)
- Primary: `#0ea5e9` (Sky Blue)
- Secondary: `#0284c7` (Ocean Blue)
- Accent: `#06b6d4` (Cyan)
- Dark: `#0e7490` (Deep Teal)

### Symbols
- 💧 Water droplet (purity, conservation)
- 🌊 Waves (flow, availability)
- 📊 Graph (data, prediction)
- 🤖 AI (intelligence, automation)

## Testing Your Favicon

1. **Local Development:**
   ```bash
   npm run dev
   ```
   Open http://localhost:5173 and check browser tab

2. **Clear Cache:**
   - Chrome: Ctrl+Shift+R (Cmd+Shift+R on Mac)
   - Firefox: Ctrl+F5
   - Safari: Cmd+Option+R

3. **Check Multiple Sizes:**
   - Browser tab (16x16, 32x32)
   - Bookmarks bar
   - Mobile home screen
   - Search results

## Current Favicon Features

✅ SVG format (scalable, crisp at any size)  
✅ Water-themed design  
✅ Professional gradient  
✅ Transparent background  
✅ Optimized file size  
✅ Cross-browser compatible  

## Favicon Specifications

- **Format:** SVG (recommended) or PNG
- **Size:** 100x100 (SVG), 512x512 (PNG)
- **Colors:** 2-3 colors max for clarity
- **Style:** Simple, recognizable at small sizes
- **File size:** < 5KB

## Need Help?

- SVG Tutorial: https://developer.mozilla.org/en-US/docs/Web/SVG
- Favicon Guide: https://web.dev/articles/icons-and-browser-colors
- Design Tools: Figma, Inkscape, Adobe Illustrator

---

**Current Active:** `favicon.svg` (Water droplet design)  
**Alternative:** `favicon-alt.svg` (Letter A with waves)
