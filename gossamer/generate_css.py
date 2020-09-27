from mappings import tag_map, css_map
import regex as re
import os


class CSSGenerator:
    def __init__(self, project_dir, component_list):
        self.src_dir = project_dir + '/src/'
        self.build_dir = project_dir + '/build/'
        self.scss_file = open(self.build_dir + 'styles.scss', 'w')
        self.components = component_list

    def convert(self):
        root_file = open(self.src_dir + 'root.styles.gsm', 'r')
        self.parse_file(root_file)
        for component in self.components:
            component_file = open(self.src_dir + '/components/' + component +
                '/' + component + '.styles.gsm', 'r')
            self.parse_file(component_file)
        self.build_scss_file()

    def parse_file(self, file):
        for line in file:
            if len(line.strip()) != 0:
                if '{' in line:
                    line = self.modify_tag(line)
                for key, value in css_map.items():
                    line = line.replace(key, value)
                if '{' not in line and '}' not in line:
                    line = line[:-1] + ';\n'
            self.scss_file.write(line)
        self.scss_file.write('\n')
    
    def build_scss_file(self):
        self.scss_file.close()
        os.system(f'sass ' + self.build_dir + 'styles.scss ' + self.build_dir + 'styles.css')

    def modify_tag(self, line):
        tag_line = re.split(r'(\s+)', line)
        for i in range(len(tag_line)):
            tag_line[i] = tag_line[i].lower()
            if tag_line[i] in tag_map:
                tag_line[i] = tag_map[tag_line[i]]
        return ''.join(tag_line)
