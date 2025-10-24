#!/usr/bin/env python3
"""
Build AppLovin-compatible HTML with AUDIO included
"""
import base64
import os
import re
from pathlib import Path
from PIL import Image
import io

def compress_image(file_path, max_size_kb=50, quality=75):
    """Compress image aggressively and return base64 string"""
    try:
        img = Image.open(file_path)
        
        # Resize very large images
        max_dimension = 800
        if max(img.size) > max_dimension:
            ratio = max_dimension / max(img.size)
            new_size = tuple(int(dim * ratio) for dim in img.size)
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            print(f"  Resized to {new_size}", end='')
        
        # Convert RGBA to RGB if needed
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            if 'A' in img.getbands():
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Try different quality levels to meet size target
        for q in range(quality, 15, -5):
            output = io.BytesIO()
            img.save(output, format='JPEG', quality=q, optimize=True)
            
            size_kb = len(output.getvalue()) / 1024
            
            if size_kb <= max_size_kb or q <= 20:
                print(f" → {size_kb:.1f} KB (q={q})")
                return base64.b64encode(output.getvalue()).decode('utf-8')
        
        return None
    except Exception as e:
        print(f"  Error: {e}")
        return None

def get_base64(file_path, compress=False):
    """Convert file to base64 string"""
    try:
        if compress and file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Determine max size based on image type
            if 'cabin_base' in file_path:
                max_size = 120
            elif 'endscreen' in file_path:
                max_size = 100
            elif 'hand' in file_path:
                max_size = 60
            else:
                max_size = 30
            
            compressed = compress_image(file_path, max_size_kb=max_size, quality=70)
            if compressed:
                return compressed
        
        # Fallback to original (for audio files)
        with open(file_path, 'rb') as f:
            data = f.read()
            size_kb = len(data) / 1024
            print(f" → {size_kb:.1f} KB")
            return base64.b64encode(data).decode('utf-8')
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return None

def get_mime_type(file_path):
    """Get MIME type"""
    ext = Path(file_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/jpeg',  # We compress PNGs to JPEG
        '.svg': 'image/svg+xml',
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg'
    }
    return mime_types.get(ext, 'application/octet-stream')

def embed_assets(html_content, base_dir):
    """Replace asset URLs with base64 data URIs"""
    
    embedded_count = 0
    total_size = 0
    
    def replace_url(match):
        nonlocal embedded_count, total_size
        quote = match.group(1) if match.group(1) else ''
        asset_path = match.group(2)
        asset_path = asset_path.split('?')[0]
        
        full_path = os.path.join(base_dir, asset_path)
        
        if not os.path.exists(full_path):
            print(f"⚠️  Not found: {asset_path}")
            return match.group(0)
        
        file_size = os.path.getsize(full_path)
        print(f"📦 {asset_path} ({file_size / 1024:.1f} KB)", end='')
        
        is_image = asset_path.lower().endswith(('.jpg', '.jpeg', '.png'))
        base64_data = get_base64(full_path, compress=is_image)
        
        if base64_data is None:
            return match.group(0)
        
        mime_type = get_mime_type(full_path)
        data_uri = f"data:{mime_type};base64,{base64_data}"
        embedded_count += 1
        total_size += len(base64_data)
        
        return f"url({quote}{data_uri}{quote})"
    
    def replace_src(match):
        nonlocal embedded_count, total_size
        quote = match.group(1)
        asset_path = match.group(2)
        asset_path = asset_path.split('?')[0]
        
        full_path = os.path.join(base_dir, asset_path)
        
        if not os.path.exists(full_path):
            print(f"⚠️  Not found: {asset_path}")
            return match.group(0)
        
        file_size = os.path.getsize(full_path)
        print(f"📦 {asset_path} ({file_size / 1024:.1f} KB)", end='')
        
        is_image = asset_path.lower().endswith(('.jpg', '.jpeg', '.png'))
        base64_data = get_base64(full_path, compress=is_image)
        
        if base64_data is None:
            return match.group(0)
        
        mime_type = get_mime_type(full_path)
        data_uri = f"data:{mime_type};base64,{base64_data}"
        embedded_count += 1
        total_size += len(base64_data)
        
        return f'src={quote}{data_uri}{quote}'
    
    # Replace url() references
    html_content = re.sub(r"url\((['\"]?)(assets/[^'\")\s]+)\1\)", replace_url, html_content)
    
    # Replace src= references
    html_content = re.sub(r'src=(["\'])(assets/[^"\']+)\1', replace_src, html_content)
    
    print(f"\n✓ Total assets embedded: {embedded_count}")
    print(f"✓ Total embedded size: {total_size / 1024 / 1024:.2f} MB")
    
    return html_content

def inline_google_fonts(html_content):
    """Replace Google Fonts link with a fallback"""
    html_content = re.sub(
        r'<link[^>]*fonts\.googleapis\.com[^>]*>',
        '<!-- Google Fonts removed for AppLovin - using system fonts -->',
        html_content
    )
    return html_content

def main():
    base_dir = Path(__file__).parent
    input_file = base_dir / 'index.html'
    output_file = base_dir / 'index_applovin_with_audio.html'
    
    print("=" * 70)
    print("Building AppLovin HTML WITH AUDIO")
    print("=" * 70)
    
    # Read original HTML
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"\n📄 Original HTML: {len(html_content) / 1024:.1f} KB")
    
    # Inline Google Fonts
    html_content = inline_google_fonts(html_content)
    
    # Embed ALL assets (including audio)
    print("\n🗜️  Embedding & compressing assets (including audio)...\n")
    html_content = embed_assets(html_content, base_dir)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    final_size = os.path.getsize(output_file)
    print("\n" + "=" * 70)
    print(f"✅ Created: {output_file}")
    print(f"✅ Final size: {final_size / 1024 / 1024:.2f} MB ({final_size / 1024:.0f} KB)")
    
    if final_size > 5 * 1024 * 1024:
        print("\n⚠️  WARNING: File exceeds 5MB AppLovin limit!")
    elif final_size > 2 * 1024 * 1024:
        print("\n✓ File is under 5MB - should work for AppLovin!")
    else:
        print("\n✓ File is under 2MB - excellent!")
    
    print("\n📝 Notes:")
    print("   • Audio IS included (ambient music + SFX)")
    print("   • All images compressed")
    print("   • Catalog items still load from assets/ folder")
    print("=" * 70)

if __name__ == '__main__':
    main()



