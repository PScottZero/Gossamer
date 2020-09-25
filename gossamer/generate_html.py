from mappings import tag_map
import os

class HTMLGenerator:
  def __init__(self, project_dir):
    self.src_dir = project_dir + '/src/'
    self.build_dir = project_dir + '/build/'
    self.html_file = open(self.build_dir + 'index.html', 'w')
    self.tab_depth = 0
    os.mkdir(self.build_dir)

  def parse_root(self):
    root_file = open(self.src_dir + 'main.layout.gsm', 'r')

    # write html header
    self.write_html_header()
    root_file.readline()
    line = self.next_line(root_file)

    # read root attributes
    while self.is_attribute_line(line):
      attr, value = line.split(': ')
      if attr.strip() == 'title':
        self.html_file.write('  <title>' + value.strip() + '</title>\n'),
      elif attr.strip() == 'icon':
        self.html_file.write('  <link rel="icon" type="image/svg+xml" href="' + value.strip() + '">\n')
      elif attr.strip() == 'alt-icon':
        self.html_file.write('  <link rel="alternate icon" href="' + value.strip() + '">\n')
      line = self.next_line(root_file)
    self.html_file.write('</head>\n<body>\n')

    # read tags and components
    while not self.is_closure(line):
      if self.is_component(line):
        inputs = 
        self.parse_component(line)
      elif self.is_tag(line):
        tag_name, tag_ids = self.get_tag(line)
        self.parse_tag(tag_name, tag_ids)
        line = root_file.readline()
    
    # close html
    if self.is_closure(line):
      self.html_file.write('</body>\n</html>\n')

  def parse_component(self, inputs):
    if '{' in curr_line:
      input_map = {}
      while self.is_attribute_line(line):
        key, value = line.split(':')
        input_map[key] = value
        line = self.next_line()
    component_file = open(self.src_dir + '/components/' + component_name + '.layout.gsm', 'r')
    component_file.readline()
    line = self.next_line(component_file)

    # parse component inputs
    input_map = {}
    while '@Input' in line:
      component_inputs


  def parse_tag(self, tag_name, tag_ids, file):

    # write html tag
    self.tab_depth += 1
    tag_line = self.get_tab() + '<' + tag_name + ' ' + tag_ids
    
    # write attributes or text
    if tag_name == 'p':
      tag_line += '>\n'
      self.html_file.write(tag_line)
      self.get_text(file)
    else:
      tag_line += self.get_attributes(file) + '>\n'
      self.html_file.write(tag_line)

    # check for nested tags
    while self.is_tag(line):
      new_tag_name, new_tag_ids = self.get_tag(line)
      self.parse_tag(new_tag_name, new_tag_ids)
      line = self.next_line()

    # close tag
    if self.is_closure(line):
      self.html_file.write(tab + '</' + tag_name + '>\n')
    self.tab_depth -= 1
      
  def get_tag(self, line):
    tag_and_ids = line.split()
    tag_name = tag_and_ids[0].lower()
    tag_ids = tag_and_ids[1:-1]
    tag_line = ''
    
    if len(tag_ids) != 0:
      class_line = 'class="'
      has_classes = False
      for id_or_class in tag_ids:
        if id_or_class[0] == '#':
          tag_line += ' id="' + id_or_class[1:] + '"'
        else:
          has_classes = True
          class_line += id_or_class[1:] + ' '
      if has_classes:
        tag_line += ' ' + class_line.strip() + '"'

    if tag_name in tag_map:
      tag_name = tag_map[tag_name]
    return tag_name, tag_line

  def get_attributes(self, file):
    tag_line = ''
    line = self.next_line(file)
    while self.is_attribute_line(line):
      attr, value = line.split(': ')
      tag_line += ' ' + attr.strip() + '="' + value.strip() + '"'
      line = self.next_line(file)
    return tag_line, line

  def get_text(self, file):
    line = self.next_line(file)
    while not self.is_closure(line):
      self.html_file.write(self.get_tab() + '  ' + line.strip() + '\n')
      line = self.next_line(file)
    return line

  def get_tab(self):
    return '  ' * self.tab_depth

  def is_attribute_line(self, line):
    return not self.is_tag(line) and not self.is_closure(line) and len(line.split(': ')) == 2

  def is_tag(self, line):
    return '{' in line

  def is_component(self, line):
    return '@Component' in line

  def is_closure(self, line):
    return line.strip() == '}'

  def next_line(self, file):
    line = file.readline()
    while len(line.strip()) == 0:
      line = file.readline()
    return line

  def get_component_inputs(self, line, file):
    inputs = {}
    if '{' in line:
      line = self.next_line(file)
      while self.is_attribute_line(line)
        key, value = line.split(':')
        inputs[key] = value
        line = self.next_line(file)
      file.readline()
    return inputs

  def write_html_header(self):
    self.html_file.write(
      '<!doctype html>\n' +
      '<html lang="en">\n' +
      '<head>\n' +
      '  <meta charset="utf-8">\n' +
      '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
      '  <link rel="stylesheet" href="' + self.file_name + '.css">\n'
    )
