import sqlobject
from sqlobject import UnicodeCol, IntCol, DateCol, BoolCol, ForeignKey
from sqlobject import RelatedJoin, MultipleJoin, SingleJoin
from sqlobject import DatabaseIndex

from sqlobject.dbconnection import ConnectionHub, connectionForURI

import backend

hub = ConnectionHub()

class Object(sqlobject.SQLObject):

    _connection = hub

class Aanstelling(Object):

    van = DateCol()
    # String that hold the date as it is known (for display)
    van_als_bekend = UnicodeCol()
    tot = DateCol()
    # String that hold the date as it is known (for display)
    tot_als_bekend = UnicodeCol()
    persoon = ForeignKey('Persoon')
    functie = ForeignKey('Functie')
    instelling = ForeignKey('Instelling')

    persoonIndex = DatabaseIndex('persoonID')
    functieIndex = DatabaseIndex('functieID')
    instellingIndex = DatabaseIndex('instellingID')

    regio = ForeignKey('Regio')
    provincie = ForeignKey('Provincie')
    lokaal = ForeignKey('Lokaal')
    stand = ForeignKey('Stand')

    vertegenwoordigend = BoolCol()
    opmerkingen = UnicodeCol()

class Persoon(Object):

    adel = BoolCol()
    heerlijkheid = UnicodeCol()
    voornaam = UnicodeCol()
    tussenvoegsel = UnicodeCol()
    geslachtsnaam = UnicodeCol()
    searchable_geslachtsnaam = UnicodeCol()
    geboortedatum = DateCol()
    # String that hold the date as it is known (for display)
    geboortedatum_als_bekend = UnicodeCol()
    geboorteplaats = UnicodeCol()
    doopjaar = BoolCol()
    overlijdensdatum = DateCol()
    # String that hold the date as it is known (for display)
    overlijdensdatum_als_bekend = UnicodeCol()
    overlijdensplaats = UnicodeCol()

    adellijketitel = ForeignKey('AdellijkeTitel')
    academischetitel = ForeignKey('AcademischeTitel')

    aanstellingen = MultipleJoin('Aanstelling')
    aliassen = MultipleJoin('Alias')

    bronnen = MultipleJoin('BronDetails')
    opmerkingen = UnicodeCol()

    functies = RelatedJoin('Functie', intermediateTable='aanstelling')
    instellingen = RelatedJoin('Instelling', intermediateTable='aanstelling')

class NamedObject(Object):
    # Baseclass for simple additional tables, that really only
    # expose a unique name.
    # As a consequence of making the naam colunm unique, it can only
    # be max 255 characters long (in MySQL at least).
    naam = UnicodeCol(length=255, alternateID=True)

class AdellijkeTitel(NamedObject):
    pass

class AcademischeTitel(NamedObject):
    pass

class Provincie(NamedObject):
    pass

class Regio(NamedObject):
    pass

class Lokaal(NamedObject):
    pass

class Stand(NamedObject):
    pass

class Periode(NamedObject):
    pass

class Alias(Object):

    naam = UnicodeCol(length=255)
    persoon = ForeignKey('Persoon')

class Functie(Object):

    naam = UnicodeCol(length=255)
    lokaal = BoolCol(default=False)

    instellingen = RelatedJoin('Instelling', intermediateTable='aanstelling')

    @property
    def unique_instellingen(self):
        return set(self.instellingen)

class Instelling(Object):

    naam = UnicodeCol(length=255)
    toelichting = UnicodeCol()
    lokaal = BoolCol(default=False)

    functies = RelatedJoin('Functie', intermediateTable='aanstelling')

    @property
    def unique_functies(self):
        return set(self.functies)

class BronDetails(Object):

    details = UnicodeCol()

    bron = IntCol(foreignKey='Bron')
    persoon = IntCol(foreignKey='Persoon')

class Bron(NamedObject):
    pass

classes = [
    Periode,
    Aanstelling,
    Persoon,
    Functie,
    Instelling,
    AdellijkeTitel,
    AcademischeTitel,
    Provincie,
    Regio,
    Lokaal,
    Stand,
    Alias,
    BronDetails,
    Bron,
    ]

def createTables():
    for class_ in classes:
        class_.createTable(ifNotExists=True)

def dropTables():
    for class_ in classes:
        class_.dropTable(ifExists=True, dropJoinTables=True)

if __name__ == '__main__':
    url = 'mysql://root@localhost/raa_web2?debug=True'
    hub.threadConnection = connectionForURI(url)
    import sqlobject
    from sqlobject import *
