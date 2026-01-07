import os
import re

# Paths
md_file = "content/Portfolio/include.md"
image_dir = "static/images"

def restore_to_obsidian_format():
    # 1. Rename physical image files: replace hyphens with spaces
    if os.path.exists(image_dir):
        for filename in os.listdir(image_dir):
            if "Pasted-image-" in filename:
                new_name = filename.replace("Pasted-image-", "Pasted image ")
                old_path = os.path.join(image_dir, filename)
                new_path = os.path.join(image_dir, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed file: {filename} -> {new_name}")

    # 2. Update Markdown to Obsidian internal link format: ![[Pasted image YYYYMMDDHHMMSS.png]]
    if os.path.exists(md_file):
        with open(md_file, 'r') as f:
            content = f.read()
        
        # Regex to find standard markdown images and convert to Obsidian wiki-links
        # Finds ![](/images/Pasted-image-NUMBER.png) or ![](/images/Pasted image NUMBER.png)
        pattern = r'!\[\]\(/images/Pasted[- ]image[- ](\d+)\.png\)'
        substitution = r'![[Pasted image \1.png]]'
        
        updated_content = re.sub(pattern, substitution, content)
        
        with open(md_file, 'w') as f:
            f.write(updated_content)
        print(f"Updated {md_file} to Obsidian format: ![[Pasted image ...]]")

if __name__ == "__main__":
    restore_to_obsidian_format()
