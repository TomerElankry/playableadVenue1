#!/usr/bin/env python3
"""
Build optimized AppLovin-compatible single HTML file
- Removes audio (most ad networks don't require it)
- Compresses images
- Embeds only essential assets
"""
import base64
import os
import re
from pathlib import Path
from PIL import Image
import io

def compress_image(file_path, max_size_kb=100, quality=85):
    """Compress image and return base64 string"""
    try:
        img = Image.open(file_path)
        
        # Convert RGBA to RGB if saving as JPEG
        if img.mode == 'RGBA' and file_path.lower().endswith('.jpg'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
            img = background
        
        # Try different quality levels to meet size target
        for q in range(quality, 20, -5):
            output = io.BytesIO()
            
            if file_path.lower().endswith('.png') and img.mode == 'RGBA':
                img.save(output, format='PNG', optimize=True)
            else:
                # Convert to RGB for JPEG
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                img.save(output, format='JPEG', quality=q, optimize=True)
            
            size_kb = len(output.getvalue()) / 1024
            
            if size_kb <= max_size_kb or q <= 25:
                print(f"  Compressed to {size_kb:.1f} KB (quality={q})")
                return base64.b64encode(output.getvalue()).decode('utf-8')
        
        return None
    except Exception as e:
        print(f"  Error compressing: {e}")
        return None

def get_base64(file_path, compress=False):
    """Convert file to base64 string"""
    try:
        if compress and file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            # Determine max size based on image type
            if 'cabin_base' in file_path or 'endscreen' in file_path:
                max_size = 150  # Larger images get more space
            elif 'hand' in file_path:
                max_size = 80
            else:
                max_size = 50
            
            compressed = compress_image(file_path, max_size_kb=max_size)
            if compressed:
                return compressed
        
        # Fallback to original
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return None

def get_mime_type(file_path, compressed=False):
    """Get MIME type from file extension"""
    ext = Path(file_path).suffix.lower()
    
    # If we compressed a PNG to JPEG, return JPEG mime type
    if compressed and ext == '.png':
        return 'image/jpeg'
    
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.svg': 'image/svg+xml',
    }
    return mime_types.get(ext, 'application/octet-stream')

def embed_assets(html_content, base_dir, include_catalog=True):
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
        
        # Skip catalog items if not including them
        if not include_catalog and ('/items/' in asset_path or '/thumbs/' in asset_path):
            return match.group(0)
        
        full_path = os.path.join(base_dir, asset_path)
        
        if not os.path.exists(full_path):
            print(f"Warning: Asset not found: {full_path}")
            return match.group(0)
        
        file_size = os.path.getsize(full_path)
        print(f"Embedding: {asset_path} ({file_size / 1024:.1f} KB)", end='')
        
        # Compress images
        is_image = asset_path.lower().endswith(('.jpg', '.jpeg', '.png'))
        base64_data = get_base64(full_path, compress=is_image)
        
        if base64_data is None:
            return match.group(0)
        
        mime_type = get_mime_type(full_path, compressed=is_image)
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
        
        # Skip catalog items if not including them
        if not include_catalog and ('/items/' in asset_path or '/thumbs/' in asset_path):
            return match.group(0)
        
        full_path = os.path.join(base_dir, asset_path)
        
        if not os.path.exists(full_path):
            print(f"Warning: Asset not found: {full_path}")
            return match.group(0)
        
        file_size = os.path.getsize(full_path)
        print(f"Embedding: {asset_path} ({file_size / 1024:.1f} KB)", end='')
        
        # Compress images
        is_image = asset_path.lower().endswith(('.jpg', '.jpeg', '.png'))
        base64_data = get_base64(full_path, compress=is_image)
        
        if base64_data is None:
            return match.group(0)
        
        mime_type = get_mime_type(full_path, compressed=is_image)
        data_uri = f"data:{mime_type};base64,{base64_data}"
        embedded_count += 1
        total_size += len(base64_data)
        
        return f'src={quote}{data_uri}{quote}'
    
    # Replace url() references
    html_content = re.sub(r"url\((['\"]?)(assets/[^'\")\s]+)\1\)", replace_url, html_content)
    
    # Replace src= references
    html_content = re.sub(r'src=(["\'])(assets/[^"\']+)\1', replace_src, html_content)
    
    print(f"\nTotal assets embedded: {embedded_count}")
    print(f"Total embedded size: {total_size / 1024 / 1024:.2f} MB")
    
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
    
    print("Audio functionality stubbed out")
    
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
    output_file = base_dir / 'index_applovin.html'
    
    print("=" * 60)
    print("Building Optimized AppLovin-compatible HTML file")
    print("=" * 60)
    
    # Read original HTML
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"\nOriginal HTML size: {len(html_content) / 1024:.1f} KB")
    
    # Inline Google Fonts
    html_content = inline_google_fonts(html_content)
    
    # Remove audio
    print("\nRemoving audio...")
    html_content = remove_audio(html_content)
    
    # Embed essential assets only (no catalog items initially)
    print("\nEmbedding essential assets (compressed)...")
    html_content = embed_assets(html_content, base_dir, include_catalog=False)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    final_size = os.path.getsize(output_file)
    print("\n" + "=" * 60)
    print(f"✓ Created: {output_file}")
    print(f"✓ Final size: {final_size / 1024 / 1024:.2f} MB ({final_size / 1024:.1f} KB)")
    
    if final_size > 5 * 1024 * 1024:
        print("\n⚠️  WARNING: File exceeds 5MB AppLovin limit!")
        print("   The catalog items will load from external URLs.")
    elif final_size > 2 * 1024 * 1024:
        print("\n⚠️  Note: File is over 2MB. Some ad networks prefer smaller files.")
        print("   The catalog items will load from external URLs.")
    else:
        print("\n✓ File size is within typical limits!")
        print("   Catalog items will load from external URLs.")
    
    print("\n📝 Note: Audio has been removed to reduce file size.")
    print("   Most ad networks don't require audio anyway.")
    print("=" * 60)

if __name__ == '__main__':
    main()



