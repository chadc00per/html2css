import re

def alphabetize_css_selectors(css_code):
    """
    Alphabetizes the CSS selectors in the given CSS code.

    Args:
        css_code (str): The CSS code as a string.

    Returns:
        str: The CSS code with selectors alphabetized.
    """
    # Regex pattern to match CSS rules
    pattern = re.compile(r'([^{]+)\{([^}]+)\}')
    matches = pattern.findall(css_code)
    
    # Sort the selectors alphabetically
    sorted_matches = sorted(matches, key=lambda x: x[0].strip())
    
    # Reconstruct the CSS code
    sorted_css_code = ''
    for selector, properties in sorted_matches:
        sorted_css_code += f'{selector} {{{properties}}}\n'
    
    return sorted_css_code.strip()

def read_css_file(file_path):
    """
    Reads the content of a CSS file.

    Args:
        file_path (str): The path to the CSS file.

    Returns:
        str: The content of the CSS file.
    """
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        return f"File not found: {file_path}. Please check the file path and try again."

# How to use this function
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python alphacss.py path/to/your/file.css")
    else:
        css_file_path = sys.argv[1]
        css_code = read_css_file(css_file_path)
        
        if "File not found" in css_code:
            print(css_code)
        else:
            # Alphabetize the CSS selectors
            sorted_css_code = alphabetize_css_selectors(css_code)
            
            # Print the sorted CSS code
            print(sorted_css_code)
