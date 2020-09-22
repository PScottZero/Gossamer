from mappings import tag_map, css_map
import regex as re
import os

class ConvertToSCSS:
  def __init__(self, folder, style_file):
    self.style_lines = open(folder + '/' + style_file, 'r').readlines()
    self.scss_file = open(folder + '/' + style_file.split('.')[0] + '.scss', 'w')
    self.file_name = folder + '/' + style_file.split('.')[0]

  def convert(self):
    self.write_defaults()
    for line in self.style_lines:
      if (len(line.strip()) != 0):
        if '{' in line:
          tag_line = re.split(r'(\s+)', line)
          for i in range(len(tag_line)):
            tag_line[i] = tag_line[i].lower()
            if tag_line[i] in tag_map:
              tag_line[i] = tag_map[tag_line[i]]
          line = ''.join(tag_line)
        for key, value in css_map.items():
          line = line.replace(key, value)
        if '{' not in line and '}' not in line:
          line = line[:len(line) - 1] + ';\n'
      self.scss_file.write(line)
    self.scss_file.close()
    os.system(f'sass {self.file_name}.scss {self.file_name}.css')

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
