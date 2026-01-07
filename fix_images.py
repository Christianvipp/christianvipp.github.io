import os
import re

# Set paths relative to the root of your Hugo project
image_dir = "static/images"
content_dir = "content"

print("--- Renaming Images in static/images ---")
# 1. Rename files: Replace spaces with hyphens
for filename in os.listdir(image_dir):
    if " " in filename:
        old_path = os.path.join(image_dir, filename)
        new_filename = filename.replace(" ", "-")
        new_path = os.path.join(image_dir, new_filename)
        
        # Avoid overwriting if a file with the new name already exists
        if not os.path.exists(new_path):
            os.rename(old_path, new_path)
            print(f"Renamed: '{filename}' -> '{new_filename}'")
        else:
            print(f"Skipped (already exists): {new_filename}")

print("\n--- Updating Markdown Links in content/ ---")
# 2. Update Markdown files to match new filenames
for root, dirs, files in os.walk(content_dir):
    for file in files:
        if file.endswith(".md"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                original_content = f.read()
            
            # This regex finds /images/Pasted image... and replaces spaces with hyphens
            # specifically for the "Pasted image" format seen in your screenshots
            updated_content = re.sub(
                r'(/images/Pasted\simage\s[^)]+\.png)', 
                lambda m: m.group(1).replace(" ", "-"), 
                original_content
            )
            
            if original_content != updated_content:
                with open(path, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print(f"Updated links in: {path}")

print("\nCleanup complete. Run 'git status' to see the changes.")
