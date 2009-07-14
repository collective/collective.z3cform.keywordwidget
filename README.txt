Introduction
============

This product adds a Keyword widget (similar to Archetypes.Widget:KeywordWidget)
for plone.z3cform.

How To Use:
===========

Use the Keywords schema field (based on zope.schema.List) in
collective.z3cform.KeywordWidget.field.py as the 

    from collective.z3cform.keywordwidget.field import Keywords 
    foo = Keywords(title=_('Foo'),)

Make sure that there is an index with the same name:

    from plone.indexer.decorator import indexer
    @indexer(IMyObject)
    def foo(obj):
        return IMyObject(obj).foo

Register it in zcml:

    <adapter factory=".indexes.foo" name="foo" />
        
Then in your form (based on a z3c.form type), specify the KeywordWidget factory
('KeywordFieldWidget') as the field's widgetFactory.

    from collective.z3cform.keywordwidget.widget import KeywordFieldWidget
    fields['foo'].widgetFactory = KeywordFieldWidget 



