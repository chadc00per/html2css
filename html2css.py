import re
import sys

def extract_ids_and_classes(html_file_path):
    # Read the content of the HTML file
    with open(html_file_path, 'r') as file:
        content = file.read()

    # Find all IDs and classes using regular expressions
    ids = re.findall(r'id="([^"]+)"', content)
    classes = re.findall(r'class="([^"]+)"', content)

    # Create CSS content
    css_content = ""
    for id in ids:
        css_content += f"#{id} {{\n    /* Add your styles here */\n}}\n\n"
    for class_list in classes:
        for class_name in class_list.split():
            css_content += f".{class_name} {{\n    /* Add your styles here */\n}}\n\n"

    # Define output CSS file path
    css_file_path = html_file_path.replace('.html', '.css')

    # Write the CSS file
    with open(css_file_path, 'w') as file:
        file.write(css_content)

    print(f"Generated {css_file_path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python html2css.py <html_file_path>")
    else:
        html_file_path = sys.argv[1]
        extract_ids_and_classes(html_file_path)

        """
        Instructions to Run the Script:

        1. Ensure you have Python installed on your system. You can download it from https://www.python.org/downloads/.
        2. Save the script in a file named `html2css.py`.
        3. Open a terminal or command prompt.
        4. Navigate to the directory where `html2css.py` is saved.
        5. Make sure you have an HTML file that you want to process. For example, `example.html`.
        6. Run the script by executing the following command:
           python html2css.py <html_file_path>
           Replace `<html_file_path>` with the path to your HTML file. For example:
           python html2css.py example.html
        7. After running the script, a new CSS file will be generated in the same directory as your HTML file. The CSS file will have the same name as your HTML file but with a `.css` extension.
        8. Open the generated CSS file to see the extracted IDs and classes with placeholder styles.

        Example:
        If you have an HTML file named `example.html`, you would run:
           python html2css.py example.html
        This will generate a file named `example.css` in the same directory.
        """
