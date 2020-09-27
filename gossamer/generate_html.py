from mappings import tag_map
import shutil
import os


class HTMLGenerator:
    def __init__(self, project_dir):
        self.src_dir = project_dir + '/src/'
        self.build_dir = project_dir + '/build/'
        if os.path.exists(self.build_dir):
            shutil.rmtree(self.build_dir)
        os.mkdir(self.build_dir)
        self.html_file = open(self.build_dir + 'index.html', 'w')
        self.components = []
        self.tab_depth = 0

    def parse_root(self):
        root_file = open(self.src_dir + 'root.layout.gsm', 'r')
        self.write_html_header()
        root_file.readline()
        curr_line = self.next_line(root_file)

        # write root attributes
        while self.is_attribute(curr_line):
            attr, value = curr_line.split(':')
            if attr.strip() == 'title':
                self.html_file.write('  <title>' + value.strip() + '</title>\n'),
            elif attr.strip() == 'icon':
                self.html_file.write('  <link rel="icon" type="image/svg+xml" href="' + value.strip() + '">\n')
            elif attr.strip() == 'alt-icon':
                self.html_file.write('  <link rel="alternate icon" href="' + value.strip() + '">\n')
            curr_line = self.next_line(root_file)
        self.html_file.write('</head>\n<body>\n')

        # read tags and or components
        while not self.is_closure(curr_line):
            if self.is_component(curr_line):
                self.parse_component(root_file, curr_line)
            elif self.is_tag(curr_line):
                self.parse_tag(root_file, curr_line, {})
            curr_line = self.next_line(root_file)

        # complete html file
        self.html_file.write('</body>\n</html>\n')
        root_file.close()

    def parse_tag(self, file, curr_line, inputs):
        self.tab_depth += 1
        tag_name, id_line = self.get_tag_info(curr_line)
        tag_line = self.get_tab() + '<' + tag_name + id_line

        # get tag attributes
        if self.is_text_tag(tag_name):
            tag_line += '>\n'
            self.html_file.write(tag_line)
            curr_line = self.get_enclosed_text(file, inputs)
        else:
            tag_attr, curr_line = self.get_attributes(file, inputs)
            tag_line += tag_attr + '>\n'
            self.html_file.write(tag_line)

        # read tags and or components
        if not self.is_self_closing(tag_name):
            while not self.is_closure(curr_line):
                if self.is_component(curr_line):
                    self.parse_component(file, curr_line)
                elif self.is_tag(curr_line):
                    self.parse_tag(file, curr_line, inputs)
                curr_line = self.replace_with_inputs(inputs, self.next_line(file))
            self.html_file.write(self.get_tab() + '</' + tag_name + '>\n')

        self.tab_depth -= 1

    def parse_component(self, file, curr_line):
        component_name, component_inputs, curr_line = self.get_component_info(file, curr_line)
        self.components.append(component_name)
        component_file = open(self.src_dir + '/components/' +
            component_name + '/' + component_name + '.layout.gsm', 'r')
        
        component_file.readline()
        curr_line = self.next_line(component_file)

        # read tags and or components
        while not self.is_closure(curr_line):
            if self.is_component(curr_line):
                self.parse_component(component_file, curr_line)
            elif self.is_tag(curr_line):
                self.parse_tag(component_file, curr_line, component_inputs)
            curr_line = self.next_line(component_file)

    def get_component_info(self, file, curr_line):
        component_name = curr_line.split()[1]
        curr_line = self.next_line(file)
        component_inputs = {}
        while self.is_attribute(curr_line):
            input_name, input_value = curr_line.split(':')
            component_inputs[input_name.strip()] = input_value.strip()
            curr_line = self.next_line(file)
        return component_name, component_inputs, curr_line

    def get_tag_info(self, curr_line):
        split_temp = curr_line.split()
        tag_name = split_temp[0].lower()
        tag_ids = split_temp[1:-1]
        id_line = ''
        if len(tag_ids) != 0:
            id_line = self.get_id_and_class_string(tag_ids)
        if tag_name in tag_map:
            tag_name = tag_map[tag_name]
        return tag_name, id_line

    def replace_with_inputs(self, inputs, line):
        for key, value in inputs.items():
            line = line.replace('$' + key, value)
        return line

    def get_id_and_class_string(self, tag_ids):
        class_line = 'class="'
        has_classes = False
        id_line = ''
        for id_or_class in tag_ids:
            if id_or_class[0] == '#':
                id_line += ' id="' + id_or_class[1:] + '"'
            else:
                has_classes = True
                class_line += id_or_class[1:] + ' '
        if has_classes:
            id_line += ' ' + class_line.strip() + '"'
        return id_line

    def get_attributes(self, file, inputs):
        tag_line = ''
        line = line = self.replace_with_inputs(inputs, self.next_line(file))
        while self.is_attribute(line):
            attr, value = line.split(': ')
            tag_line += ' ' + attr.strip() + '="' + value.strip() + '"'
            line = line = self.replace_with_inputs(inputs, self.next_line(file))
        return tag_line, line

    def get_tab(self):
        return '    ' * self.tab_depth

    def get_enclosed_text(self, file, inputs):
        line = self.replace_with_inputs(inputs, self.next_line(file))
        while not self.is_closure(line):
            self.html_file.write(self.get_tab() + '    ' + line.strip() + '\n')
            line = self.replace_with_inputs(inputs, self.next_line(file))
        return line

    def is_self_closing(self, tag_name):
        return tag_name == 'img'

    def is_text_tag(self, tag_name):
        return tag_name == 'p'

    def is_attribute(self, line):
        return not self.is_tag(line) and not self.is_closure(line) and len(line.split(': ')) == 2

    def is_tag(self, line):
        return '{' in line

    def is_component(self, line):
        return 'Component' in line

    def is_closure(self, line):
        return line.strip() == '}'

    def next_line(self, file):
        line = file.readline()
        while len(line.strip()) == 0:
            line = file.readline()
        return line

    def write_html_header(self):
        self.html_file.write(
          '<!doctype html>\n' +
          '<html lang="en">\n' +
          '<head>\n' +
          '  <meta charset="utf-8">\n' +
          '  <meta name="viewport" content="width=device-width, initial-scale=1">\n'
          '  <link rel="stylesheet" href="styles.css">\n'
        )
