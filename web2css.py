import sys
import re
from collections import defaultdict
import requests

def read_html_file(file_path):
    try:
        # Try to open the file in read mode
        with open(file_path, 'r') as file:
            return file.read()  # Return the content of the file
    except FileNotFoundError:
        # If the file is not found, return an error message
        return f"File not found: {file_path}. Please check the file path and try again."

def read_html_url(url):
    try:
        # Try to get the content from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.text  # Return the content of the URL
    except requests.RequestException as e:
        # If there is an error, return an error message
        return f"Error fetching URL: {url}. {e}"

def read_css_file(file_path):
    try:
        # Try to open the file in read mode
        with open(file_path, 'r') as file:
            return file.read()  # Return the content of the file
    except FileNotFoundError:
        # If the file is not found, return an error message
        return f"File not found: {file_path}. Please check the file path and try again."

def parse_html_to_css(html_content):
    # Regular expressions to find tags, classes, IDs, and pseudo-classes
    tag_pattern = re.compile(r'<(?!head|title|style|div)(\w+)')
    class_pattern = re.compile(r'class="([^"]+)"')
    id_pattern = re.compile(r'id="([^"]+)"')
    style_pattern = re.compile(r'style="([^"]+)"')
    pseudo_class_pattern = re.compile(r'([.#]?\w+):(\w+)')

    css_dict = defaultdict(set)

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

    # Extract styles from linked stylesheets
    link_pattern = re.compile(r'<link\s+rel="stylesheet"\s+href="([^"]+)"')
    linked_stylesheets = link_pattern.findall(html_content)
    for stylesheet in linked_stylesheets:
        if stylesheet.startswith("http://") or stylesheet.startswith("https://"):
            css_content = read_html_url(stylesheet)
        else:
            css_content = read_css_file(stylesheet)
        default_css_pattern = re.compile(r'([.#]?\w+)\s*{\s*([^}]*)\s*}')
        for match in default_css_pattern.finditer(css_content):
            selector, styles = match.groups()
            css_dict[selector].add(styles.strip())

    # Merge styles for the same selector
    css_content = "/*Welcome*/\n"
    for selector, styles in sorted(css_dict.items(), key=lambda x: x[0].lstrip('.#')):
        merged_styles = "; ".join(filter(None, styles))
        if merged_styles:
            css_content += f"{selector} {{\n    {merged_styles};\n}}\n"
        else:
            css_content += f"{selector} {{\n}}\n"

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
        media_flags = {'--mobile': '(max-width: 480px)', '--tablet': '(min-width: 481px) and (max-width: 767px)', '--tv': '(min-width: 1201px)'}
        active_media_queries = []

        # Check for media flags and store them
        for flag in media_flags.keys():
            if flag in sys.argv:
                active_media_queries.append(media_flags[flag])
                sys.argv.remove(flag)
        
        # Iterate over each file path or URL provided in the command-line arguments
        for path_or_url in sys.argv[1:]:
            if path_or_url.startswith("http://") or path_or_url.startswith("https://"):
                # Read the content from the URL
                html_content = read_html_url(path_or_url)
            else:
                # Read the content of the HTML file
                html_content = read_html_file(path_or_url)
            # Append the content to the combined HTML content
            combined_html_content += html_content + "\n"
        
        # Parse the combined HTML content to CSS
        css_content, css_dict = parse_html_to_css(combined_html_content)
        
        # Print the generated CSS content
        print(css_content)

        # Add media queries if any media flags are active
        if active_media_queries:
            for media_query in active_media_queries:
                media_content = f"@media screen and {media_query} {{\n"
                for selector in sorted(css_dict.keys(), key=lambda x: x[0].lstrip('.#')):
                    if selector not in [":root", "html"]:
                        media_content += f"    {selector} {{\n    }}\n"
                media_content += "}\n"
                print(media_content)
