from distutils.core import setup
setup(
    name = "asciimathml",
    # packages = ["chardet"],
    version = "0.3.1",
    description = "ASCIIMathML to MathML translator",
    author = "Gabriele Favalessa",
    author_email = "favalex@gmail.com",
    url = "http://github.com/favalex/python-asciimathml",
    # download_url = "http:///python-asciimathml-0.3.1.tgz",
    keywords = ["markup", "math", "xml"],
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
Translate from ASCIIMathML (an easy to type and highly readable way to
represent math formulas) into MathML (a w3c standard directly displayable by
some web browsers).
"""
)
