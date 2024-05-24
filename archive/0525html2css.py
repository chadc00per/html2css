import os
import sys
import re
import requests

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
        if tag not in ['h6', 'blockquote', 'figure']:
            tags.add(tag)
        
        tag_content = match.group(0)
        for id_match in id_pattern.finditer(tag_content):
            ids.add(id_match.group(1))
        
        for class_match in class_pattern.finditer(tag_content):
            class_names = class_match.group(1).split()
            for class_name in class_names:
                classes.add(class_name)
    
    return tags, classes, ids

# Function to fetch external CSS
def fetch_external_css(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""

# Function to check if a CSS selector matches any of the extracted HTML selectors
def is_selector_matching(selector, tags, classes, ids):
    if selector.startswith('.'):
        return selector[1:] in classes
    elif selector.startswith('#'):
        return selector[1:] in ids
    else:
        return selector in tags

# Function to filter and combine external CSS based on selectors in HTML
def filter_external_css(external_css, tags, classes, ids):
    filtered_css = {}
    css_rules = re.findall(r'([^{]+){([^}]+)}', external_css)
    
    for selector, properties in css_rules:
        selector = selector.strip()
        
        # Split complex selectors into individual selectors
        sub_selectors = re.split(r'\s*,\s*', selector)
        match = False
        for sub_selector in sub_selectors:
            if is_selector_matching(sub_selector, tags, classes, ids):
                match = True
                break
        
        if match:
            if selector not in filtered_css:
                filtered_css[selector] = properties.strip()
            else:
                filtered_css[selector] += " " + properties.strip()
    
    combined_css = ""
    for selector, properties in filtered_css.items():
        combined_css += f"{selector} {{{properties}}}\n"
    
    return combined_css

# Function to create CSS content
def create_css_content(tags, classes, ids, external_css=""):
    filtered_external_css = filter_external_css(external_css, tags, classes, ids) if external_css else ""
    
    # Extract root styles from external CSS
    root_styles = ""
    root_match = re.search(r':root\s*{([^}]*)}', external_css)
    if root_match:
        root_styles = root_match.group(1).strip()
    
    css_content = f":root {{\n    {root_styles}\n}}\n\n" + filtered_external_css + "\n"
    
    # Ensure specific tags are at the top
    for tag in ['html', 'body', 'header', 'footer']:
        if tag in tags:
            css_content += f"{tag} {{\n    /* Add your styles here */\n}}\n\n"
            tags.remove(tag)
    
    for tag in sorted(tags):
        if tag not in filtered_external_css:
            css_content += f"{tag} {{\n    /* Add your styles here */\n}}\n\n"
    
    for class_name in sorted(classes, key=lambda x: x.lower()):
        if f".{class_name}" not in filtered_external_css:
            css_content += f".{class_name} {{\n    /* Add your styles here */\n}}\n\n"
    
    for id_name in sorted(ids, key=lambda x: x.lower()):
        if f"#{id_name}" not in filtered_external_css:
            css_content += f"#{id_name} {{\n    /* Add your styles here */\n}}\n\n"
    
    return css_content

# Function to create media query CSS content
def create_media_css_content(tags, classes, ids, media_type, external_css=""):
    media_filtered_css = {}
    css_rules = re.findall(r'@media\s*([^{]+){([^}]+)}', external_css, re.DOTALL)
    
    for media_query, media_content in css_rules:
        if media_type in media_query:
            # Extract individual CSS rules within the media query
            inner_css_rules = re.findall(r'([^{]+){([^}]+)}', media_content)
            for selector, properties in inner_css_rules:
                selector = selector.strip()
                sub_selectors = re.split(r'\s*,\s*', selector)
                match = False
                for sub_selector in sub_selectors:
                    if is_selector_matching(sub_selector, tags, classes, ids):
                        match = True
                        break
                if match:
                    if selector not in media_filtered_css:
                        media_filtered_css[selector] = properties.strip()
                    else:
                        media_filtered_css[selector] += " " + properties.strip()
    
    combined_media_css = f"@media {media_type} {{\n"
    for selector, properties in media_filtered_css.items():
        combined_media_css += f"    {selector} {{{properties}}}\n"
    combined_media_css += "}\n"
    
    return combined_media_css

# Function to create base CSS content without external properties
def create_base_css_content(tags, classes, ids):
    css_content = ""
    
    # Ensure specific tags are at the top
    for tag in ['html', 'body', 'header', 'footer']:
        if tag in tags:
            css_content += f"{tag} {{\n    /* Add your styles here */\n}}\n\n"
            tags.remove(tag)
    
    for tag in sorted(tags):
        css_content += f"{tag} {{\n    /* Add your styles here */\n}}\n\n"
    
    for class_name in sorted(classes, key=lambda x: x.lower()):
        css_content += f".{class_name} {{\n    /* Add your styles here */\n}}\n\n"
    
    for id_name in sorted(ids, key=lambda x: x.lower()):
        css_content += f"#{id_name} {{\n    /* Add your styles here */\n}}\n\n"
    
    return css_content

# Main function to read HTML, extract selectors, and write CSS
def generate_css_from_html(html_file_path, external_css_url=None, generate_mobile=False, generate_tablet=False, generate_tv=False, use_default_style=False):
    if not os.path.isfile(html_file_path):
        print(f"The file {html_file_path} does not exist.")
        return
    
    with open(html_file_path, 'r', encoding='utf-8') as html_file:
        html_content = html_file.read()
    
    tags, classes, ids = extract_selectors(html_content)
    
    # Fetch external CSS if URL is provided, otherwise use default or none
    if external_css_url == "none":
        external_css = ""
    elif use_default_style:
        external_css = fetch_external_css("https://raw.githubusercontent.com/playsetco/template/main/styles.css")
    else:
        external_css = fetch_external_css(external_css_url) if external_css_url else ""
    
    base_css_content = create_base_css_content(tags.copy(), classes.copy(), ids.copy())
    external_css_content = create_css_content(tags.copy(), classes.copy(), ids.copy(), external_css)
    
    # Generate regular CSS file
    css_output_path = os.path.splitext(html_file_path)[0] + '.css'
    with open(css_output_path, 'w', encoding='utf-8') as css_file:
        css_file.write(external_css_content)
    print(f"CSS file has been generated at {css_output_path}")
    
    if generate_mobile:
        # Generate mobile.css
        mobile_css_content = create_media_css_content(tags.copy(), classes.copy(), ids.copy(), "max-width: 480px", external_css)
        mobile_css_output_path = os.path.splitext(html_file_path)[0] + '_mobile.css'
        with open(mobile_css_output_path, 'w', encoding='utf-8') as mobile_css_file:
            mobile_css_file.write(f"@media max-width: 480px {{\n{base_css_content}\n{mobile_css_content}}}")
        print(f"Mobile CSS file has been generated at {mobile_css_output_path}")
    
    if generate_tablet:
        # Generate tablet.css
        tablet_css_content = create_media_css_content(tags.copy(), classes.copy(), ids.copy(), "min-width: 481px and max-width: 767px", external_css)
        tablet_css_output_path = os.path.splitext(html_file_path)[0] + '_tablet.css'
        with open(tablet_css_output_path, 'w', encoding='utf-8') as tablet_css_file:
            tablet_css_file.write(f"@media min-width: 481px and max-width: 767px {{\n{base_css_content}\n{tablet_css_content}}}")
        print(f"Tablet CSS file has been generated at {tablet_css_output_path}")
    
    if generate_tv:
        # Generate tv.css
        tv_css_content = create_media_css_content(tags.copy(), classes.copy(), ids.copy(), "min-width: 1201px", external_css)
        tv_css_output_path = os.path.splitext(html_file_path)[0] + '_tv.css'
        with open(tv_css_output_path, 'w', encoding='utf-8') as tv_css_file:
            tv_css_file.write(f"@media min-width: 1201px {{\n{base_css_content}\n{tv_css_content}}}")
        print(f"TV CSS file has been generated at {tv_css_output_path}")

# Entry point of the script
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 html2css.py <path_to_html_file> --mobile --tablet --tv --defaultstyle <external_css_url>")
        sys.exit(1)
    
    html_file_path = sys.argv[1]
    external_css_url = sys.argv[-1] if sys.argv[-1].startswith('http') or sys.argv[-1] == "none" else None
    generate_mobile = '--mobile' in sys.argv
    generate_tablet = '--tablet' in sys.argv
    generate_tv = '--tv' in sys.argv
    use_default_style = '--defaultstyle' in sys.argv
    
    generate_css_from_html(html_file_path, external_css_url, generate_mobile, generate_tablet, generate_tv, use_default_style)

