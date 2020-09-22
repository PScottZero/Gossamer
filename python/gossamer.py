from convert_to_html import ConvertToHTML
from convert_to_scss import ConvertToSCSS
import sys

files = sys.argv[1:]
for file in files:
    ext = file.split('.')[-1]
    if ext == 'glayout':
        ConvertToHTML(file)
    elif ext == 'gstyle':
        ConvertToSCSS(file)
    else:
        print(f'Invalid file: {file}')
