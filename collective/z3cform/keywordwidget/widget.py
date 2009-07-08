from zope.interface import implementsOnly
from zope.component import adapter
from zope.interface import implementer

from z3c.form.browser import widget
from z3c.form.interfaces import IFormLayer
from z3c.form.interfaces import IFieldWidget
from z3c.form.widget import Widget
from z3c.form.widget import FieldWidget

from interfaces import IKeywordWidget

class KeywordWidget(widget.HTMLTextInputWidget, Widget):
    """ Keyword widget. """
    implementsOnly(IKeywordWidget)


@adapter(IKeywordWidget, IFormLayer)
@implementer(IFieldWidget)
def KeywordFieldWidget(field, request):
   """ IFieldWidget factory for KeywordWidget 
   """
   return FieldWidget(field, KeywordWidget(request))
