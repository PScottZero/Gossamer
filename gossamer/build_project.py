from generate_html import HTMLGenerator
from generate_css import CSSGenerator
import shutil
import sys

html_gen = HTMLGenerator(sys.argv[1])
html_gen.parse_root()
css_gen = CSSGenerator(sys.argv[1], html_gen.components)
css_gen.convert()

shutil.copytree(sys.argv[1] + '/assets/', sys.argv[1] + '/build/assets/')
