# fix curl command:
# curl -sSL https://raw.githubusercontent.com/playsetco/html2css/main/html2css.py | python3 - path_to_your_html_file.html

#working command: download script to html folder & run:
# python3 html2css.py index.html

import os
import sys
import re

# Function to extract unique selectors
def extract_selectors(html_content):
    ids = set()
    classes = set()
    tags = set()
    
    # Regex patterns to match tags, ids, and classes
    tag_pattern = re.compile(r'<\s*([a-zA-Z][a-zA-Z0-9]*)\b[^>]*>')
    id_pattern = re.compile(r'id\s*=\s*["\']([^"\']+)["\']')
    class_pattern = re.compile(r'class\s*=\s*["\']([^"\']+)["\']')
    
    for match in tag_pattern.finditer(html_content):
        tag = match.group(1)
        tags.add(tag)
        
        tag_content = match.group(0)
        id_match = id_pattern.search(tag_content)
        if id_match:
            ids.add(id_match.group(1))
        
        class_match = class_pattern.search(tag_content)
        if class_match:
            class_names = class_match.group(1).split()
            for class_name in class_names:
                classes.add(class_name)
    
    return tags, classes, ids

# Function to create CSS content
def create_css_content(tags, classes, ids):
    css_content = ""
    
    for tag in tags:
        css_content += f"{tag} {{\n    /* Add your styles here */\n}}\n\n"
    
    for class_name in classes:
        css_content += f".{class_name} {{\n    /* Add your styles here */\n}}\n\n"
    
    for id_name in ids:
        css_content += f"#{id_name} {{\n    /* Add your styles here */\n}}\n\n"
    
    return css_content

# Main function to read HTML, extract selectors, and write CSS
def generate_css_from_html(html_file_path):
    if not os.path.isfile(html_file_path):
        print(f"The file {html_file_path} does not exist.")
        return
    
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
    
    tags, classes, ids = extract_selectors(html_content)
    css_content = create_css_content(tags, classes, ids)
    
    css_output_path = os.path.splitext(html_file_path)[0] + '.css'
    
    with open(css_output_path, 'w', encoding='utf-8') as css_file:
        css_file.write(css_content)
    
    print(f"CSS file has been generated at {css_output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 html2css.py <path_to_html_file>")
        sys.exit(1)
    
    html_file_path = sys.argv[1]
    generate_css_from_html(html_file_path)
