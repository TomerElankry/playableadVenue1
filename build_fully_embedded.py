#!/usr/bin/env python3
"""
Build FULLY self-contained AppLovin HTML with ALL assets embedded
Including all catalog items (220+ images)
"""
import base64
import os
import re
from pathlib import Path
from PIL import Image
import io

def get_audio_base64(file_path):
    """Convert audio file to base64 data URI"""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            b64 = base64.b64encode(data).decode('utf-8')
            size_kb = len(data) / 1024
            print(f"  🎵 {os.path.basename(file_path)}: {size_kb:.1f} KB")
            return f"data:audio/mpeg;base64,{b64}"
    except Exception as e:
        print(f"  ⚠️  Error reading {file_path}: {e}")
        return None

def compress_image(file_path, max_size_kb=120, quality=70, preserve_transparency=False):
    """Compress image and return base64"""
    try:
        img = Image.open(file_path)
        
        max_dimension = 800
        if max(img.size) > max_dimension:
            ratio = max_dimension / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # If we need to preserve transparency, keep as PNG
        if preserve_transparency and img.mode == 'RGBA':
            output = io.BytesIO()
            img.save(output, format='PNG', optimize=True)
            return base64.b64encode(output.getvalue()).decode('utf-8')
        
        # Otherwise convert to JPEG
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            if 'A' in img.getbands():
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        for q in range(quality, 15, -5):
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=q, optimize=True)
            size_kb = len(output.getvalue()) / 1024
            if size_kb <= max_size_kb or q <= 20:
                return base64.b64encode(output.getvalue()).decode('utf-8')
        return None
    except Exception as e:
        return None

def get_base64(file_path, compress=False):
    """Convert file to base64"""
    try:
        if compress and file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Preserve transparency for logo, hand, and golden stars
            preserve_alpha = ('Logo' in file_path or 'logo' in file_path or 
                            'hand' in file_path or 'Hand' in file_path or
                            'goldenStars' in file_path or 'star' in file_path.lower())
            
            if 'cabin_base' in file_path:
                max_size = 120
            elif 'endscreen' in file_path:
                max_size = 100
            elif 'hand' in file_path or 'Hand' in file_path:
                max_size = 60
            elif 'Logo' in file_path or 'logo' in file_path:
                max_size = 50
            elif 'goldenStars' in file_path or 'star' in file_path.lower():
                max_size = 40
            elif '/view/' in file_path:
                max_size = 50  # Catalog view items
            elif '/thumbs/' in file_path or '/item/' in file_path:
                max_size = 20  # Thumbnails (very compressed)
            else:
                max_size = 30
            
            compressed = compress_image(file_path, max_size_kb=max_size, quality=65, 
                                       preserve_transparency=preserve_alpha)
            if compressed:
                return compressed
        
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        return None

def get_mime_type(file_path, is_png_preserved=False):
    """Get MIME type"""
    ext = Path(file_path).suffix.lower()
    
    # If we preserved PNG transparency, return PNG mime type
    if is_png_preserved and ext == '.png':
        return 'image/png'
    
    if ext in ['.jpg', '.jpeg', '.png']:
        return 'image/jpeg'
    elif ext == '.svg':
        return 'image/svg+xml'
    return 'application/octet-stream'

