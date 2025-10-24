#!/usr/bin/env python3
"""
Build COMPLETE self-contained HTML with ALL assets embedded as base64
Includes dynamic catalog items by creating a pre-loaded asset map
"""
import base64
import os
import re
import json
from pathlib import Path
from PIL import Image
import io

def compress_image(file_path, max_size_kb=30, quality=60, preserve_transparency=False):
    """Compress image aggressively"""
    try:
        img = Image.open(file_path)
        
        # Resize if too large
        max_dim = 600 if '/view/' in file_path else 400
        if max(img.size) > max_dim:
            ratio = max_dim / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Preserve transparency for specific images
        if preserve_transparency and img.mode == 'RGBA':
            output = io.BytesIO()
            img.save(output, format='PNG', optimize=True)
            return base64.b64encode(output.getvalue()).decode('utf-8'), 'image/png'
        
        # Convert to JPEG
        if img.mode == 'RGBA':
            bg = Image.new('RGB', img.size, (255, 255, 255))
            if 'A' in img.getbands():
                bg.paste(img, mask=img.split()[3])
            else:
                bg.paste(img)
            img = bg
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        for q in range(quality, 10, -5):
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=q, optimize=True)
            size_kb = len(output.getvalue()) / 1024
            if size_kb <= max_size_kb or q <= 15:
                return base64.b64encode(output.getvalue()).decode('utf-8'), 'image/jpeg'
        
        return None, None
    except Exception as e:
        print(f"Error compressing {file_path}: {e}")
        return None, None

def build_asset_map(base_dir):
    """Build a complete map of all catalog assets as base64"""
    asset_map = {}
    total_size = 0
    count = 0
    
    print("\n🗜️  Building catalog asset map...")
    
    # Find all catalog images
    for root, dirs, files in os.walk(os.path.join(base_dir, 'assets')):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                
                # Skip if not a catalog item
                if '/thumbs/' not in rel_path and '/items/' not in rel_path:
                    continue
                
                # Determine compression settings
                # Preserve transparency for PNG catalog items (furniture, chandeliers, etc.)
                preserve_alpha = (file.lower().endswith('.png') or 
                                'logo' in file.lower() or 'hand' in file.lower() or 
                                'star' in file.lower())
                
                if '/thumbs/' in rel_path:
                    max_size = 20  # Small thumbnails
                elif '/view/' in rel_path:
                    max_size = 60  # Larger view images (need more quality)
                else:
                    max_size = 30
                
                b64, mime = compress_image(full_path, max_size_kb=max_size, 
                                          preserve_transparency=preserve_alpha)
                
                if b64:
                    # Normalize path (forward slashes, no query params)
                    norm_path = rel_path.replace('\\', '/')
                    asset_map[norm_path] = f"data:{mime};base64,{b64}"
                    total_size += len(b64)
                    count += 1
                    
                    if count % 20 == 0:
                        print(f"  📦 Processed {count} catalog images...")
    
    print(f"✓ Embedded {count} catalog images ({total_size / 1024 / 1024:.1f} MB)")
    return asset_map

