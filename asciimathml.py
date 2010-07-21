import re
from collections import namedtuple

import pdb

from xml.etree.ElementTree import Element, SubElement, tostring

__all__ = ['parse', 'El', 'remove_private']

def El(tag, *args, **kwargs):
    text = kwargs.pop('text', '')
    element = Element(tag, attrib=kwargs.get('attrib', {}))
    element.text = text

    for child in args:
        child.set('_parent', element)
        element.append(child)

    return element

number_re = re.compile('\d+(\.\d+)?')

def is_frac(e):
    return e.text == '/'

def is_sub(e):
    return e.text == '_'

def is_sup(e):
    return e.text == '^'

def strip_parens(n):
    if n.tag == 'mrow':
        ns = n.getchildren()

        if ns[0].get('_opening', False):
            n.remove(ns[0])

        if ns[-1].get('_closing', False):
            n.remove(ns[-1])

    return n

def frac(num, den):
    return El('mfrac', strip_parens(num), strip_parens(den))

def parse(s):
    root = El('math', El('mstyle'))

    parse__(s, root[0])

    remove_private(root)
    return root

def parse__(s, ns):
    while True:
        s = parse_(s, ns.append)

        if len(ns) > 0:
            n = ns[-1]

            if n.get('_closing', False):
                ns = ns.get('_parent')

            if n.get('_opening', False):
                ns[-1] = El('mrow', n, attrib={'_parent': ns})
                ns = ns[-1]

            if len(ns) > 2:
                if is_frac(ns[-2]):
                    ns[-3:] = [frac(ns[-3], ns[-1])]
                elif is_sub(ns[-2]):
                    if ns[-3].tag in ('msup', 'mover'):
                        children = ns[-3].getchildren()
                        n = El('msubsup' if ns[-3].tag == 'msup' else 'munderover', children[0], ns[-1], children[1])
                    else:
                        n = El('munder' if ns[-3].get('_underover', False) else 'msub', ns[-3], ns[-1])
                    ns[-3:] = [n]
                elif is_sup(ns[-2]):
                    if ns[-3].tag in ('msub', 'munder'):
                        children = ns[-3].getchildren()
                        n = El('msubsup' if ns[-3].tag == 'msub' else 'munderover', children[0], children[1], ns[-1])
                    else:
                        n = El('mover' if ns[-3].get('_underover', False) else 'msup', ns[-3], ns[-1])
                    ns[-3:] = [n]

            arity = n.get('_arity', 0) if not n is None else None

            if arity == 2:
                n = ns[-1]

                s = parse_(s, n.append, True)
                s = parse_(s, n.append, True)
            elif arity == 1:
                n = ns[-1]

                s = parse_(s, n.append, True)

        if s == '':
            # return El('math', El('mstyle', *ns, attrib={"displaystyle": "true"}), attrib={"xmlns": "http://www.w3.org/1998/Math/MathML"})
            for n in ns:
                remove_private(n)

            return

def remove_private(n):
    # FIXME maybe it's better to store private attributes in another place
    # (e.g. n._mathml_XXX)

    _ks = [k for k in n.keys() if k.startswith('_')]

    for _k in _ks:
        del n.attrib[_k]

    for c in n.getchildren():
        remove_private(c)

    return n

def copy(n):
    m = El(tag=n.tag, attrib=n.attrib, text=n.text)

    for c in n.getchildren():
        m.append(copy(c))

    return m

def parse_(s, append, required=False):
    s = s.strip()

    if s == '':
        if required:
            append(El('mi', text='bla'))
        return ''

    m = number_re.match(s)

    if m:
        append(El('mn', text=m.group(0)))
        return s[m.end():]

    for y in symbols:
        if s.startswith(y.input):
            append(y.el)
            return s[len(y.input):]

    append(El('mi' if s[0].isalpha() else 'mo', text=s[0]))
    return s[1:]

Symbol = namedtuple('Symbol', 'input el')

symbols = [
    Symbol(input="alpha",  el=El("mi", text=u"\u03B1")),
    Symbol(input="beta",  el=El("mi", text=u"\u03B2")),
    Symbol(input="gamma",  el=El("mi", text=u"\u03B3")),

    Symbol(input="*",  el=El("mo", text=u"\u22C5")),
    Symbol(input="**", el=El("mo", text=u"\u22C6")),

    Symbol(input="(",  el=El("mo", text="(", attrib={'_opening': True})),
    Symbol(input=")",  el=El("mo", text=")", attrib={'_closing': True})),

    Symbol(input="sum", el=El("mo", text=u"\u2211", attrib={'_underover':True})),

    Symbol(input="sin", el=El("mrow", El("mo", text="sin"), attrib={'_arity':1})),
    Symbol(input="dot", el=El("mover", El("mo", text="."), attrib={'_arity':1})),
    Symbol(input="sqrt", el=El("msqrt", attrib={'_arity':1})),
    Symbol(input="text", el=El("mtext", attrib={'_arity':1})),

    Symbol(input="frac", el=El("mfrac", attrib={'_arity':2})),
    Symbol(input="root", el=El("mroot", attrib={'_arity':2})),
    Symbol(input="stackrel", el=El("mover", attrib={'_arity':2})),
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
