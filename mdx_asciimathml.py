import re, markdown

import asciimathml

class ASCIIMathMLExtension(markdown.Extension):
    def __init__(self, configs):
        pass

    def extendMarkdown(self, md, md_globals):
        self.md = md

        RE = re.compile(r'^(.*)\$\$([^\$]*)\$\$(.*)$', re.M) # $$ a $$

        md.inlinePatterns.add('', ASCIIMathMLPattern(RE), '_begin')

    def reset(self):
        pass

class ASCIIMathMLPattern(markdown.inlinepatterns.Pattern):
    def getCompiledRegExp(self):
        return re.compile(r'^(.*)\$\$([^\$]*)\$\$(.*)$', re.M) # $$ a $$

    def handleMatch(self, m):
        math = asciimathml.parse(m.group(2).strip(), markdown.etree.Element, markdown.AtomicString)
        math.set('xmlns', 'http://www.w3.org/1998/Math/MathML')
        return math

def makeExtension(configs=None):
    return ASCIIMathMLExtension(configs=configs)
