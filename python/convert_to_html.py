from mappings import tag_map

class ConvertToHTML:
  def __init__(self, layout_dir):
    self.layout_file = open(layout_dir, 'r')
    self.html_file = open(layout_dir.split('.')[0] + '.html', 'w')
    self.file_name = layout_dir.split('/')[-1].split('.')[0]
    self.tab_depth = 0
    self.convert()

  def convert(self):

    # write html header
    self.write_html_header()
    self.skip_line()
    line = self.next_line()

    # read root attributes
    while self.is_attribute_line(line):
      attr, value = line.split(': ')
      if attr.strip() == 'title':
        self.html_file.write('  <title>' + value.strip() + '</title>\n'),
      elif attr.strip() == 'icon':
        self.html_file.write('  <link rel="icon" type="image/svg+xml" href="' + value.strip() + '">\n')
      elif attr.strip() == 'alt-icon':
        self.html_file.write('  <link rel="alternate icon" href="' + value.strip() + '">\n')
      line = self.next_line()
    self.html_file.write('</head>\n<body>\n')

    # read all tags
    while self.is_tag(line):
      tag_name, tag_ids = self.get_tag(line)
      self.parse_tag(tag_name, tag_ids)
      line = self.next_line()
    
    # close html
    if self.is_closure(line):
      self.html_file.write('</body>\n</html>\n')

  def parse_tag(self, tag_name, tag_ids):

    # write html tag
    self.tab_depth += 1
    tab = '  ' * self.tab_depth
    tag_line = tab + '<' + tag_name
    line = self.next_line()

    # write tag's id or class
    if tag_ids != None:
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
    
    # write attributes or text
    if tag_name == 'p':
      tag_line += '>\n'
      self.html_file.write(tag_line)
      while not self.is_closure(line):
        self.html_file.write(tab + '  ' + line.strip() + '\n')
        line = self.next_line()
    else:
      while self.is_attribute_line(line):
        attr, value = line.split(': ')
        tag_line += ' ' + attr.strip() + '="' + value.strip() + '"'
        line = self.next_line()
      tag_line += '>\n'
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
    tag_line = line.split()
    tag_name = tag_line[0].lower()
    tag_ids = tag_line[1:-1]
    if len(tag_ids) == 0:
      tag_ids = None
    if tag_name in tag_map:
      return tag_map[tag_name], tag_ids
    else:
      return tag_name, tag_ids

  def is_attribute_line(self, line: str):
    return not self.is_tag(line) and not self.is_closure(line) and len(line.split(': ')) == 2

  def is_tag(self, line: str):
    return '{' in line

  def is_closure(self, line: str):
    return line.strip() == '}'

  def skip_line(self):
    self.layout_file.readline()

  def next_line(self):
    line = self.layout_file.readline()
    while len(line.strip()) == 0:
      line = self.layout_file.readline()
    return line

  def write_html_header(self):
    self.html_file.write(
      '<!doctype html>\n' +
      '<html lang="en">\n' +
      '<head>\n' +
      '  <meta charset="utf-8">\n' +
      '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
      '  <link rel="stylesheet" href="' + self.file_name + '.css">\n'
    )
