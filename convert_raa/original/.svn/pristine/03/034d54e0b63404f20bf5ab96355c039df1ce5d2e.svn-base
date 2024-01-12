# -*- coding: utf-8 -*-
from Globals import InitializeClass
from OFS.Folder import Folder
from OFS.SimpleItem import SimpleItem
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
# Zope 3
from zope.interface import implements
from zope.app import zapi
from zope.app.component.interfaces import IPossibleSite

from sqlobject import SQLObjectNotFound
from sqlos.interfaces import ISQLObject, IISQLObject, IConnectionName
from sqlos.interfaces.container import ISQLObjectContainer
from Products.Five.site import localsite
from Products.FiveSQLOS.interfaces import IFiveSQLObject
from Products.FiveSQLOS.wrapper import ItemWrapper

from interfaces import IRaa, INamedContainer

class Wrapper(ItemWrapper):
    def getId(self):
        return str(self.context.id)
    id = property(getId)

class Container(SimpleItem):

    implements(ISQLObjectContainer)

    # abstract base class - override id and table_name
    id = None
    table_name = None

    def _table(self):
        return zapi.getUtility(IISQLObject, self.table_name)
    table = property(_table)

    def getId(self):
        return self.id

    def items(self):
        for obj in self.table.select():
            yield (obj.id, Wrapper(obj).__of__(self))

    def __getitem__(self, name):
        if not isinstance(name, basestring):
            raise KeyError, "%s is not a string" % name
        try:
            obj = self.table.get(name)
            return Wrapper(obj).__of__(self)
        except (ValueError, SQLObjectNotFound), e:
            raise KeyError, name

class Personen(Container):
    id = 'personen'
    table_name = 'persoon'

class Aanstellingen(Container):
    id = 'aanstellingen'
    table_name = 'aanstelling'

class Instellingen(Container):

    implements(INamedContainer)

    id = 'instellingen'
    table_name = 'instelling'

class Functies(Container):

    implements(INamedContainer)

    id = 'functies'
    table_name = 'functie'

class Lokaal(Container):

    implements(INamedContainer)

    id = 'lokaal'
    table_name = 'lokaal'

class Provincies(Container):

    implements(INamedContainer)

    id = 'provinvies'
    table_name = 'provincie'

class Regios(Container):

    implements(INamedContainer)

    id = 'regios'
    table_name = 'regio'

# XXX site manager implementation will change when switching to Five 1.5
class Raa(Folder, localsite.FiveSite):

    implements(IRaa, IPossibleSite)

    meta_type = 'RAA Application Object'

    def __init__(self, id, title):
        self.id = id
        self.title = title

    @property
    def personen(self):
        return Personen()

    @property
    def aanstellingen(self):
        return Aanstellingen()

    @property
    def instellingen(self):
        return Instellingen()

    @property
    def functies(self):
        return Functies()

    @property
    def lokaal(self):
        return Lokaal()

    @property
    def provincies(self):
        return Provincies()

    @property
    def regios(self):
        return Regios()

InitializeClass(Raa)

class ConnectionName(SimpleItem):

    implements(IConnectionName)

    def __init__(self, name):
        self.name = name

manage_addRaaForm = PageTemplateFile(
    "www/raaAdd", globals(), __name__='manage_addRaaForm')

def manage_addRaa(context, id, title, REQUEST=None):
    """Add RAA Application object.
    """
    context._setObject(id, Raa(id, title))
    app = getattr(context, id)
    localsite.enableLocalSiteHook(app)
    sm = app.getSiteManager()
    sm.registerUtility(IConnectionName, ConnectionName('raa'))
    REQUEST.RESPONSE.redirect(REQUEST['URL1'] + '/manage_main')
    return ''
