import cStringIO
import requests
import xml.sax

req = requests.get('http://rubyinstaller.org/downloads/archives')
if req.status_code == 200:
    file = cStringIO.StringIO()
    file.write(req.content)
    file.seek(0)
else:
    raise IOError('Cannot connect to RubyInstaller.')


class VersionHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.in_li = False
        self.col = 0
        self.versions = {}
        self.href = ''
        self.version = ''

    def startElement(self, name, attrs):
        if name == 'div':
            if attrs.get('class') == 'span-6 border':
                self.col += 1

        if self.col == 2:
            if name == 'li':
                if attrs.get('class') == 'sevenz':
                    self.in_li = True
            if self.in_li:
                if name == 'a':
                    self.href = attrs.get('href')

    def endElement(self, name):
        if self.col == 2:
            if self.in_li == True:
                if name == 'a':
                    self.versions[self.version] = self.href
                    self.version = ''
                    self.href = ''
            if name == 'li':
                self.in_li = False


    def characters(self, content):
        if self.col == 2:
            if self.in_li:
                self.version = content


parser = xml.sax.make_parser()
handler = VersionHandler()
parser.setContentHandler(handler)
parser.parse(file)

print(handler.versions)

version = 'Ruby 2.2.2'
href = handler.versions[version]
req = requests.get(href)

if req.status_code == 200:
    import re

    filename = 'dist/{0}.7z'.format(re.sub('[ \.]', '', version).lower())

    open(filename, 'wb').write(req.content)