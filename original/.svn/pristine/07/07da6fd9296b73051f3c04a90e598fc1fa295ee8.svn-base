# -*- coding: utf-8 -*-
import re
from sqlobject import AND, OR, IN, LIKE
from sqlobject.sqlbuilder import Select, LEFTJOINOn
from sqlobject.sqlbuilder import Alias as Alias_

from zope.interface import implements

import interfaces
from model import Persoon, Aanstelling, Functie, Instelling, Alias
from model import Lokaal, Provincie, Regio, AdellijkeTitel, AcademischeTitel

def _escape(string):
    escapes = [
        ("'", "''"),
        ('\\', '\\\\'),
        ('%', '\%'),
        ('_', '\_'),
        ('?', '_'),
        ('*', '%')
        # XXX What about semi-colon?
        ]
    for i, o in escapes:
        string = string.replace(i, o)
    return string

quoted_strings_re = re.compile('\"[^"]+\"')

def _text_search(column, query_string):
    # We hijack some code from
    #    http://dev.inghist.nl/svn/utilities/INGSearch/query_parser.py
    # See also:
    #   http://dev.inghist.nl/trac/wiki/ZoekSimpel
    q = _escape(query_string.lower())
    quoted_parts = [part[1:-1] for part in quoted_strings_re.findall(q)]
    # Remove the quoted parts from the query
    q = quoted_strings_re.sub('', q)
    # Split the remainder, and ignore empty parts
    parts = [p for p in q.split() if p]
    likes = []
    for part in parts:
        if not (part.startswith('%') or part.endswith('%')):
        #if not (part.startswith('%')) :
	    # always wildcards around the part
	    # only not when wildcard was given at front
            part = '%'+part.strip('%')+'%'
        likes.append(LIKE(column, part))
    for part in quoted_parts:
        likes.append(LIKE(column, part))
    return AND(*likes)

class NamedObjectQuery:

    implements(interfaces.IQuery)

    def __init__(self, container):
        self.container = container

    def execute(self, data, orderBy=None):
        if orderBy is not None:
            orderBy = orderBy.encode('utf-8')
        r = self.container.table.select(distinct=True, orderBy=orderBy)
        naam = data.get('naam')
        return r.filter(_text_search(self.container.table.q.naam, naam))

class PersoonQuery:

    implements(interfaces.IQuery)

    def __init__(self, container):
        pass

    def execute(self, data, orderBy='geslachtsnaam'):
        if orderBy is not None:
            orderBy = orderBy.encode('utf-8')
        r = Persoon.select(distinct=True, orderBy=orderBy) # XXX not sure about distinct

        van, tot = data.get('timespan_birth', (None, None))
        if van is not None:
            r = r.filter(Persoon.q.geboortedatum >= van)
        if tot is not None:
            r = r.filter(Persoon.q.geboortedatum <= tot)

        van, tot = data.get('timespan_death', (None, None))
        if van is not None:
            r = r.filter(Persoon.q.overlijdensdatum >= van)
        if tot is not None:
            r = r.filter(Persoon.q.overlijdensdatum <= tot)

        van, tot = data.get('timespan_aanst', (None, None))
        additional_filters = []
        if van is not None:
            additional_filters.append(Aanstelling.q.van >= van)
        if tot is not None:
            additional_filters.append(Aanstelling.q.tot <= tot)

        for col in [
            'voornaam', 'geslachtsnaam', 'searchable_geslachtsnaam',
            'heerlijkheid','opmerkingen'
            ]:
            value = data.get(col)
            if value is None:
                continue
            q = getattr(Persoon.q, col)
            r = r.filter(_text_search(q, value))

        adel = data.get('adel')
        if adel is not None:
            r = r.filter(Persoon.q.adel == adel)

        alias_query = data.get('alias')
        if alias_query:
            aliases = Alias.select().filter(
                _text_search(Alias.q.naam, alias_query))
            if not aliases.count():
                # No aliases found, hence we cannot find any persons by
                # that alias.
                return Persoon.select(Persoon.q.id == None)
            additional_filters.append(
                IN(Persoon.q.id, [a.persoon.id for a in aliases]))

        criteria = [
            'functie', 'instelling', 'lokaal', 'provincie', 'regio', 'stand']
        for criterium in criteria:
            items = data.get(criterium)
            and_query = data.get('%s_and_query'%criterium, False)
            if not items:
                continue
            if and_query:
                for item in items:
                    alias = Alias_(Aanstelling, "aanstelling%s"%item.id)
                    column = getattr(alias.q, '%sID'%criterium)
                    additional_filters.append(AND(
                        Persoon.q.id == alias.q.persoonID, column == item.id))
            else:
                column = getattr(Aanstelling.q, '%sID'%criterium)
                additional_filters.append(
                    IN(column, [i.id for i in items]))

        criteria = ['adellijketitel', 'academischetitel']
        for criterium in criteria:
            items = data.get(criterium)
            if not items:
                continue
            column = getattr(Persoon.q, '%sID'%criterium)
            additional_filters.append(IN(column, [i.id for i in items]))

        if additional_filters:
            r = r.filter(
                # XXX This should be a JOIN I think
                AND(Aanstelling.q.persoonID == Persoon.q.id,
                *additional_filters))

        return r

class AanstellingQuery:

    implements(interfaces.IQuery)

    def __init__(self, container):
        pass

    def execute(self, data, orderBy=None):
        if orderBy is not None:
            orderBy = [o.encode('utf-8') for o in orderBy]
        # Always join with Instelling and Functie to be able to sort on it
        # XXX Shouldn't this use a proper JOIN then?
        # Well, I guess this actually *is* proper join, even if the JOIN
        # syntax itself is not used.
        r = Aanstelling.select(
            AND(
                Functie.q.id == Aanstelling.q.functieID,
                Instelling.q.id == Aanstelling.q.instellingID,
                Persoon.q.id == Aanstelling.q.persoonID,
                ),
            orderBy=orderBy)

        van, tot = data.get('periode', (None, None))
        if van is not None:
            r = r.filter(Aanstelling.q.van >= van)
        if tot is not None:
            r = r.filter(Aanstelling.q.tot <= tot)

        additional_filters = []

        criteria = [
            'functie', 'instelling', 'lokaal', 'provincie', 'regio', 'stand']
        for criterium in criteria:
            items = data.get(criterium)
            and_query = data.get('%s_and_query'%criterium, False)
            if not items:
                continue
            if and_query:
                for item in items:
                    alias = Alias_(Aanstelling, "aanstelling%s"%item.id)
                    column = getattr(alias.q, '%sID'%criterium)
                    additional_filters.append(AND(
                        Persoon.q.id == alias.q.persoonID, column == item.id))
            else:
                column = getattr(Aanstelling.q, '%sID'%criterium)
                additional_filters.append(
                    IN(column, [i.id for i in items]))

        if additional_filters:
            r = r.filter(AND(*additional_filters))

        return r

class NamedQuery:

    implements(interfaces.IQuery)

    _table = None

    def __init__(self, container):
        pass

    def execute(self, data, orderBy=None):
        if orderBy is not None:
            orderBy = orderBy.encode('utf-8')
        r = self._table.select(distinct=True, orderBy=orderBy)
        r = r.filter(self._table.q.lokaal == False)
        naam = data.get('naam')
        if naam:
            r = r.filter(_text_search(self._table.q.naam, naam))
        return r

class FunctieQuery(NamedQuery):
    _table = Functie

class InstellingenQuery(FunctieQuery):
    _table = Instelling
