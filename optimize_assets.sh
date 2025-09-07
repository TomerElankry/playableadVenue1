#!/bin/bash

# Asset optimization script for Cabin Design Playable Ad
# Converts PNG to optimized JPEG and creates thumbnails

echo "🏔️ Starting Cabin Design Asset Optimization..."

# Base directories
SOURCE_DIR="/Users/tomerelankry/Desktop/assets"
TARGET_DIR="/Users/tomerelankry/Desktop/playableadVenue1/assets"

# Process cabin background (already done, but keeping for reference)
echo "📸 Processing cabin background..."
if [ ! -f "$TARGET_DIR/bg/cabin_base.jpg" ]; then
    sips -s format jpeg -s formatOptions high "$SOURCE_DIR/cabin .png" --out "$TARGET_DIR/bg/cabin_base.jpg"
fi

# Function to process category assets
process_category() {
    local category=$1
    local source_folder=$2
    
    echo "🛠️  Processing $category assets..."
    
    # Create directories if they don't exist
    mkdir -p "$TARGET_DIR/items/$category/view"
    mkdir -p "$TARGET_DIR/thumbs/$category"
    
    # Counter for naming
    counter=1
    
    # Process each PNG file in the source folder
    for file in "$SOURCE_DIR/$source_folder"/*.png; do
        if [ -f "$file" ]; then
            echo "   Converting $(basename "$file") -> $category/$counter"
            
            # Create view image (800px max, 85% quality for better detail)
            sips -Z 800 -s format jpeg -s formatOptions 85 "$file" --out "$TARGET_DIR/items/$category/view/$counter.jpg"
            
            # Create thumbnail (120px, 75% quality)
            sips -Z 120 -s format jpeg -s formatOptions 75 "$file" --out "$TARGET_DIR/thumbs/$category/$counter.jpg"
            
            # Create item copy (same as view for this implementation)
            cp "$TARGET_DIR/items/$category/view/$counter.jpg" "$TARGET_DIR/items/$category/item/$counter.jpg"
            
            ((counter++))
        fi
    done
    
    echo "   ✅ $category complete - processed $((counter-1)) items"
}

# Process all categories
process_category "windows" "windows catalog"
process_category "chandelier" "bed chandelier catalog" 
process_category "bed_frame" "bed frames catalog"
process_category "bed_sheets" "bed sheets catalog"
process_category "floor" "floors catalog"

echo ""
echo "📊 Optimization Summary:"
echo "  Cabin background: $(ls -lah "$TARGET_DIR/bg/cabin_base.jpg" 2>/dev/null | awk '{print $5}' || echo 'Not found')"

for category in windows chandelier bed_frame bed_sheets floor; do
    view_count=$(ls "$TARGET_DIR/items/$category/view/" 2>/dev/null | wc -l | xargs)
    thumb_count=$(ls "$TARGET_DIR/thumbs/$category/" 2>/dev/null | wc -l | xargs)
    echo "  $category: $view_count views, $thumb_count thumbs"
done

echo ""
echo "🎯 Total bundle size estimate:"
du -sh "$TARGET_DIR" 2>/dev/null || echo "Bundle size calculation failed"

echo ""
echo "✅ Asset optimization complete!"
echo "📁 Assets ready at: $TARGET_DIR"
echo ""
echo "📝 Next steps:"
echo "   1. Update HTML to use .jpg extensions instead of .webp"
echo "   2. Test the playable ad in browser"
echo "   3. Optimize further if bundle exceeds 5MB"