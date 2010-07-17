import re
from collections import namedtuple

import pdb

from xml.etree.ElementTree import Element, SubElement, tostring

__all__ = ['parse', 'El']

def El(tag, *args, **kwargs):
    text = kwargs.pop('text', '')
    element = Element(tag, attrib=kwargs.get('attrib', {}))
    element.text = text

    for child in args:
        element.append(child)

    return element

number_re = re.compile('\d+(\.\d+)?')

def is_frac(e):
    return e.text == '/'

def is_sub(e):
    return e.text == '_'

def is_sup(e):
    return e.text == '^'

def parse(s):
    ns = []

    while True:
        n, s = parse_(s)
        if not n is None:
            ns.append(n)

        if len(ns) > 2:
            if is_frac(ns[-2]):
                n = El('mfrac', ns[-3], ns[-1])
                ns = ns[:-3]
                ns.append(n)
            elif is_sub(ns[-2]):
                n = El('msub', ns[-3], ns[-1])
                ns = ns[:-3]
                ns.append(n)
            elif is_sup(ns[-2]):
                n = El('msup', ns[-3], ns[-1])
                ns = ns[:-3]
                ns.append(n)

        if s == '':
            return El('math', El('mstyle', *ns))

def parse_(s):
    s = s.strip()

    if s == '':
        return None, ''

    m = number_re.match(s)

    if m:
        return El('mn', text=m.group(0)), s[m.end():]

    for y in symbols:
        if s.startswith(y.input):
            return El(y.tag, text=y.output), s[len(y.input):]

    return El('mi', text=s[0]), s[1:]

Symbol = namedtuple('Symbol', 'input tag output tex type')
CONST = 1

symbols = [
    Symbol(input="alpha",  tag="mi", output=u"\u03B1", tex=None, type=CONST),
]

if __name__ == '__main__':
    import sys
    print tostring(parse(' '.join(sys.argv[1:])))
