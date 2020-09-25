from mappings import tag_map, css_map
import regex as re
import os

class CSSGenerator:
  def __init__(self, style_dir):
    self.style_file = open(style_dir, 'r').readlines()
    self.scss_file = open(style_dir.split('.')[0] + '.scss', 'w')
    self.style_dir = style_dir.split('.')[0]
    self.convert()

  def convert(self):
    self.write_defaults()
    for line in self.style_file:
      if (len(line.strip()) != 0):
        if '{' in line:
          line = self.modify_tag(line)
        for key, value in css_map.items():
          line = line.replace(key, value)
        if '{' not in line and '}' not in line:
          line = line[:-1] + ';\n'
      self.scss_file.write(line)
    self.scss_file.close()
    os.system(f'sass {self.style_dir}.scss {self.style_dir}.css')

  def modify_tag(self, line):
    tag_line = re.split(r'(\s+)', line)
    for i in range(len(tag_line)):
      tag_line[i] = tag_line[i].lower()
      if tag_line[i] in tag_map:
        tag_line[i] = tag_map[tag_line[i]]
    return ''.join(tag_line)

  def write_defaults(self):
    self.scss_file.write(
      '* {\n' +
      '\tborder: 0;\n'
      '\tmargin: 0;\n'
      '\tpadding: 0;\n'
      '\tfont-family: Arial, Helvetica, sans-serif;\n'
      '}\n\n' +
      'body {\n' +
      '\twidth: 100vw;\n' +
      '\theight: 100vh;\n' +
      '}\n\n'
    )
