import xml


class Handler(xml.sax.handler.ContentHandler):
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

    def get_parser(self):
        parser = xml.sax.make_parser()
        parser.setContentHandler(self)

        return parser
