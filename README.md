# HTML2CSS parser
This script converts an HTML's tags, classes & ID's into a stylesheet.
This will generate the following files in the same directory as the HTML file:
- file.css
- file_mobile.css
- file_tablet.css
- file_tv.css

# Download script to html folder & run:
```
python3 html2css.py path/to/your/file.html --mobile --tablet --tv url/to/external/css.css
```
    
# Parameters:
The script:
```
html2css.py
```

The path to the HTML input source: 
```
path_to_html_file.html
```

# Optional Flags:
Generate a mobile CSS file (max-width: 480px):
```
--mobile
```

Generate a tablet CSS file (min-width: 481px and max-width: 767px):
```
--tablet
```

Generate a TV CSS file (min-width: 1201px):
```    
--tv
```

Use properties from external CSS:
```
url_to_css.css
```

# Testing
Use test HTML to test code which will render output files in same directory.

Run with:
```
./test.sh
```

Install/enable run script by running:
```
chmod +x test.sh one time
```