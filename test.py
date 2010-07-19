import unittest

from xml.etree.ElementTree import tostring

from asciimathml import *

class ParseTestCase(unittest.TestCase):
    def assertTreeEquals(self, a, b):
        self.assertEquals(tostring(a), tostring(b))

    def assertRendersTo(self, asciimathml, xmlstring):
        mathml = parse(asciimathml)
        self.assertEquals(tostring(mathml), '<math><mstyle>%s</mstyle></math>' % xmlstring)

    def testEmpty(self):
        self.assertTreeEquals(parse(''), El('math', El('mstyle')))

    def testNumber(self):
        self.assertTreeEquals(parse('3.1415'), El('math', El('mstyle', El('mn', text='3.1415'))))

    def testSymbol(self):
        self.assertTreeEquals(parse('alpha'), El('math', El('mstyle', El('mi', text=u'\u03b1'))))

    def testSymbols(self):
        self.assertTreeEquals(parse('alpha beta'), El('math', El('mstyle', El('mi', text=u'\u03b1'), El('mi', text=u'\u03b2'))))

    def testFrac(self):
        self.assertTreeEquals(parse('alpha / beta'),
            El('math', El('mstyle',
                El('mfrac',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2')))))

    def testSub(self):
        self.assertTreeEquals(parse('alpha _ beta'),
            El('math', El('mstyle',
                El('msub',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2')))))

    def testSup(self):
        self.assertTreeEquals(parse('alpha ^ beta'),
            El('math', El('mstyle',
                El('msup',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2')))))

    def testSubSup(self):
        self.assertTreeEquals(parse('alpha _ beta ^ gamma'),
            El('math', El('mstyle',
                El('msubsup',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2'),
                    El('mi', text=u'\u03b3')))))

    def testSupSub(self):
        self.assertTreeEquals(parse('alpha ^ beta _ gamma'),
            El('math', El('mstyle',
                El('msubsup',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b3'),
                    El('mi', text=u'\u03b2')))))

    def testUnary(self):
        self.assertTreeEquals(parse('sin alpha'),
            El('math', El('mstyle',
                El('mrow',
                    El('mo', text='sin'),
                    El('mi', text=u'\u03b1')))))

    def testUnary2(self):
        self.assertTreeEquals(parse('dot alpha'),
            El('math', El('mstyle',
                El('mover',
                    El('mo', text='.'),
                    El('mi', text=u'\u03b1')))))

    def testUnary3(self):
        self.assertTreeEquals(parse('sqrt alpha'),
            El('math', El('mstyle',
                El('msqrt',
                    El('mi', text=u'\u03b1')))))

    def testUnary4(self):
        self.assertTreeEquals(parse('text alpha'),
            El('math', El('mstyle',
                El('mtext',
                    El('mi', text=u'\u03b1')))))

    def testBinary(self):
        self.assertTreeEquals(parse('frac alpha beta'),
            El('math', El('mstyle',
                El('mfrac',
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2')))))

    def testUnderOver(self):
        self.assertTreeEquals(parse('sum_alpha^beta'),
            El('math', El('mstyle',
                El('munderover',
                    El('mo', text=u'\u2211'),
                    El('mi', text=u'\u03b1'),
                    El('mi', text=u'\u03b2')))))

    def testParens(self):
        self.assertTreeEquals(parse('(alpha + beta) / gamma'),
            El('math', El('mstyle',
                El('mfrac',
                    El('mrow',
                        El('mi', text=u'\u03b1'),
                        El('mo', text='+'),
                        El('mi', text=u'\u03b2')),
                    El('mi', text=u'\u03b3')))))

    def testUnbalancedParens(self):
        self.assertRendersTo('(alpha + beta / gamma',
            '<mrow><mo>(</mo><mi>&#945;</mi><mo>+</mo><mfrac><mi>&#946;</mi><mi>&#947;</mi></mfrac></mrow>')

if __name__ == '__main__':
    unittest.main()

