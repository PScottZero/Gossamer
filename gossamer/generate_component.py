import sys
import os

root = sys.argv[1]
name = sys.argv[2].lower()

os.mkdir(root + '/src/components/' + name + '/')

layout = open(root + '/src/components/' + name + '/' + name + '.layout.gsm', 'w')
styles = open(root + '/src/components/' + name + '/' + name + '.styles.gsm', 'w')

layout.write(
    'Component {\n' +
    '  Text {\n' +
    '    ' + name.capitalize() + ' component works!\n'
    '  }\n' +
    '}\n'
)

layout.close()
styles.close()
