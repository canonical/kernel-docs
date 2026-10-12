import os
import re
from collections import defaultdict

# Directories to scan
directories = ['how-to', 'reference', 'tutorial', 'explanation']

# Tag patterns
rst_tag_pattern = re.compile(r'^\s*\.\.\s+tags::\s*(.+)', re.IGNORECASE)
md_tag_pattern = re.compile(r'^\s*```\{tags\}\s*(.+)', re.IGNORECASE)

# Tag map: {tag: [file_paths]}
tags = defaultdict(list)

# File processing
def process_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            # Read the whole file: kernel-docs pages require a meta
            # description front matter block before owners/tags, which can
            # push the tags directive past a fixed early-line window.
            lines = f.readlines()
            for i, line in enumerate(lines):
                rst_match = rst_tag_pattern.match(line)
                if rst_match:
                    tag_list = [tag.strip() for tag in rst_match.group(1).split(',')]
                    for tag in tag_list:
                        tags[tag].append(filepath)
                    return
                md_match = md_tag_pattern.match(line)
                if md_match and i + 1 < len(lines) and lines[i + 1].strip() == '```':
                    tag_list = [tag.strip() for tag in md_match.group(1).split(',')]
                    for tag in tag_list:
                        tags[tag].append(filepath)
                    return
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

# Walk through directories
for directory in directories:
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(('.md', '.rst')):
                filepath = os.path.join(root, file)
                process_file(filepath)

# Write to tags.list
with open('tags.list', 'w', encoding='utf-8') as out_file:
    for tag in sorted(tags):
        paths = ', '.join(tags[tag])
        out_file.write(f"{tag} | {paths}\n")

print("tags.list generated.")
