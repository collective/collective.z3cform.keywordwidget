from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from unicodedata import normalize
from z3c.form.i18n import MessageFactory as _
from zope.schema import vocabulary
import interfaces
import re
import z3c.form
import zope.component
import zope.interface
import zope.schema


_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:]+')


def slugify(text, delim=u'-'):
    """ ASCII-only slug."""
    result = []
    for word in _punct_re.split(text.lower()):
        word = normalize('NFKD', word).encode('ascii', 'ignore')
        if word:
            result.append(word)
    return unicode(delim.join(result))


class KeywordWidget(z3c.form.browser.select.SelectWidget):

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

    def getValuesFromRequest(self, default=z3c.form.interfaces.NOVALUE):
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

    def extract(self, default=z3c.form.interfaces.NOVALUE):
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
            self.terms = z3c.form.term.Terms()

        context = aq_inner(self.context)
        index = self.field.getName()
        catalog = getToolByName(context, 'portal_catalog')
        values = list(catalog.uniqueValuesFor(index))

        if None in values or '' in values:
            values = [v for v in values if v]

        added_values = self.getValuesFromRequest()
        for v in added_values:
            if v and v not in values:
                values.append(v)

        items = []
        unique_values = []
        for v in values:
            normalized_value = slugify(v)
            if not normalized_value in unique_values:
                unique_values.append(normalized_value)
                items.append(vocabulary.SimpleTerm(normalized_value,
                    title=safe_unicode(v)))

        self.terms.terms = vocabulary.SimpleVocabulary(items)
        return self.terms


@zope.component.adapter(interfaces.IKeywordCollection,
                        z3c.form.interfaces.IFormLayer)
@zope.interface.implementer(z3c.form.interfaces.IFieldWidget)
def KeywordFieldWidget(field, request):
    """ IFieldWidget factory for KeywordWidget
    """
    return z3c.form.widget.FieldWidget(field, KeywordWidget(request))
