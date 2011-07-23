# Copyright (c) 2010-2011, Gabriele Favalessa
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from distutils.core import setup
setup(
    name = "asciimathml",
    py_modules = ["asciimathml", "mdx_asciimathml"],
    version = "0.9.3",
    description = "ASCIIMathML to MathML translator",
    author = "Gabriele Favalessa",
    author_email = "favalex@gmail.com",
    url = "http://github.com/favalex/python-asciimathml",
    keywords = ["markup", "math", "mathml", "xml", "markdown"],
    classifiers = [
        "Programming Language :: Python",
        "Development Status :: 4 - Beta",
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
