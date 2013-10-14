from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from unicodedata import normalize
from z3c.form.i18n import MessageFactory as _
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary
import interfaces
import re
from z3c.form import interfaces as z3cfinterfaces
from z3c.form.widget import FieldWidget
from z3c.form.browser.select import SelectWidget
from z3c.form.browser.orderedselect import OrderedSelectWidget
from z3c.form.term import Terms
import z3c.form

import zope.component
import zope.interface


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')


def slugify(text, delim=u'-'):
    """ ASCII-only slug."""
    result = []
    for word in _punct_re.split(safe_unicode(text.lower())):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


class KeywordWidget(SelectWidget):

    zope.interface.implementsOnly(interfaces.IKeywordWidget)
    klass = u'keyword-widget'
    multiple = 'multiple'
    size = 14
    style = "width: 100%;"
    noValueToken = u''
    noValueMessage = _('no value')
    promptMessage = _('select a value ...')

    @property
    def formatted_value(self):
        if not self.value:
            return ''
        return '<br/>'.join(self.value)

    def getValuesFromRequest(self, default=z3cfinterfaces.NOVALUE):
        """Get the values from the request and split the terms with newlines
        """
        new_val = []
        old_val = self.request.get(self.name, [])
        for v in self.request.get('%s_additional' % self.name, "").split("\n"):
            clean = v.strip().strip("\r").strip("\n")
            if clean and clean not in old_val:
                new_val.append(clean)
        return old_val + new_val

    def isSelected(self, term):
        return term.title in self.value

    def extract(self, default=z3cfinterfaces.NOVALUE):
        """See z3c.form.interfaces.IWidget.
        """
        if (self.name not in self.request and
            self.name + '_additional' not in self.request and
            self.name + '-empty-marker' in self.request):
            return default

        value = self.getValuesFromRequest() or default
        titles = []
        if value != default:
            for val in value:
                token = slugify(val)
                if token == self.noValueToken:
                    continue

                try:
                    term = self.terms.getTermByToken(token)
                    titles.append(term.title)
                except LookupError:
                    # a new value is entered which is not available in vocab
                    continue

        return len(titles) > 0 and titles or default

    def updateTerms(self):
        if self.terms is None:
            self.terms = Terms()

        context = aq_inner(self.context)
        index = self.field.index_name or self.field.getName()
        catalog = getToolByName(context, 'portal_catalog')
        values = list(catalog.uniqueValuesFor(index))

        if None in values or '' in values:
            values = [v for v in values if v]

        added_values = self.getValuesFromRequest()
        for value in added_values:
            if value and value not in values:
                values.append(value)

        items = []
        unique_values = set()
        for value in values:
            token = slugify(value)
            if token not in unique_values:
                unique_values.add(token)
                items.append(SimpleTerm(value, token, safe_unicode(value)))

        self.terms.terms = SimpleVocabulary(items)
        return self.terms


class InAndOutKeywordWidget(KeywordWidget, OrderedSelectWidget):

    zope.interface.implementsOnly(interfaces.IInAndOutKeywordWidget)
    klass = u'inandoutkeyword-widget'
    multiple = 'multiple'
    size = 14
    style = "width: 100%;"
    noValueToken = u''
    noValueMessage = _('no value')
    promptMessage = _('select a value ...')
    items = []

    def update(self):
        # Do not call OrderedSelectWidget.update, because it would fail on different
        # term policy. Rather call update of OrderedSelectWidget parents manually
        # and copy updated version of OrderedSelectWidget.update here.
        z3c.form.browser.widget.HTMLSelectWidget.update(self)
        z3c.form.widget.SequenceWidget.update(self)
        z3c.form.browser.widget.addFieldClass(self)
        self.items = [
            self.getItem(term, count)
            for count, term in enumerate(self.terms)]
        self.selectedItems = [
            self.getItem(self.terms.getTermByToken(slugify(token)), count)
            for count, token in enumerate(self.value)]
        self.notselectedItems = self.deselect()


@zope.component.adapter(interfaces.IKeywordCollection,
                       z3cfinterfaces.IFormLayer)
@zope.interface.implementer(z3cfinterfaces.IFieldWidget)
def KeywordFieldWidget(field, request):
    """ IFieldWidget factory for KeywordWidget
    """
    return FieldWidget(field, KeywordWidget(request))


@zope.component.adapter(interfaces.IKeywordCollection,
                        z3cfinterfaces.IFormLayer)
@zope.interface.implementer(z3cfinterfaces.IFieldWidget)
def InAndOutKeywordFieldWidget(field, request):
    """ IFieldWidget factory for InAndOutKeywordWidget
    """
    return FieldWidget(field, InAndOutKeywordWidget(request))
