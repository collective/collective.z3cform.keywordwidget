from plone.testing.z2 import ZSERVER_FIXTURE
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.configuration import xmlconfig


class CZ3CFKeywordwidgetLayer(PloneSandboxLayer):
    defaultBases = (PLONE_FIXTURE,)


    def setUpZope(self, app, configurationContext):
        # prepare z3cforms
        from z3c.form import testing
        testing.setupFormDefaults()

        # load ZCML
        import collective.z3cform.keywordwidget
        xmlconfig.file('configure.zcml', collective.z3cform.keywordwidget,
                        context=configurationContext)

    def setUpPloneSite(self, portal):
        # install into the Plone site
        applyProfile(portal, 'collective.z3cform.keywordwidget:testing')
        setRoles(portal, TEST_USER_ID, ['Manager'])


CZ3CFKEYWORDWIDGET_FIXTURE = CZ3CFKeywordwidgetLayer()

CZ3CFKEYWORDWIDGE_INTEGRATION_TESTING = IntegrationTesting(\
    bases=(CZ3CFKEYWORDWIDGET_FIXTURE,), \
    name="collective.z3cform.keywordwidget:Integration")

CZ3CFKEYWORDWIDGEL_FUNCTIONAL_TESTING = FunctionalTesting(\
    bases=(CZ3CFKEYWORDWIDGET_FIXTURE,), \
    name="collective.z3cform.keywordwidget:Functional")

CZ3CFKEYWORDWIDGEL_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(CZ3CFKEYWORDWIDGET_FIXTURE, ZSERVER_FIXTURE),
    name="collective.z3cform.keywordwidget:Acceptance")
