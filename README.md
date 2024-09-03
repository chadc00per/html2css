# HTML2CSS Parser
This script converts an HTML's tags, classes & ID's into a CSS stylesheet and optionally applies matching default styles.

### Run
```
python3 html2css.py path/to/your/file.html --mobile --tablet --tv --defaultstyle
```
    
### Parameters
1. The script: `html2css.py`

2. The path to the HTML input source: `path_to_html_file.html`

3. Optional Media Screen Flags:
 - Generate mobile CSS @media screens (max-width: 480px): `--mobile`
 - Generate tablet CSS @media screens (min-width: 481px and max-width: 767px): `--tablet`
 - Generate TV CSS @media screens (min-width: 1201px): `--tv`

4. Optional Default Style Flag: `--defaultstyle`

##### Testing
 - Run with `npm run test`

### Known Issues
 - The default style sheet included in here is junk, it's just for confirming the script works.