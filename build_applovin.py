#!/usr/bin/env python3
"""
Build AppLovin-compatible single HTML file with embedded assets
"""
import base64
import os
import re
from pathlib import Path

def get_base64(file_path):
    """Convert file to base64 string"""
    try:
        with open(file_path, 'rb') as f:
            return base64.b64encode(f.read()).decode('utf-8')
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return None

def get_mime_type(file_path):
    """Get MIME type from file extension"""
    ext = Path(file_path).suffix.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.svg': 'image/svg+xml',
        '.mp3': 'audio/mpeg',
        '.wav': 'audio/wav',
        '.ogg': 'audio/ogg'
    }
    return mime_types.get(ext, 'application/octet-stream')

def embed_assets(html_content, base_dir):
    """Replace asset URLs with base64 data URIs"""
    
    embedded_count = 0
    
    # Pattern 1: url('path') or url("path") or url(path)
    def replace_url(match):
        nonlocal embedded_count
        quote = match.group(1) if match.group(1) else ''
        asset_path = match.group(2)
        # Remove query parameters
        asset_path = asset_path.split('?')[0]
        
        full_path = os.path.join(base_dir, asset_path)
        
        if not os.path.exists(full_path):
            print(f"Warning: Asset not found: {full_path}")
            return match.group(0)
        
        file_size = os.path.getsize(full_path)
        print(f"Embedding: {asset_path} ({file_size / 1024:.1f} KB)")
        
        base64_data = get_base64(full_path)
        if base64_data is None:
            return match.group(0)
        
        mime_type = get_mime_type(full_path)
        data_uri = f"data:{mime_type};base64,{base64_data}"
        embedded_count += 1
        
        return f"url({quote}{data_uri}{quote})"
    
    # Pattern 2: src="path" or src='path'
    def replace_src(match):
        nonlocal embedded_count
        quote = match.group(1)
        asset_path = match.group(2)
        # Remove query parameters
        asset_path = asset_path.split('?')[0]
        
        full_path = os.path.join(base_dir, asset_path)
        
        if not os.path.exists(full_path):
            print(f"Warning: Asset not found: {full_path}")
            return match.group(0)
        
        file_size = os.path.getsize(full_path)
        print(f"Embedding: {asset_path} ({file_size / 1024:.1f} KB)")
        
        base64_data = get_base64(full_path)
        if base64_data is None:
            return match.group(0)
        
        mime_type = get_mime_type(full_path)
        data_uri = f"data:{mime_type};base64,{base64_data}"
        embedded_count += 1
        
        return f'src={quote}{data_uri}{quote}'
    
    # Replace url() references
    html_content = re.sub(r"url\((['\"]?)(assets/[^'\")\s]+)\1\)", replace_url, html_content)
    
    # Replace src= references
    html_content = re.sub(r'src=(["\'])(assets/[^"\']+)\1', replace_src, html_content)
    
    print(f"\nTotal assets embedded: {embedded_count}")
    
    return html_content

def inline_google_fonts(html_content):
    """Replace Google Fonts link with a fallback"""
    # For AppLovin, we'll use system fonts only to reduce size
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
    print("Building AppLovin-compatible HTML file")
    print("=" * 60)
    
    # Read original HTML
    with open(input_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print(f"\nOriginal HTML size: {len(html_content) / 1024:.1f} KB")
    
    # Inline Google Fonts
    html_content = inline_google_fonts(html_content)
    
    # Embed all assets
    print("\nEmbedding assets...")
    html_content = embed_assets(html_content, base_dir)
    
    # Write output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    final_size = os.path.getsize(output_file)
    print("\n" + "=" * 60)
    print(f"✓ Created: {output_file}")
    print(f"✓ Final size: {final_size / 1024 / 1024:.2f} MB ({final_size / 1024:.1f} KB)")
    
    if final_size > 5 * 1024 * 1024:
        print("\n⚠️  WARNING: File exceeds 5MB AppLovin limit!")
        print("   Consider removing audio or optimizing images further.")
    elif final_size > 2 * 1024 * 1024:
        print("\n⚠️  Note: File is over 2MB. Some ad networks prefer smaller files.")
    else:
        print("\n✓ File size is within typical limits!")
    
    print("=" * 60)

if __name__ == '__main__':
    main()