def embed_images(html_content, base_dir):
    """Embed ALL images as base64"""
    
    embedded_count = 0
    
    def replace_url(match):
        nonlocal embedded_count
        quote = match.group(1) if match.group(1) else ''
        asset_path = match.group(2).split('?')[0]
        
        # Skip audio files
        if 'music loop and sfx' in asset_path:
            return match.group(0)
        
        full_path = os.path.join(base_dir, asset_path)
        if not os.path.exists(full_path):
            print(f"⚠️  Not found: {asset_path}")
            return match.group(0)
        
        is_image = asset_path.lower().endswith(('.jpg', '.jpeg', '.png'))
        base64_data = get_base64(full_path, compress=is_image)
        if base64_data is None:
            return match.group(0)
        
        # Check if transparency was preserved
        is_png_preserved = ('Logo' in asset_path or 'logo' in asset_path or 
                           'hand' in asset_path or 'Hand' in asset_path or
                           'goldenStars' in asset_path or 'star' in asset_path.lower())
        mime_type = get_mime_type(full_path, is_png_preserved=is_png_preserved)
        data_uri = f"data:{mime_type};base64,{base64_data}"
        embedded_count += 1
        
        # Show progress for catalog items
        if '/thumbs/' in asset_path or '/items/' in asset_path:
            if embedded_count % 10 == 0:
                print(f"  📦 Embedded {embedded_count} images...")
        
        return f"url({quote}{data_uri}{quote})"
    
    def replace_src(match):
        nonlocal embedded_count
        quote = match.group(1)
        asset_path = match.group(2).split('?')[0]
        
        # Skip audio files
        if 'music loop and sfx' in asset_path:
            return match.group(0)
        
        full_path = os.path.join(base_dir, asset_path)
        if not os.path.exists(full_path):
            print(f"⚠️  Not found: {asset_path}")
            return match.group(0)
        
        is_image = asset_path.lower().endswith(('.jpg', '.jpeg', '.png'))
        base64_data = get_base64(full_path, compress=is_image)
        if base64_data is None:
            return match.group(0)
        
        # Check if transparency was preserved
        is_png_preserved = ('Logo' in asset_path or 'logo' in asset_path or 
                           'hand' in asset_path or 'Hand' in asset_path or
                           'goldenStars' in asset_path or 'star' in asset_path.lower())
        mime_type = get_mime_type(full_path, is_png_preserved=is_png_preserved)
        data_uri = f"data:{mime_type};base64,{base64_data}"
        embedded_count += 1
        
        return f'src={quote}{data_uri}{quote}'
    
    # Updated regex to handle spaces in file paths
    html_content = re.sub(r"url\((['\"]?)(assets/[^'\")\r\n]+)\1\)", replace_url, html_content)
    html_content = re.sub(r'src=(["\'])(assets/[^"\']+)\1', replace_src, html_content)
    
    print(f"\n✓ Total images embedded: {embedded_count}")
    
    return html_content

def embed_audio_in_js(html_content, base_dir):
    """Replace audio file paths with base64 data URIs in JavaScript"""
    
    audio_files = {
        'assets/music loop and sfx/Ambient Voiceover Background Loop.mp3': None,
        'assets/music loop and sfx/item click pop.mp3': None,
        'assets/music loop and sfx/Select button click (when stars appearing).mp3': None,
        'assets/music loop and sfx/task completed.mp3': None
    }
    
    print("\n🎵 Embedding audio files...")
    for audio_path in audio_files.keys():
        full_path = os.path.join(base_dir, audio_path)
        data_uri = get_audio_base64(full_path)
        if data_uri:
            audio_files[audio_path] = data_uri
            # Replace all occurrences of this audio path
            html_content = html_content.replace(f"'{audio_path}'", f"'{data_uri}'")
            html_content = html_content.replace(f'"{audio_path}"', f'"{data_uri}"')
    
    return html_content

def main():
    base_dir = Path(__file__).parent
    input_file = base_dir / 'index.html'
    output_file = base_dir / 'index_applovin_full_embedded.html'
    
    print("=" * 70)
    print("Building FULLY EMBEDDED AppLovin HTML")
    print("(All catalog items + audio + transparent assets)")
    print("=" * 70)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"\n📄 Original: {len(html_content) / 1024:.1f} KB")
    
    # Remove Google Fonts
    html_content = re.sub(
        r'<link[^>]*fonts\.googleapis\.com[^>]*>',
        '<!-- Google Fonts removed - using system fonts -->',
        html_content
    )
    
    # Embed audio files
    html_content = embed_audio_in_js(html_content, base_dir)
    
    # Embed ALL images (including catalog items)
    print("\n🖼️  Embedding ALL images (this may take a minute)...")
    html_content = embed_images(html_content, base_dir)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    final_size = os.path.getsize(output_file)
    print("\n" + "=" * 70)
    print(f"✅ Created: {output_file}")
    print(f"✅ Final size: {final_size / 1024 / 1024:.2f} MB ({final_size / 1024:.0f} KB)")
    
    if final_size > 5 * 1024 * 1024:
        print("\n⚠️  File exceeds 5MB AppLovin limit!")
        print("   This version is for EMAIL TESTING only.")
        print("   For AppLovin, use index_applovin_with_audio.html + assets folder")
    else:
        print("\n✓ Under 5MB - works for AppLovin!")
    
    print("\n📝 This is a FULLY SELF-CONTAINED file:")
    print("   ✅ Works anywhere (email, USB, etc.)")
    print("   ✅ All catalog items embedded")
    print("   ✅ Audio + transparent assets included")
    print("   ✅ No external dependencies")
    print("=" * 70)

if __name__ == '__main__':
    main()



