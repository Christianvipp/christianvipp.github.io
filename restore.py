import os
import re

# Paths
md_file = "content/Portfolio/include.md"
image_dir = "static/images"

def restore_obsidian_state():
    # 1. Rename physical image files: Hyphens -> Spaces
    if os.path.exists(image_dir):
        for filename in os.listdir(image_dir):
            if "Pasted-image-" in filename:
                new_name = filename.replace("Pasted-image-", "Pasted image ")
                os.rename(os.path.join(image_dir, filename), os.path.join(image_dir, new_name))
                print(f"Renamed: {filename} -> {new_name}")

    # 2. Update Markdown: Convert to ![[Pasted image ...]]
    if os.path.exists(md_file):
        with open(md_file, 'r') as f:
            content = f.read()
        
        # Regex to find any variation and turn it into Obsidian Wikilinks
        pattern = r'!\[.*\]\(.*Pasted[- ]image[- ](\d+)\.png\)'
        substitution = r'![[Pasted image \1.png]]'
        updated_content = re.sub(pattern, substitution, content)
        
        with open(md_file, 'w') as f:
            f.write(updated_content)
        print(f"Markdown updated to Obsidian format.")

if __name__ == "__main__":
    restore_obsidian_state()
