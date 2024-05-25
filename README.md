# HTML2CSS parser
This script converts an HTML's tags, classes & ID's into a stylesheet.

## Run
```
python3 html2css.py path/to/your/file.html --mobile --tablet --tv --defaultstyle
```
    
## Parameters
The script:
```
html2css.py
```

The path to the HTML input source: 
```
path_to_html_file.html
```

### Optional Flags:
Generate mobile CSS @media screens (max-width: 480px):
```
--mobile
```

Generate tablet CSS @media screens (min-width: 481px and max-width: 767px):
```
--tablet
```

Generate TV CSS @media screens (min-width: 1201px):
```    
--tv
```

Add default styles:
```    
--defaultstyle
```

#### Default Styles
https://raw.githubusercontent.com/playsetco/template/main/styles.css

## Testing
Use test HTML to test code which will print the output.

Test with:
```
./test.sh
```

### Install/enable run & test scripts ONE TIME:
```
chmod +x test.sh
```