import sys  # Import the sys module to access command-line arguments
import re   # Import the re module for regular expressions
from collections import defaultdict

def read_html_file(file_path):
    try:
        # Try to open the file in read mode
        with open(file_path, 'r') as file:
            return file.read()  # Return the content of the file
    except FileNotFoundError:
        # If the file is not found, return an error message
        return f"File not found: {file_path}. Please check the file path and try again."

def read_css_file(file_path):
    try:
        # Try to open the file in read mode
        with open(file_path, 'r') as file:
            return file.read()  # Return the content of the file
    except FileNotFoundError:
        # If the file is not found, return an error message
        return f"File not found: {file_path}. Please check the file path and try again."

def parse_html_to_css(html_content, default_css_content=None):
    # Regular expressions to find tags, classes, IDs, and pseudo-classes
    tag_pattern = re.compile(r'<(?!head|title|style|div)(\w+)')
    class_pattern = re.compile(r'class="([^"]+)"')
    id_pattern = re.compile(r'id="([^"]+)"')
    style_pattern = re.compile(r'style="([^"]+)"')
    pseudo_class_pattern = re.compile(r'([.#]?\w+):(\w+)')

    css_dict = defaultdict(set)

    # Add :root{} at the very top
    css_dict[":root"] = set()

    # Find all tags
    tags = tag_pattern.findall(html_content)
    for tag in tags:
        css_dict[tag].add("")

    # Find all classes
    classes = class_pattern.findall(html_content)
    for class_list in classes:
        for class_name in class_list.split():
            css_dict[f".{class_name}"].add("")

    # Find all IDs
    ids = id_pattern.findall(html_content)
    for id_name in ids:
        css_dict[f"#{id_name}"].add("")

    # Find all inline styles
    for match in re.finditer(r'<(\w+)[^>]*style="([^"]+)"[^>]*>', html_content):
        tag, style = match.groups()
        css_dict[tag].add(style)

    # Apply default styles if provided, but only to selectors already found in HTML
    if default_css_content:
        default_css_pattern = re.compile(r'([.#]?\w+)\s*{\s*([^}]*)\s*}')
        root_pattern = re.compile(r':root\s*{\s*([^}]*)\s*}')
        
        # Extract and add :root styles
        root_match = root_pattern.search(default_css_content)
        if root_match:
            root_styles = root_match.group(1).strip()
            css_dict[":root"].add(root_styles)
        
        for match in default_css_pattern.finditer(default_css_content):
            selector, styles = match.groups()
            if selector in css_dict:
                css_dict[selector].add(styles.strip())
            elif selector == ":root":
                css_dict[":root"].add(styles.strip())

        # Include pseudo-classes if they match existing selectors
        for match in pseudo_class_pattern.finditer(default_css_content):
            base_selector, pseudo_class = match.groups()
            if base_selector in css_dict:
                css_dict[f"{base_selector}:{pseudo_class}"].update(css_dict[base_selector])

    # Merge styles for the same selector
    css_content = "/*Welcome*/\n"
    for selector, styles in sorted(css_dict.items(), key=lambda x: x[0].lstrip('.#')):
        merged_styles = "; ".join(filter(None, styles))
        if merged_styles:
            css_content += f"{selector} {{ {merged_styles}; }}\n"
        else:
            css_content += f"{selector} {{ }}\n"

    # Remove any duplicate semicolons
    css_content = re.sub(r';{2,}', ';', css_content)

    return css_content, css_dict

if __name__ == "__main__":
    # Check if the number of command-line arguments is less than 2
    if len(sys.argv) < 2:
        # Print usage instructions if the number of arguments is incorrect
        print("Usage: python3 test.py path/to/your/file1.html path/to/your/file2.html ... --defaultstyle --mobile --tablet --tv")
    else:
        # Initialize an empty string to hold the combined HTML content
        combined_html_content = ""
        default_css_content = None
        media_flags = {'--mobile': '(max-width: 480px)', '--tablet': '(min-width: 481px) and (max-width: 767px)', '--tv': '(min-width: 1201px)'}
        active_media_queries = []

        # Check for --defaultstyle flag and read the default CSS file if present
        if '--defaultstyle' in sys.argv:
            default_css_path = "default.css"
            default_css_content = read_css_file(default_css_path)
            # Remove the flag from the arguments list
            sys.argv.remove('--defaultstyle')
        
        # Check for media flags and store them
        for flag in media_flags.keys():
            if flag in sys.argv:
                active_media_queries.append(media_flags[flag])
                sys.argv.remove(flag)
        
        # Iterate over each file path provided in the command-line arguments
        for file_path in sys.argv[1:]:
            # Read the content of the HTML file
            html_content = read_html_file(file_path)
            # Append the content to the combined HTML content
            combined_html_content += html_content + "\n"
        
        # Parse the combined HTML content to CSS
        css_content, css_dict = parse_html_to_css(combined_html_content, default_css_content)
        
        # Print the generated CSS content
        print(css_content)

        # Add media queries if any media flags are active
        if active_media_queries:
            for media_query in active_media_queries:
                media_content = f"@media screen and {media_query} {{\n"
                for selector in sorted(css_dict.keys(), key=lambda x: x.lstrip('.#')):
                    if selector not in [":root", "html"]:
                        media_content += f"  {selector} {{ }}\n"
                media_content += "}\n"
                print(media_content)
