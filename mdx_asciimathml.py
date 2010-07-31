import re, markdown, random

import asciimathml

class ASCIIMathMLExtension (markdown.Extension):

    def __init__ (self, configs) :
        pass

    def extendMarkdown(self, md, md_globals) :

        self.md = md

        RE = re.compile(r'^(.*)\$\$([^\$]*)\$\$(.*)$', re.M) # $$ a $$

        md.inlinePatterns.add('', ASCIIMathMLPattern(RE), '_begin')

    def reset(self) :
        pass

class ASCIIMathMLPattern (markdown.inlinepatterns.Pattern) :
    def getCompiledRegExp(self):
        return re.compile(r'^(.*)\$\$([^\$]*)\$\$(.*)$', re.M) # $$ a $$

    def handleMatch(self, m) :
        # sup = doc.createElement('sup')
        # a = doc.createElement('a')
        # sup.appendChild(a)
        id = m.group(2).strip()
        # num = self.footnotes.used_footnotes[id]
        # sup.setAttribute('id', self.footnotes.makeFootnoteRefId(num))
        # a.setAttribute('href', '#' + self.footnotes.makeFootnoteId(num))
        # a.appendChild(doc.createTextNode(str(num)))
        # return sup
        # return doc.createTextNode(id)
        return asciimathml.parse(id, markdown.etree.Element, markdown.AtomicString)

def makeExtension(configs=None) :
    return ASCIIMathMLExtension(configs=configs)

