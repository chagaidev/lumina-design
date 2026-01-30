import os
import re
import sys

# Define root directory
ROOT_DIR = "lumina_design"
INDEX_FILE = os.path.join(ROOT_DIR, "index.html")

def verify_assets():
    print(f"🔍 Verifying assets in {INDEX_FILE}...\n")
    
    if not os.path.exists(INDEX_FILE):
        print(f"❌ CRITICAL: {INDEX_FILE} not found!")
        sys.exit(1)

    with open(INDEX_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    # Regex patterns for assets
    img_pattern = r'<img[^>]+src=["\']([^"\']+)["\']'
    bg_pattern = r'url\([\'"]?([^"\'\)]+)[\'"]?\)'
    
    images = re.findall(img_pattern, content)
    backgrounds = re.findall(bg_pattern, content)
    
    all_assets = images + backgrounds
    # Remove duplicates and external links (http/https)
    local_assets = list(set([a for a in all_assets if not a.startswith("http")]))
    
    # Remove query parameters (e.g., hero.jpg?v=1)
    cleaned_assets = [asset.split('?')[0] for asset in local_assets]

    missing_count = 0
    
    print(f"📋 Found {len(cleaned_assets)} local asset references:")
    
    for asset in cleaned_assets:
        # Construct full path
        full_path = os.path.join(ROOT_DIR, asset)
        
        if os.path.exists(full_path):
            print(f"   ✅ FOUND: {asset} (Size: {os.path.getsize(full_path)} bytes)")
        else:
            print(f"   ❌ MISSING: {asset} -> Expected at: {full_path}")
            missing_count += 1

    print("\n" + "="*30)
    if missing_count == 0:
        print("✅ SUCCESS: All local assets verified.")
        sys.exit(0)
    else:
        print(f"❌ FAILURE: {missing_count} assets are missing!")
        sys.exit(1)

if __name__ == "__main__":
    verify_assets()
