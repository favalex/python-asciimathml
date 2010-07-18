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
        n, s, i = parse_(s)
        if not n is None:
            ns.append(n)

        if len(ns) > 2:
            if is_frac(ns[-2]):
                n = El('mfrac', ns[-3], ns[-1])
                ns = ns[:-3]
                ns.append(n)
            elif is_sub(ns[-2]):
                # TODO use under over if ns[-3] requires it
                if ns[-3].tag == 'msup':
                    children = ns[-3].getchildren()
                    n = El('msubsup', children[0], ns[-1], children[1])
                else:
                    n = El('msub', ns[-3], ns[-1])
                ns = ns[:-3]
                ns.append(n)
            elif is_sup(ns[-2]):
                # TODO use under over if ns[-3] requires it
                if ns[-3].tag == 'msub':
                    children = ns[-3].getchildren()
                    n = El('msubsup', children[0], children[1], ns[-1])
                else:
                    n = El('msup', ns[-3], ns[-1])
                ns = ns[:-3]
                ns.append(n)

        if i.type == BINARY:
            a, s, i = parse_(s)
            b, s, i = parse_(s)
            n = ns[-1]
            ns[-1] = El(n.tag, a, b)
        elif i.type == UNARY:
            a, s, ai = parse_(s)
            n = ns[-1]
            if n.text is None:
                ns[-1] = El(n.tag, a)
            else:
                # mo is hardcoded. Good enough?
                ns[-1] = El(n.tag, El('mo', text=n.text), a)

        if s == '':
            # return El('math', El('mstyle', *ns, attrib={"displaystyle": "true"}), attrib={"xmlns": "http://www.w3.org/1998/Math/MathML"})
            return El('math', El('mstyle', *ns))

def parse_(s):
    s = s.strip()

    if s == '':
        return None, '', SymbolInfo(type=CONST)

    m = number_re.match(s)

    if m:
        return El('mn', text=m.group(0)), s[m.end():], SymbolInfo(type=CONST)

    for y in symbols:
        if s.startswith(y.input):
            return El(y.tag, text=y.output), s[len(y.input):], SymbolInfo(type=y.type)

    return El('mi', text=s[0]), s[1:], SymbolInfo(type=CONST)

Symbol = namedtuple('Symbol', 'input tag output type')
# TODO arity=0,1,2
# TODO subsup=SUBSUP,UNDEROVER

SymbolInfo = namedtuple('SymbolInfo', 'type')
# TODO private element attribs '_type'

CONST = 1; BINARY = 2; UNARY = 3

symbols = [
    Symbol(input="alpha",  tag="mi", output=u"\u03B1", type=CONST),
    Symbol(input="beta",  tag="mi", output=u"\u03B2", type=CONST),
    Symbol(input="gamma",  tag="mi", output=u"\u03B3", type=CONST),

    Symbol(input="*",  tag="mo", output="\u22C5", type=CONST),
    Symbol(input="**", tag="mo", output="\u22C6", type=CONST),

    Symbol(input="sum", tag="mo", output="\u2211", type=CONST), # type=UNDEROVER),

    Symbol(input="sin", tag="mrow", output="sin", type=UNARY), # TODO output=El('mo', text='sin')
    Symbol(input="dot", tag="mover", output=".", type=UNARY),
    Symbol(input="sqrt", tag="msqrt", output=None, type=UNARY),
    Symbol(input="text", tag="mtext", output=None, type=UNARY),

    Symbol(input="frac", tag="mfrac", output=None, type=BINARY),
    Symbol(input="root", tag="mroot", output=None, type=BINARY),
    Symbol(input="stackrel", tag="mover", output=None, type=BINARY),
]

if __name__ == '__main__':
    import sys
    print """\
<?xml version="1.0"?>
<html xmlns="http://www.w3.org/1999/xhtml">
    <head>
        <meta http-equiv="Content-Type" content="application/xhtml+xml" />
        <title>ASCIIMathML preview</title>
    </head>
    <body>
"""
    print tostring(parse(' '.join(sys.argv[1:])))
    print """\
    </body>
</html>
"""
