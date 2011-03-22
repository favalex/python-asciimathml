from distutils.core import setup
setup(
    name = "asciimathml",
    py_modules = ["asciimathml", "mdx_asciimathml"],
    version = "0.9.2",
    description = "ASCIIMathML to MathML translator",
    author = "Gabriele Favalessa",
    author_email = "favalex@gmail.com",
    url = "http://github.com/favalex/python-asciimathml",
    # download_url = "http:///python-asciimathml-0.9.1.tgz",
    keywords = ["markup", "math", "mathml", "xml", "markdown"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 3 - Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: XML"
        ],
    long_description = """\
Translates from ASCIIMathML (an easy to type and highly readable way to
represent math formulas) into MathML (a w3c standard directly displayable by
some web browsers).

The MathML tree is represented by Elements from the standard
xml.etree.ElementTree python library.

The obtained tree can then be further manipulated and then serialized into a
string to be included for example in a HTML document.

Also included is a markdown extension that allows the use of ASCIIMathML,
eclosed between $$, inside markdown documents.
"""
)
