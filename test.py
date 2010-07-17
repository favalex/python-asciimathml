import unittest

from xml.etree.ElementTree import tostring

from asciimathml import *

class ParseTestCase(unittest.TestCase):
    def assertTreeEquals(self, a, b):
        self.assertEquals(tostring(a), tostring(b))

    def testEmpty(self):
        self.assertTreeEquals(parse(''), El('math', El('mstyle')))

    def testNumber(self):
        self.assertTreeEquals(parse('3.1415'), El('math', El('mstyle', El('mn', text='3.1415'))))

    def testSymbol(self):
        self.assertTreeEquals(parse('alpha'), El('math', El('mstyle', El('mi', text=u'\u03b1'))))

    def testSymbols(self):
        self.assertTreeEquals(parse('alpha alpha'), El('math', El('mstyle', El('mi', text=u'\u03b1'), El('mi', text=u'\u03b1'))))

    def testFrac(self):
        self.assertTreeEquals(parse('alpha / alpha'),
            El('math', El('mstyle',
                El('mfrac',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b1')))))

    def testSub(self):
        self.assertTreeEquals(parse('alpha _ alpha'),
            El('math', El('mstyle',
                El('msub',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b1')))))

    def testSup(self):
        self.assertTreeEquals(parse('alpha ^ alpha'),
            El('math', El('mstyle',
                El('msup',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b1')))))

if __name__ == '__main__':
    unittest.main()

