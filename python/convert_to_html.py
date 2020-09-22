from mappings import tag_map

class ConvertToHTML:
  def __init__(self, folder, layout_file):
    self.layout_file = open(folder + '/' + layout_file, 'r')
    self.html_file = open(folder + '/' + layout_file.split('.')[0] + '.html', 'w')
    self.file_name = layout_file.split('.')[0]
    self.tab_depth = 0

  def convert(self):
    self.parse_root()

  def parse_root(self):

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
      tag_name, tag_id = self.get_tag(line)
      self.parse_tag(tag_name, tag_id)
      line = self.next_line()
    
    # close html
    if self.is_closure(line):
      self.html_file.write('</body>\n</html>\n')

  def parse_tag(self, tag_name, tag_id):

    # write html tag
    self.tab_depth += 1
    tab = '  ' * self.tab_depth
    tag_line = tab + '<' + tag_name
    line = self.next_line()

    # write tags id or class
    if tag_id != None:
      if tag_id[0] == '#':
        tag_line += ' id="' + tag_id[1:] + '"'
      else:
        tag_line += ' class="' + tag_id[1:] + '"'
    
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
      new_tag_name, new_tag_id = self.get_tag(line)
      self.parse_tag(new_tag_name, new_tag_id)
      line = self.next_line()

    # close tag
    if self.is_closure(line):
      self.html_file.write(tab + '</' + tag_name + '>\n')
    self.tab_depth -= 1
      
  def get_tag(self, line):
    tag_line = line.split()
    tag_name = tag_line[0].lower()
    tag_id = tag_line[1]
    if tag_id == '{':
      tag_id = None
    if tag_name in tag_map:
      return tag_map[tag_name], tag_id
    else:
      return tag_name, tag_id

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
      '  <link rel="stylesheet" href="' + self.file_name + '.css">'
    )
