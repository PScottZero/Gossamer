import sys
import os
from shutil import copyfile

project_name = sys.argv[1].lower()

os.mkdir(project_name + '/')
os.mkdir(project_name + '/src/')
os.mkdir(project_name + '/src/components')
os.mkdir(project_name + '/assets/')
os.mkdir(project_name + '/assets/icons/')

copyfile('gossamer/icons/favicon.svg', project_name + '/assets/icons/favicon.svg')
copyfile('gossamer/icons/favicon.ico', project_name + '/assets/icons/favicon.ico')

layout = open(project_name + '/src/root.layout.gsm', 'w')
styles = open(project_name + '/src/root.styles.gsm', 'w')

layout.write(
    'Root {\n' +
    '  title: Gossamer Project\n' +
    '  icon: ../assets/icons/favicon.svg\n' + 
    '  alt-icon: ../assets/icons/favicon.ico\n\n' +
    '  Text {\n' +
    '    Welcome to Gossamer v0.1\n' +
    '  }\n' +
    '}\n'
)

styles.write(
    '* {\n' +
    '  border: 0\n' +
    '  margin: 0\n' +
    '  padding: 0\n' +
    '  font-family: Arial, Helvetica, sans-serif\n' +
    '}\n\n' +
    'body {\n' +
    '  width: 100vw\n' +
    '  height: 100vh\n' +
    '}\n'
)

layout.close()
styles.close()
