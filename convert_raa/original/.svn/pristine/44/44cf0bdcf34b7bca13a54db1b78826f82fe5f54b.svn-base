# -*- coding: utf-8 -*-
from zope.interface import implements, classProvides
from zope.schema.interfaces import IVocabulary, IVocabularyTokenized
from zope.schema.interfaces import ITokenizedTerm, ITitledTokenizedTerm
from zope.schema import Field

import sqlobject
from sqlobject import UnicodeCol, IntCol, DateCol, BoolCol, ForeignKey
from sqlobject import RelatedJoin, MultipleJoin

from sqlos import SQLOS

from interfaces import INamed, ITimePeriod

class TimePeriod(Field):
    __doc__ = ITimePeriod.__doc__
    implements(ITimePeriod)

    def _validate(self, value):
        pass # we keep it simple for now and trust the input widget for
             # this field.

class Object(SQLOS):
    pass

class Aanstelling(Object):

    class sqlmeta:
        defaultOrder = 'van'

    van = DateCol()
    # String that hold the date as it is known (for display)
    van_als_bekend = UnicodeCol()
    tot = DateCol()
    # String that hold the date as it is known (for display)
    tot_als_bekend = UnicodeCol()

    persoon = ForeignKey('Persoon')
    functie = ForeignKey('Functie')
    instelling = ForeignKey('Instelling')
    regio = ForeignKey('Regio')
    provincie = ForeignKey('Provincie')
    lokaal = ForeignKey('Lokaal')
    stand = ForeignKey('Stand')

    vertegenwoordigend = BoolCol()
    opmerkingen = UnicodeCol()

class Persoon(Object):

    class sqlmeta:
        defaultOrder = 'geslachtsnaam'
        table = 'persoon'

    adel = BoolCol()
    heerlijkheid = UnicodeCol()
    voornaam = UnicodeCol()
    tussenvoegsel = UnicodeCol()
    geslachtsnaam = UnicodeCol()

    searchable_geslachtsnaam = UnicodeCol()
 
    onbepaaldgeboortedatum = BoolCol()
    geboortedatum = DateCol()
    # String that hold the date as it is known (for display)
    geboortedatum_als_bekend = UnicodeCol()
    geboorteplaats = UnicodeCol()
    doopjaar = BoolCol()
    onbepaaldoverlijdensdatum = BoolCol()
    overlijdensdatum = DateCol()
    overlijdensplaats = UnicodeCol()
    # String that hold the date as it is known (for display)
    overlijdensdatum_als_bekend = UnicodeCol()

    adellijketitel = ForeignKey('AdellijkeTitel')
    def _get_adellijketitel(self):
        titel = self._SO_get_adellijketitel()
        if titel is None:
            return None
        return titel.naam

    academischetitel = ForeignKey('AcademischeTitel')
    def _get_academischetitel(self):
        titel = self._SO_get_academischetitel()
        if titel is None:
            return None
        return titel.naam

    aanstellingen = MultipleJoin('Aanstelling') #, orderBy='van')
    aliassen = MultipleJoin('Alias')

    functies = RelatedJoin('Functie', intermediateTable='aanstelling')
    instellingen = RelatedJoin('Instelling', intermediateTable='aanstelling')

    bronnen = MultipleJoin('BronDetails')
    opmerkingen = UnicodeCol()

class Named(Object):
    # Baseclass for simple additional tables, that really only
    # expose a unique name.
    # As a consequence of making the naam colunm unique, it can only
    # be max 255 characters long (in MySQL at least).

    implements(INamed)

    class sqlmeta:
        defaultOrder = 'naam'

    naam = UnicodeCol(length=255, unique=True)

class AdellijkeTitel(Named):
    pass

class AcademischeTitel(Named):
    pass

class Provincie(Named):
    pass

class Regio(Named):
    pass

class Lokaal(Named):
    pass

class Stand(Named):
    pass

class Functie(Object):

    implements(INamed)

    class sqlmeta:
        defaultOrder = 'naam'

    naam = UnicodeCol(length=255)
    lokaal = BoolCol()

    instellingen = RelatedJoin('Instelling', intermediateTable='aanstelling')

    @property
    def unique_instellingen(self):
        return set(self.instellingen)

class Instelling(Object):

    implements(INamed)

    class sqlmeta:
        defaultOrder = 'naam'

    naam = UnicodeCol(length=255)
    toelichting = UnicodeCol()
    lokaal = BoolCol()

    functies = RelatedJoin('Functie', intermediateTable='aanstelling')

    @property
    def unique_functies(self):
        return set(self.functies)

class Alias(Object):

    implements(INamed)

    class sqlmeta:
        defaultOrder = 'naam'

    naam = UnicodeCol(length=255)
    persoon = ForeignKey('Persoon')

class BronDetails(Object):

    details = UnicodeCol()

    bron = IntCol(foreignKey='Bron')
    persoon = IntCol(foreignKey='Persoon')

    @property
    def naam(self):
        return self.bron.naam

    @property
    def pagina_en_deel(self):
        return self.details

class Bron(Named):

    personen = RelatedJoin('Persoon', intermediateTable='bron_details')

class NamedTerm(object):

    implements(ITitledTokenizedTerm)

    def __init__(self, obj):
        self.value = obj
        self.title = obj.naam
        self.token = str(obj.id)

class NamedVocabulary(object):

    implements(IVocabularyTokenized)

    def __init__(self, named):
        self.named = named

    def __contains__(self, value):
        return True # since the objects come from this very vocabulary

    def getTerm(self, obj):
        return NamedTerm(obj)

    def getTermByToken(self, token):
        obj = self.named.get(int(token))
        return NamedTerm(obj)

    def __iter__(self):
        return iter([NamedTerm(obj) for obj in self.named.select()])

    def __len__(self):
        return self.named.select().count()


provincien = NamedVocabulary(Provincie)
regios = NamedVocabulary(Regio)
lokalen = NamedVocabulary(Lokaal)
standen = NamedVocabulary(Stand)
academischetitels = NamedVocabulary(AcademischeTitel)
adellijketitels = NamedVocabulary(AdellijkeTitel)

class FunctieVocabulary(NamedVocabulary):

    def __init__(self):
        self.named = Functie

    def __iter__(self):
        results = Functie.select().filter(Functie.q.lokaal == False)
        return iter([NamedTerm(obj) for obj in results])

    def __len__(self):
        return Functie.select().filter(Functie.q.lokaal == False).count()

class InstellingenVocabulary(NamedVocabulary):

    def __init__(self):
        self.named = Instelling

    def __iter__(self):
        results = Instelling.select().filter(Instelling.q.lokaal == False)
        return iter([NamedTerm(obj) for obj in results])

    def __len__(self):
        return Instelling.select().filter(Instelling.q.lokaal == False).count()


instellingen = InstellingenVocabulary()
functies = FunctieVocabulary()
