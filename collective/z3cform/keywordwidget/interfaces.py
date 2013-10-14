import zope.schema
import z3c.form.interfaces

class IKeywordWidget(z3c.form.interfaces.ISequenceWidget):
    """A keyword widget.
    """

class IInAndOutKeywordWidget(z3c.form.interfaces.IOrderedSelectWidget):
    """An In-out keyword widget.
    """

class IKeywordCollection(zope.schema.interfaces.ICollection):
    """ Marker interfaces for keyword collections
    """

    index_name = zope.schema.TextLine(title=u"Index name",
                                      description=u"Name of the catalog index "
                                                  u"for the values of this field")