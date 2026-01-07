#!/usr/bin/env python3
"""
Fix Hugo site issues:
1. URL-encode spaces in image paths
2. Fix malformed shortcodes in brains.md
"""

import re
from pathlib import Path
from urllib.parse import quote

def url_encode_image_paths(content):
    """
    URL-encode spaces in image paths.
    ![alt](/images/Pasted image.png) -> ![alt](/images/Pasted%20image.png)
    """
    def encode_path(match):
        alt = match.group(1)
        path = match.group(2)
        # Only encode the filename part after /images/
        if '/images/' in path:
            parts = path.split('/images/')
            filename = quote(parts[1])
            encoded_path = f'/images/{filename}'
            return f'![{alt}]({encoded_path})'
        return match.group(0)
    
    pattern = r'!\[([^\]]*)\]\((/images/[^)]+)\)'
    return re.sub(pattern, encode_path, content)

def fix_brains_shortcodes(content):
    """
    Fix malformed Hugo shortcodes in brains.md
    {{< figure src="/path"->}} -> ![](/path)
    {{<-figure-src="/path"->}} -> ![](/path)
    """
    # Fix malformed figure shortcodes - convert to markdown images
    content = re.sub(
        r'{{<-?\s*figure\s*src\s*=\s*"([^"]+)"\s*-?>}}',
        r'![\1](\1)',
        content
    )
    
    # Clean up text artifacts (excessive dashes)
    content = re.sub(r'(\w)-(\s)', r'\1\2', content)
    content = re.sub(r'(\w)-$', r'\1', content, flags=re.MULTILINE)
    content = re.sub(r'\.-([\w\s])', r'. \1', content)
    content = re.sub(r'-(\d)', r' \1', content)
    
    return content

def process_file(filepath):
    """Process a single markdown file."""
    print(f"Processing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Apply fixes based on filename
    if filepath.name == 'brains.md':
        print("  Fixing brains.md shortcodes...")
        content = fix_brains_shortcodes(content)
    
    # URL-encode image paths for all files
    print("  URL-encoding image paths...")
    content = url_encode_image_paths(content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✓ Fixed")
        return True
    else:
        print("  ✓ No changes needed")
        return False

def main():
    """Find and process all markdown files in content directory."""
    content_dir = Path('content')
    
    if not content_dir.exists():
        print("❌ Error: 'content' directory not found!")
        return
    
    # Find all markdown files
    md_files = list(content_dir.rglob('*.md'))
    
    if not md_files:
        print("❌ No markdown files found")
        return
    
    print(f"Found {len(md_files)} markdown file(s)\n")
    
    fixed_count = 0
    for md_file in md_files:
        if process_file(md_file):
            fixed_count += 1
        print()
    
    print("="*50)
    print(f"✓ Processing complete!")
    print(f"  Files checked: {len(md_files)}")
    print(f"  Files modified: {fixed_count}")
    print("\nNext steps:")
    print("  1. Review: git diff")
    print("  2. Test: hugo server")
    print("  3. Commit: git add . && git commit -m 'Fix image paths and shortcodes'")
    print("  4. Push: git push")

if __name__ == '__main__':
    main()
