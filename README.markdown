This small python module exports a single function, `parse()`, which parses a
string containing [ASCIIMathML][ASCIIMathML] and returns the corresponding
MathML tree as an [xml.etree.ElementTree][etree] instance.

Also included is a [python-markdown][python-markdown] extension that translates
text enclosed between `$$` into MathML.

[ASCIIMathML]: http://www1.chapman.edu/~jipsen/mathml/asciimath.html
[etree]: http://docs.python.org/library/xml.etree.elementtree.html
[python-markdown]: http://www.freewisdom.org/projects/python-markdown/

## Example usage

The function `parse()` generates a tree of elements:

    >>> import asciimathml
    >>> asciimathml.parse('sqrt 2')
    <Element math at b76fb28c>

The tree can then be manipulated using the standard python library.  For
example we can generate its string representation:

    >>> from xml.etree.ElementTree import tostring
    >>> tostring(asciimathml.parse('sqrt 2'))
    '<math><mstyle><msqrt><mn>2</mn></msqrt></mstyle></math>'

Or, if you want to add the attributes title and xmlns to the root node:

    >>> tree = asciimathml.parse('sqrt 2')
    >>> tree.set('title', 'sqrt2')
    >>> tree.set('xmlns', 'http://www.w3.org/1998/Math/MathML')
    >>> tostring(tree)
    '<math title="sqrt2" xmlns="http://www.w3.org/1998/Math/MathML"><mstyle><msqrt><mn>2</mn></msqrt></mstyle></math>'

As you can see MathML is very verbose and is not intended to be written by hand.

And this is an example of ASCIIMathML embedded in markdown:

    >>> import markdown
    >>> markdown.markdown('$$ sqrt 2 $$', ['asciimathml'])
    u'<p>\n<math xmlns="http://www.w3.org/1998/Math/MathML"><mstyle><msqrt><mn>2</mn></msqrt></mstyle></math>\n</p>'

## Dependencies and installation

Tested with python 2.7.  The core module, `asciimathml` has no dependencies.
The markdown extension `mdx_asciimathml` requires at least markdown 2.0.

A standard `setup.py` is provided (as usual it's enough to execute `python
setup.py install` to perform the installation).  You can also manually copy the
two files `asciimathml.py` and (optionally) `mdx_asciimathml.py` somewhere in
your PYTHONPATH.

## Browser support

The current status of support for MathML by web browsers is disheartening.

As far as I know only firefox and opera, among the major browsers, can properly
render MathML (webkit support is on the way, you can follow progress made
closing the tickets of this master [bug][bug]).

[bug]: https://bugs.webkit.org/show_bug.cgi?id=3251

But please note that MathML is displayed correctly only when embedded in a
XHTML or in HTML5 document.

XHTML must be served with content type 'application/xhtml+xml' (it's not enough
for the document to be valid XHTML).  As you know this will prevent IE (up to
IE8, I haven't tested with IE9) from displaying the page at all.

HTML5 on the other hand is backwards compatible, but is not enabled by default
on the current version of firefox (3.6).  The user must enable it explicitly by
setting to true 'html5' in about:config.
