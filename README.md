# Cabin Design Playable Ad

A responsive HTML5 playable ad for interior design, featuring a mountain cabin customization experience.

## 🏔️ Project Overview

**Target:** 720×1280 portrait canvas, designed to fill ~98% of the viewport while maintaining aspect ratio, fully responsive.
**Bundle Size:** 2.2MB (Target: ≤3-5MB) ✅
**Asset Optimization:** PNG → JPEG (3-6MB → 20-50KB per asset) ✅
**Compatibility:** Desktop & Mobile, iOS Safari 15+, Android Chrome 9+ ✅

## 🎯 Game Features

### In-Scene Tutorial
- **Immediate Cabin View:** Game starts directly with the cabin scene visible.
- **Text Bubble:** "Help us decorate the dream cabin!" message in the top-right corner.
- **Animated Hand:** Guides user by pointing to the "windows" hotspot.
- **"Start" Button:** Enables interaction and dismisses the tutorial.
- **Free-Order Gameplay:** Tutorial hints, but does not force interaction order.
- **Responsive:** Tutorial elements are positioned dynamically and scale with the game.

### Interactive Zones (5 total)
- **Windows** - Located at `{"x": -216, "y": -243}`
- **Chandelier** - Located at `{"x": -4, "y": -129}`
- **Bed Frame** - Located at `{"x": 162, "y": 280}`
- **Bed Sheets** - Located at `{"x": -12, "y": 239}`
- **Floor** - Located at `{"x": -270, "y": 311}`

### Catalog System  
- **9 variants per zone** (45 total options)
- **Free-order gameplay** - click any zone at any time
- **Progressive approval** - dots turn green when confirmed
- **Completion reward** - 5-star animation + CTA

### Responsive Design
- **Viewport scaling** - dynamically adapts to screen size using JavaScript `transform: scale()` to fill approximately 98% of the window while preserving the 720x1280 aspect ratio.
- **Touch-friendly** - 80px hotspot areas 
- **Mobile optimized** - appropriate button sizes

## 🚀 Quick Start

### Option 1: Simple File Server
```bash
# Navigate to project directory
cd /Users/tomerelankry/Desktop/playableadVenue1

# Python 3 (recommended)
python3 -m http.server 8000

# Open browser
open http://localhost:8000
```

### Option 2: Node.js Server (if available)
```bash
npx http-server . -p 8000 -o
```

### Option 3: Direct File Access
Double-click `index.html` (may have CORS limitations with local assets)

## 📊 Performance Metrics

### Asset Optimization Results
- **Cabin Background:** 6.8MB → 899KB (87% reduction)
- **Catalog Items:** 3-6MB → 20-50KB each (99% reduction)
- **Total Bundle:** 2.2MB (within FRD limits)

### Loading Performance
- **Target:** First interaction ≤2s on 4G ✅
- **FPS Target:** 45-60 FPS ✅
- **Mobile Performance:** Optimized for touch interaction ✅

## 🔧 Development Notes

### File Structure
```
playableadVenue1/
├── index.html                 # Main playable ad
├── assets/
│   ├── bg/cabin_base.jpg     # Cabin background (899KB)
│   ├── items/                # Full-size catalog images
│   │   ├── windows/view/1-9.png
│   │   ├── chandelier/view/1-9.png
│   │   ├── bed_frame/view/1-9.png
│   │   ├── bed_sheets/view/1-9.png
│   │   └── floor/view/1-9.png
│   └── thumbs/               # Catalog thumbnails (120px)
│       ├── windows/1-9.png
│       ├── chandelier/1-9.png
│       ├── bed_frame/1-9.png
│       ├── bed_sheets/1-9.png
│       └── floor/1-9.png
└── optimize_assets.sh        # Asset processing script
```

### Analytics Events (Built-in)
- `playable_start` - Game initialized
- `tutorial_shown` - In-scene tutorial displayed
- `tutorial_dismissed` - In-scene tutorial dismissed via "Start" button
- `intro_design_click` - Start button clicked (from tutorial or immediate start)
- `spot_opened` - Catalog opened for zone
- `variant_preview` - Item selected in catalog  
- `spot_confirmed` - Zone approved
- `all_spots_confirmed` - All zones complete
- `rating_shown` - Final screen displayed
- `cta_click` - Download button clicked

## 🎨 Customization

### Zone Positioning
Hotspot coordinates are defined in `CONFIG.application.zonesConfig` (logical 720x1280 coordinates):
```javascript
"windows": {"dot": {"x": -216, "y": -243}},
"chandelier": {"dot": {"x": -4, "y": -129}},
"bed_frame": {"dot": {"x": 162, "y": 280}},
"bed_sheets": {"dot": {"x": -12, "y": 239}},
"floor": {"dot": {"x": -270, "y": 311}}
```

### Store URLs
Update in `CONFIG.application` for your app:
```javascript
"googlePlayUrl": "https://www.venuegame.co",
"appStoreUrl": "https://www.venuegame.co"
```
Both now point to the unified download link.

## 🚦 Testing Checklist

- [x] Load game on desktop Chrome/Firefox/Safari
- [x] Load game on mobile iOS Safari
- [x] Load game on mobile Android Chrome  
- [x] Test new in-scene tutorial functionality (text, hand, "Start" button)
- [x] Test all 5 hotspots open catalogs
- [x] Test variant selection and approval
- [x] Test completion flow (all zones → stars → CTA)
- [x] Test responsive scaling on different screen sizes
- [x] Verify bundle size ≤5MB for ad network requirements

## 🎯 Ad Network Deployment

### File Requirements
- **Single HTML file:** `index.html` 
- **Asset folder:** `assets/` (included in bundle)
- **Total size:** 2.2MB ✅
- **Format:** HTML5 compatible with AppLovin, Meta, Unity, Google Ads ✅

### Upload Instructions
1. Zip the entire `playableadVenue1` folder
2. Upload to ad network as HTML5 playable
3. Set canvas size as 720×1280 portrait
4. Configure store URLs in ad network dashboard

---

**Status:** ✅ Ready for deployment
**Bundle Size:** 2.2MB / 5MB (44% of limit)
**Compatibility:** ✅ Desktop + Mobile responsive