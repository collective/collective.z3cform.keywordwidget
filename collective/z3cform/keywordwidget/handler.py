from copy import copy
import plone.supermodel.exportimport
from collective.z3cform.keywordwidget.field import Keywords

# Field import/export handlers
KeywordsHandler = plone.supermodel.exportimport.BaseHandler(Keywords)
KeywordsHandler.fieldAttributes = copy(KeywordsHandler.fieldAttributes)
#KeywordsHandler.filteredAttributes.update({'index_name': 'w'})