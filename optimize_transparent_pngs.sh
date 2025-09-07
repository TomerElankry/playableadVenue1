#!/bin/bash

# PNG Optimization Script for Transparent Assets
# Reduces PNG file sizes while maintaining transparency

echo "🎨 Starting PNG optimization for transparent assets..."

SOURCE_DIR="/Users/tomerelankry/Desktop/assets"
TARGET_DIR="/Users/tomerelankry/Desktop/playableadVenue1/assets"

# Function to optimize PNG files
optimize_png_category() {
    local category=$1
    local source_folder=$2
    local target_size="1500000"  # 1.5MB in bytes
    
    echo "🔧 Optimizing $category PNGs..."
    
    mkdir -p "$TARGET_DIR/items/$category/view"
    mkdir -p "$TARGET_DIR/thumbs/$category"
    
    counter=1
    
    for file in "$SOURCE_DIR/$source_folder"/*.png; do
        if [ -f "$file" ]; then
            echo "   Processing $(basename "$file") -> $category/$counter"
            
            # Get original file size
            original_size=$(stat -f%z "$file" 2>/dev/null || echo "0")
            
            if [ "$original_size" -le "$target_size" ]; then
                echo "     ✓ Already under 1.5MB, copying directly"
                cp "$file" "$TARGET_DIR/items/$category/view/$counter.png"
            else
                echo "     🔧 Optimizing from $(echo "$original_size" | awk '{print int($1/1024/1024*10)/10"MB"}')"
                
                # Method 1: Reduce dimensions to fit size
                max_width=600
                while [ "$max_width" -gt 200 ]; do
                    sips -Z "$max_width" "$file" --out "/tmp/temp_$counter.png" >/dev/null 2>&1
                    temp_size=$(stat -f%z "/tmp/temp_$counter.png" 2>/dev/null || echo "999999999")
                    
                    if [ "$temp_size" -le "$target_size" ]; then
                        mv "/tmp/temp_$counter.png" "$TARGET_DIR/items/$category/view/$counter.png"
                        final_size=$(stat -f%z "$TARGET_DIR/items/$category/view/$counter.png" 2>/dev/null || echo "0")
                        echo "     ✓ Optimized to ${max_width}px ($(echo "$final_size" | awk '{print int($1/1024/1024*10)/10"MB"}'))"
                        break
                    fi
                    max_width=$((max_width - 50))
                done
                
                # If still too large, use aggressive compression
                if [ ! -f "$TARGET_DIR/items/$category/view/$counter.png" ]; then
                    echo "     ⚡ Using aggressive compression..."
                    sips -Z 400 "$file" --out "$TARGET_DIR/items/$category/view/$counter.png" >/dev/null 2>&1
                fi
            fi
            
            # Create thumbnail (always small)
            sips -Z 120 "$TARGET_DIR/items/$category/view/$counter.png" --out "$TARGET_DIR/thumbs/$category/$counter.png" >/dev/null 2>&1
            
            # Create item copy
            cp "$TARGET_DIR/items/$category/view/$counter.png" "$TARGET_DIR/items/$category/item/$counter.png"
            
            # Verify final size
            final_size=$(stat -f%z "$TARGET_DIR/items/$category/view/$counter.png" 2>/dev/null || echo "0")
            if [ "$final_size" -gt "$target_size" ]; then
                echo "     ⚠️  WARNING: Still $(echo "$final_size" | awk '{print int($1/1024/1024*10)/10"MB"}') - may need manual optimization"
            fi
            
            ((counter++))
        fi
    done
    
    echo "   ✅ $category complete - processed $((counter-1)) items"
}

# Process all categories with transparent PNGs
optimize_png_category "windows" "windows catalog"
optimize_png_category "chandelier" "bed chandelier catalog" 
optimize_png_category "bed_frame" "bed frames catalog"
optimize_png_category "bed_sheets" "bed sheets catalog"
optimize_png_category "floor" "floors catalog"

echo ""
echo "📋 Usage Instructions:"
echo "1. Put your transparent PNGs in the original asset folders"
echo "2. Uncomment the categories you want to process above"
echo "3. Run: ./optimize_transparent_pngs.sh"
echo ""
echo "🎯 Target: Each PNG will be optimized to ≤1.5MB while keeping transparency"
echo ""
echo "💡 Manual alternatives if script doesn't work:"
echo "   - Use ImageOptim (Mac app) - drag & drop your PNGs"
echo "   - Use TinyPNG.com - upload and download optimized versions"
echo "   - Use Photoshop: Save for Web -> PNG-24 with transparency"