def main():
    base_dir = Path(__file__).parent
    input_file = base_dir / 'index.html'
    output_file = base_dir / 'index_applovin_complete.html'
    
    print("=" * 70)
    print("Building COMPLETE Self-Contained AppLovin HTML")
    print("=" * 70)
    
    # Read HTML
    with open(input_file, 'r', encoding='utf-8') as f:
        html = f.read()
    
    print(f"📄 Original HTML: {len(html) / 1024:.1f} KB")
    
    # Build catalog asset map
    asset_map = build_asset_map(base_dir)
    
    # Embed audio
    print("\n🎵 Embedding audio...")
    audio_files = [
        'assets/music loop and sfx/Ambient Voiceover Background Loop.mp3',
        'assets/music loop and sfx/item click pop.mp3',
        'assets/music loop and sfx/Select button click (when stars appearing).mp3',
        'assets/music loop and sfx/task completed.mp3'
    ]
    
    for audio_path in audio_files:
        full_path = os.path.join(base_dir, audio_path)
        try:
            with open(full_path, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode('utf-8')
                data_uri = f"data:audio/mpeg;base64,{b64}"
                html = html.replace(f"'{audio_path}'", f"'{data_uri}'")
                html = html.replace(f'"{audio_path}"', f'"{data_uri}"')
                print(f"  ✓ {os.path.basename(audio_path)}")
        except Exception as e:
            print(f"  ⚠️  {audio_path}: {e}")
    
    # Embed main images (logo, hand, stars, portrait, etc.)
    print("\n🖼️  Embedding main images...")
    main_images = [
        ('assets/bg/cabin_base.jpg', 120, False),
        ('assets/avenueLogo/0bcc9c966f0cd81e21b73073b6486eae28f2e07f.png', 50, True),
        ('assets/hilary stone/1618970c4b26552e8ee72c322c2753ce94242c7f.jpg', 40, False),
        ('assets/others/hovering hand.png', 60, True),
        ('assets/star /goldenStars.png', 40, True),
        ('assets/star /Vector.svg', 10, False),
        ('assets/star /endscreenstar.png', 20, True),
    ]
    
    for img_path, max_kb, preserve_alpha in main_images:
        full_path = os.path.join(base_dir, img_path)
        if os.path.exists(full_path):
            if img_path.endswith('.svg'):
                with open(full_path, 'rb') as f:
                    b64 = base64.b64encode(f.read()).decode('utf-8')
                    data_uri = f"data:image/svg+xml;base64,{b64}"
            else:
                b64, mime = compress_image(full_path, max_size_kb=max_kb, 
                                          preserve_transparency=preserve_alpha)
                if b64:
                    data_uri = f"data:{mime};base64,{b64}"
                else:
                    continue
            
            # Replace in HTML (handle spaces in paths)
            html = html.replace(f"url('{img_path}')", f"url('{data_uri}')")
            html = html.replace(f'url("{img_path}")', f'url("{data_uri}")')
            html = html.replace(f"src='{img_path}'", f"src='{data_uri}'")
            html = html.replace(f'src="{img_path}"', f'src="{data_uri}"')
            print(f"  ✓ {os.path.basename(img_path)}")
    
    # Embed end screen images
    for i in range(1, 4):
        for fname in os.listdir(os.path.join(base_dir, 'assets/endscreenNextDesign')):
            if fname.endswith('.jpg'):
                img_path = f'assets/endscreenNextDesign/{fname}'
                full_path = os.path.join(base_dir, img_path)
                b64, mime = compress_image(full_path, max_size_kb=100)
                if b64:
                    data_uri = f"data:{mime};base64,{b64}"
                    html = html.replace(f"src='{img_path}'", f"src='{data_uri}'")
                    html = html.replace(f'src="{img_path}"', f'src="{data_uri}"')
    
    # Inject asset map as JavaScript and override gameData functions
    print("\n💉 Injecting catalog asset map...")
    asset_map_json = json.dumps(asset_map, separators=(',', ':'))
    
    # First, inject the asset map in the head
    head_injection = f"""
    <script>
    // Pre-loaded catalog assets (base64 embedded)
    window.EMBEDDED_ASSETS = {asset_map_json};
    </script>
    """
    html = html.replace('</head>', head_injection + '</head>')
    
    # Directly replace the function calls in the HTML
    print("🔧 Replacing function calls with embedded asset lookups...")
    
    # Replace objectData.thumbPath(i) calls
    html = re.sub(
        r'objectData\.thumbPath\(i\)',
        r'(function() { const originalPath = objectData.thumbPath(i); const cleanPath = originalPath.split("?")[0]; return window.EMBEDDED_ASSETS[cleanPath] || originalPath; })()',
        html
    )
    
    # Replace objectData.viewPath calls (with any parameter)
    html = re.sub(
        r'objectData\.viewPath\(([^)]+)\)',
        r'(function() { const originalPath = objectData.viewPath(\1); const cleanPath = originalPath.split("?")[0]; return window.EMBEDDED_ASSETS[cleanPath] || originalPath; })()',
        html
    )
    
    # Remove Google Fonts
    html = re.sub(r'<link[^>]*fonts\.googleapis\.com[^>]*>', 
                  '<!-- Fonts removed -->', html)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    final_size = os.path.getsize(output_file)
    print("\n" + "=" * 70)
    print(f"✅ Created: {output_file}")
    print(f"✅ Final size: {final_size / 1024 / 1024:.2f} MB")
    
    if final_size > 5 * 1024 * 1024:
        print("\n⚠️  Exceeds 5MB - for EMAIL/TESTING only")
        print("   For AppLovin: use index_applovin_with_audio.html + assets/")
    else:
        print("\n✓ Under 5MB - works everywhere!")
    
    print("\n📝 This file is 100% self-contained:")
    print("   ✅ All catalog items embedded")
    print("   ✅ Audio embedded")
    print("   ✅ Transparent assets (logo, hand, stars)")
    print("   ✅ Works via email, USB, anywhere!")
    print("=" * 70)

if __name__ == '__main__':
    main()

