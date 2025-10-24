#!/usr/bin/env python3
"""
Build FULL AppLovin-compatible single HTML file with ALL assets embedded
Uses aggressive compression to fit within size limits
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

def get_base64(file_path, compress=False, max_size_kb=50):
    """Convert file to base64 string"""
    try:
        if compress and file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Determine max size based on image type
            if 'cabin_base' in file_path:
                max_size = 120  # Main background
            elif 'endscreen' in file_path:
                max_size = 100  # End screen images
            elif 'hand' in file_path:
                max_size = 60   # Tutorial hand
            elif '/view/' in file_path:
                max_size = 40   # Catalog view items (larger)
            elif '/thumbs/' in file_path or '/item/' in file_path:
                max_size = 15   # Thumbnails (very small)
            else:
                max_size = 30   # Other images
            
            compressed = compress_image(file_path, max_size_kb=max_size, quality=70)
            if compressed:
                return compressed
        
        # Fallback to original
        with open(file_path, 'rb') as f:
            data = f.read()
            print(f" → {len(data) / 1024:.1f} KB (original)")
            return base64.b64encode(data).decode('utf-8')
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return None

def get_mime_type(file_path):
    """Get MIME type - always JPEG for compressed images"""
    ext = Path(file_path).suffix.lower()
    if ext in ['.jpg', '.jpeg', '.png']:
        return 'image/jpeg'  # We compress everything to JPEG
    elif ext == '.svg':
        return 'image/svg+xml'
    return 'application/octet-stream'

def embed_assets(html_content, base_dir):
    """Replace asset URLs with base64 data URIs"""
    
    embedded_count = 0
    total_size = 0
    
    # Pattern 1: url('path') or url("path") or url(path)
    def replace_url(match):
        nonlocal embedded_count, total_size
        quote = match.group(1) if match.group(1) else ''
        asset_path = match.group(2)
        # Remove query parameters
        asset_path = asset_path.split('?')[0]
        
        full_path = os.path.join(base_dir, asset_path)
        
        if not os.path.exists(full_path):
            print(f"⚠️  Not found: {asset_path}")
            return match.group(0)
        
        file_size = os.path.getsize(full_path)
        print(f"📦 {asset_path} ({file_size / 1024:.1f} KB)", end='')
        
        # Compress images
        is_image = asset_path.lower().endswith(('.jpg', '.jpeg', '.png'))
        base64_data = get_base64(full_path, compress=is_image)
        
        if base64_data is None:
            return match.group(0)
        
        mime_type = get_mime_type(full_path)
        data_uri = f"data:{mime_type};base64,{base64_data}"
        embedded_count += 1
        total_size += len(base64_data)
        
        return f"url({quote}{data_uri}{quote})"
    
    # Pattern 2: src="path" or src='path'
    def replace_src(match):
        nonlocal embedded_count, total_size
        quote = match.group(1)
        asset_path = match.group(2)
        # Remove query parameters
        asset_path = asset_path.split('?')[0]
        
        full_path = os.path.join(base_dir, asset_path)
        
        if not os.path.exists(full_path):
            print(f"⚠️  Not found: {asset_path}")
            return match.group(0)
        
        file_size = os.path.getsize(full_path)
        print(f"📦 {asset_path} ({file_size / 1024:.1f} KB)", end='')
        
        # Compress images
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

def remove_audio(html_content):
    """Remove or stub out audio functionality"""
    
    # Remove Audio() constructor calls
    html_content = re.sub(
        r"new Audio\(['\"]assets/[^'\"]+['\"]\)",
        "{ play: function(){}, pause: function(){}, volume: 0.5, loop: false }",
        html_content
    )
    
    # Comment out audio preload
    html_content = re.sub(
        r"(\s+)(\{\s*src:\s*['\"]assets/music[^}]+\})",
        r"\1// \2 /* Audio removed for size */",
        html_content
    )
    
    print("✓ Audio functionality stubbed out")
    
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
    output_file = base_dir / 'index_applovin_full.html'
    
    print("=" * 70)
    print("Building FULL AppLovin HTML (ALL assets embedded & compressed)")
    print("=" * 70)
    
    # Read original HTML
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"\n📄 Original HTML: {len(html_content) / 1024:.1f} KB")
    
    # Inline Google Fonts
    html_content = inline_google_fonts(html_content)
    
    # Remove audio
    print("\n🔇 Removing audio...")
    html_content = remove_audio(html_content)
    
    # Embed ALL assets with aggressive compression
    print("\n🗜️  Embedding & compressing ALL assets...\n")
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
        print("   You may need to host catalog items externally.")
    elif final_size > 2 * 1024 * 1024:
        print("\n✓ File is under 5MB - should work for most ad networks!")
    else:
        print("\n✓ File is under 2MB - excellent size!")
    
    print("\n📝 Notes:")
    print("   • Audio removed (most ad networks don't require it)")
    print("   • All images compressed to JPEG with quality optimization")
    print("   • Catalog items embedded and will work offline")
    print("=" * 70)

if __name__ == '__main__':
    main()



