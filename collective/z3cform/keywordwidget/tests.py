import unittest
import doctest
from plone.testing import layered
from plone.app.testing import FunctionalTesting
from .testing import CZ3CFKEYWORDWIDGEL_FUNCTIONAL_TESTING

OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)

TEST_FILES = [
    ('README.txt', CZ3CFKEYWORDWIDGEL_FUNCTIONAL_TESTING),
]

def test_suite():
    return unittest.TestSuite(
        [layered(doctest.DocFileSuite(testfile, optionflags=OPTIONFLAGS),
                 layer=layer)
            for testfile, layer in TEST_FILES]
        )

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
