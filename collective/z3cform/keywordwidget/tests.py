from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite
from Testing import ZopeTestCase as ztc
from zope.app.testing import setup
import Products.CMFPlone
import collective.z3cform.keywordwidget
import doctest
import unittest
import zope.component
import zope.testing
# For loading zcml


ptc.setupPloneSite(
    extension_profiles=['collective.z3cform.keywordwidget:testing'], )


OPTIONFLAGS = (doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE |
               doctest.REPORT_NDIFF |
               doctest.REPORT_ONLY_FIRST_FAILURE)


def test_suite():
    return unittest.TestSuite((
        ztc.FunctionalDocFileSuite(
            'README.txt',
            package='collective.z3cform.keywordwidget',
            test_class=ptc.PloneTestCase,
            optionflags=OPTIONFLAGS),
        ))

