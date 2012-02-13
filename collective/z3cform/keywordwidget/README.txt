Introduction
============

This product adds a Keyword widget (similar to Archetypes.Widget:KeywordWidget)
for plone.z3cform.


How To Use (Doc Tests):
=======================

    >>> from z3c.form import testing
    >>> testing.setupFormDefaults()

In your interface schema, use the Keywords field as your field type:

    >>> import zope.interface
    >>> import zope.schema
    >>> from zope.schema.fieldproperty import FieldProperty
    >>> from collective.z3cform.keywordwidget.field import Keywords
    >>> class IFoo(zope.interface.Interface):
    ...
    ...     id = zope.schema.TextLine(
    ...         title=u'ID',
    ...         readonly=True,
    ...         required=True
    ...         )
    ...
    ...     keywords = Keywords(
    ...         title=u'Keywords',
    ...         required=True
    ...         )


Let's now create a class that implements our interface.

    >>> from OFS.SimpleItem import SimpleItem
    >>> class Foo(SimpleItem):
    ...     zope.interface.implements(IFoo)
    ...     id = FieldProperty(IFoo['id'])
    ...     keywords = FieldProperty(IFoo['keywords'])
    ...
    ...     def __init__(self, id, keywords):
    ...         super(Foo, self).__init__(id)
    ...         self.id = id
    ...         self.keywords = keywords

For the keywordwidget to work, we need to make sure that the keywords
property is indexed in portal_catalog.

First, we write the indexer. The indexer is a special adapter that adapts the type of an object
and provides the value of the attribute to be indexed.

    >>> from plone.indexer.decorator import indexer
    >>> @indexer(IFoo)
    ... def keywords(obj):
    ...     return IFoo(obj).keywords

We need to register our indexer as a named adapter, where the name corresponds to
the index name. In ZCML, that may be::

    <adapter name="keywords" factory=".indexers.keywords" />

For testing purpoese, we will register it directly.

    >>> from zope.component import provideAdapter
    >>> provideAdapter(keywords, name='keywords')

Now we add a form in which the widget will be rendered:

Specify the KeywordWidget factory ('KeywordFieldWidget') as the field's widgetFactory.

    >>> from z3c.form.testing import TestRequest
    >>> from z3c.form import form, field
    >>> from collective.z3cform.keywordwidget.widget import KeywordFieldWidget

    >>> class FooAddForm(form.AddForm):
    ...
    ...     fields = field.Fields(IFoo)
    ...     fields['keywords'].widgetFactory = KeywordFieldWidget
    ...
    ...     def create(self, data):
    ...         return Foo(**data)
    ...
    ...     def add(self, object):
    ...         self.context[str(object.id)] = object
    ...
    ...     def nextURL(self):
    ...         return 'index.html'


Create an AddForm:

    >>> request = TestRequest()
    >>> addForm = FooAddForm(portal, request)
    >>> addForm.update()

Check for the keyword widget and render it:

    >>> addForm.widgets.keys()
    ['id', 'keywords']

    >>> addForm.widgets['keywords'].render()
    u'<div style="width: 45%; float: left">\n<span> Existing categories </span>\n<br />\n<select id="form-widgets-keywords" name="form.widgets.keywords:list" class="keyword-widget required keywords-field" multiple="multiple" size="14" style="width: 100%;">\n\n</select>\n</div>\n\n<div style="width: 45%; float: right;">\n<span>New categories</span>\n<br />\n<textarea id="form-widgets-keywords" name="form.widgets.keywords_additional" cols="15" rows="13" wrap="off"></textarea>\n</div>\n\n<input name="form.widgets.keywords-empty-marker" type="hidden" value="1" />\n\n<div class="visualClear"><!-- --></div>\n'

Let's now submit the addform with data:

    >>> request = TestRequest(form={
    ...     'form.widgets.id': u'myobject',
    ...     'form.widgets.keywords_additional': u'chocolate\nvanilla\nsüße Nachspeise',
    ...     'form.buttons.add': u'Add'}
    ...     )

    >>> addForm = FooAddForm(portal, request)
    >>> addForm.update()

Check that the object has been created:

    >>> myobject = portal['myobject']
    >>> myobject
    <Foo at /plone/myobject>

Check that the keywords attr has been set:

    >>> myobject.keywords
    [u'chocolate', u'vanilla', u's\xc3\xbc\xc3\x9fe Nachspeise']

Render the widget again and check that the keywords are present and selected:

    >>> addForm.widgets['keywords'].render()
    u'<div style="width: 45%; float: left">\n<span> Existing categories </span>\n<br />\n<select id="form-widgets-keywords" name="form.widgets.keywords:list" class="keyword-widget required keywords-field" multiple="multiple" size="14" style="width: 100%;">\n\n    \n        <option id="form-widgets-keywords-0" value="chocolate" selected="selected">chocolate</option>\n\n        \n    \n    \n        <option id="form-widgets-keywords-1" value="vanilla" selected="selected">vanilla</option>\n\n        \n    \n    \n        <option id="form-widgets-keywords-2" value="sa14ae-nachspeise" selected="selected">s\xc3\xbc\xc3\x9fe Nachspeise</option>\n\n        \n    \n</select>\n</div>\n\n<div style="width: 45%; float: right;">\n<span>New categories</span>\n<br />\n<textarea id="form-widgets-keywords" name="form.widgets.keywords_additional" cols="15" rows="13" wrap="off">chocolate\nvanilla\ns\xc3\xbc\xc3\x9fe Nachspeise</textarea>\n</div>\n\n<input name="form.widgets.keywords-empty-marker" type="hidden" value="1" />\n\n<div class="visualClear"><!-- --></div>\n'

Now add a new category to existing ones

    >>> class FooEditForm(form.EditForm):
    ...
    ...     fields = field.Fields(IFoo)
    ...     fields['keywords'].widgetFactory = KeywordFieldWidget

    >>> request = TestRequest(form={
    ...     'form.widgets.keywords': [u'chocolate', u'vanilla', u's\xc3\xbc\xc3\x9fe Nachspeise'],
    ...     'form.widgets.keywords_additional': u'new category\nzweite Kategorie mit Umlauten äöüß',
    ...     'form.buttons.apply': u'Apply'}
    ...     )

    >>> editForm = FooEditForm(myobject, request)
    >>> editForm.update()

Check if the newly added categories are available

    >>> myobject.keywords
    [u'chocolate', u'vanilla', u's\xc3\xbc\xc3\x9fe Nachspeise', u'new category', u'zweite Kategorie mit Umlauten \xc3\xa4\xc3\xb6\xc3\xbc\xc3\x9f']

Remove some keywords

    >>> request = TestRequest(form={
    ...     'form.widgets.keywords': [u's\xc3\xbc\xc3\x9fe Nachspeise', u'zweite Kategorie mit Umlauten \xc3\xa4\xc3\xb6\xc3\xbc\xc3\x9f'],
    ...     'form.buttons.apply': u'Apply'}
    ...     )

    >>> editForm = FooEditForm(myobject, request)
    >>> editForm.update()

And get the new value
    >>> myobject.keywords
    [u's\xc3\xbc\xc3\x9fe Nachspeise', u'zweite Kategorie mit Umlauten \xc3\xa4\xc3\xb6\xc3\xbc\xc3\x9f']
