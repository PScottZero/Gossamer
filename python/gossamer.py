import convert_to_html as cth
import convert_to_scss as ctc

html_converter = cth.ConvertToHTML('demo', 'demo.glayout')
html_converter.convert()
css_converter = ctc.ConvertToSCSS('demo', 'demo.gstyle')
css_converter.convert()
