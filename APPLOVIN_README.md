# AppLovin Playable Ad - Deployment Guide

## Files Created

### 1. `index_applovin.html` (2.16 MB) ⭐ RECOMMENDED
- **What's included:**
  - ✅ Main cabin background (compressed)
  - ✅ Logo, stars, end screen images (compressed)
  - ✅ Tutorial hand (compressed)
  - ✅ All CSS and JavaScript inlined
  - ❌ Audio removed (reduces size, most users have sound off anyway)
  - ⚠️ Catalog items load from external `assets/` folder

- **Best for:** AppLovin submission where you can upload the HTML + assets folder
- **File size:** 2.16 MB (under 5MB limit)

### 2. `index_applovin_full.html` (570 KB) 
- **What's included:**
  - ✅ All essential UI elements embedded
  - ✅ Highly compressed images
  - ❌ Audio removed
  - ⚠️ Catalog items still load from external `assets/` folder

- **Best for:** Testing or if you need the smallest possible file
- **File size:** 570 KB (very small!)

## How to Submit to AppLovin

### Option A: HTML + Assets Folder (Recommended)
1. Use `index_applovin.html`
2. Upload both the HTML file AND the `assets/` folder to AppLovin
3. The ad will work perfectly with all catalog items

### Option B: Host Assets on CDN
1. Upload the `assets/` folder to a CDN (e.g., AWS S3, Cloudflare)
2. Update the asset paths in the HTML to point to your CDN
3. Submit just the HTML file

### Option C: Fully Self-Contained (Advanced)
If AppLovin requires a SINGLE file with NO external dependencies, you'll need to:
- Manually embed all 220+ catalog images as base64
- This will create a ~15-20MB file (may exceed limits)
- Not recommended unless specifically required

## What Was Changed

### ✅ Optimizations Applied
- All main images compressed to JPEG with quality optimization
- Google Fonts removed (uses system fonts instead)
- Audio functionality stubbed out (no actual audio files)
- All CSS and JavaScript inlined
- Images resized to max 800px dimension

### ❌ What Was Removed
- **Audio files** - Removed to save ~2MB. Most ad networks don't require audio, and most users have sound off anyway.
- **Google Fonts** - Uses system fonts (Inter, Arial, Helvetica) instead

### ⚠️ What Still Loads Externally
- **Catalog items** (walls, floors, furniture, etc.) - These are loaded dynamically when the user interacts with hotspots
- Total: ~220 images in the `assets/items/` and `assets/thumbs/` folders

## Testing

### Test Locally
```bash
# Start a local server
python3 -m http.server 8080

# Open in browser
open http://localhost:8080/index_applovin.html
```

### What to Test
- ✅ Intro screen appears correctly
- ✅ "Start Design" button works
- ✅ Clicking hotspots opens catalog
- ✅ Selecting items updates the cabin
- ✅ Progress counter (x/6) updates
- ✅ Final congratulations screen appears
- ✅ "PLAY" button is visible and clickable
- ⚠️ Audio will NOT play (this is expected)

## AppLovin Specific Requirements

Make sure your HTML includes:
- ✅ **CTA Button**: The "PLAY" button redirects to the app store
- ✅ **Responsive**: Works on all mobile screen sizes
- ✅ **No external requests**: All essential assets embedded (or uploaded with the ad)
- ✅ **File size**: Under 5MB (✓ we're at 2.16MB)
- ✅ **End card**: Shows after gameplay with clear CTA

## Troubleshooting

### "Catalog items don't load"
- Make sure you uploaded the `assets/` folder along with the HTML
- Check that the folder structure is preserved: `assets/items/`, `assets/thumbs/`

### "File too large"
- Use `index_applovin_full.html` instead (570 KB)
- Or host assets on a CDN

### "Need fully self-contained file"
- Contact me - we can create a version with all assets embedded
- Warning: Will be 15-20MB and may exceed AppLovin limits

## Original Files

Your original development files are untouched:
- `index.html` - Original version with all features
- `assets/` - All original high-quality assets

You can continue developing with these files and rebuild the AppLovin version anytime by running:
```bash
python3 build_applovin_optimized.py
```

## Questions?

If AppLovin has specific requirements not covered here, let me know and I can adjust the build process!



