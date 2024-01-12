import sqlobject
from sqlobject import UnicodeCol, IntCol, ForeignKey
from sqlobject import RelatedJoin, MultipleJoin
from sqlobject import SQLObjectNotFound
from sqlobject.dbconnection import ConnectionHub, connectionForURI

hub = ConnectionHub()

class backendObject(sqlobject.SQLObject):

    _connection = hub

class Functie(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'functie'
        idName = 'IDFunctie'

    naam = UnicodeCol(dbName='Functie', dbEncoding='latin-1')
    lokaal = IntCol(dbName='Lokaal')
    def _get_lokaal(self):
        return bool(self._SO_get_lokaal())

class Regent(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'regent'
        idName = 'IDRegent'

    geslachtsnaam = UnicodeCol(dbName='Geslachtsnaam', dbEncoding='latin-1')
    tussenvoegsel = UnicodeCol(dbName='Tussenvoegsel', dbEncoding='latin-1')
    voornaam = UnicodeCol(dbName='Voornaam', dbEncoding='latin-1')
    adel = IntCol(dbName='Adel')
    adelspredikaat = UnicodeCol(dbName='Adelspredikaat', dbEncoding='latin-1')
    heerlijkheid = UnicodeCol(dbName='Heerlijkheid', dbEncoding='latin-1')
    heerlijkheid2 = UnicodeCol(dbName='Heerlijkheid2', dbEncoding='latin-1')

    geboortejaar = UnicodeCol(dbName='Geboortejaar', dbEncoding='latin-1')
    geboortemaand = UnicodeCol(dbName='geboortemaand', dbEncoding='latin-1')
    geboortedag = UnicodeCol(dbName='geboortedag', dbEncoding='latin-1')
    geboorteplaats = UnicodeCol(dbName='geboorteplaats', dbEncoding='latin-1')

    overlijdensjaar = UnicodeCol(dbName='Overlijdensjaar', dbEncoding='latin-1')
    overlijdensmaand = UnicodeCol(
        dbName='overlijdensmaand', dbEncoding='latin-1'
        )
    overlijdensdag = UnicodeCol(dbName='overlijdensdag', dbEncoding='latin-1')
    overlijdensplaats = UnicodeCol(
        dbName='overlijdensplaats', dbEncoding='latin-1'
        )

    doopjaar = UnicodeCol(dbName='doopjaar', dbEncoding='latin-1')

    aliassen = MultipleJoin('Alias', joinColumn='IDRegent')
    aanstellingen = MultipleJoin('Aanstelling', joinColumn='IDRegent')

    bronnen = MultipleJoin('BronDetails', joinColumn='IDRegent')

    # Hacks to get to adellijketitel and academischetitel just right
    #
    # The values for these columns can either be NULL - which is OK, there's
    # no relation then, or 0.
    # 0 apparently *means* there's no relation as well, but how would we
    # know not to look for a record with id == 0 in the corresponding tables.
    adellijketitel = IntCol(dbName='IDAdellijkeTitel')
    def _get_adellijketitel(self):
        id = self._SO_get_adellijketitel()
        if id is None or id == 0:
            return None
        return AdellijkeTitel.get(id)

    academischetitel = IntCol(dbName='IDAcademischeTitel')
    def _get_academischetitel(self):
        id = self._SO_get_academischetitel()
        if id is None or id == 0:
            return None
        return AcademischeTitel.get(id)

    opmerkingen = UnicodeCol(dbName='Opmerkingen', dbEncoding='latin-1')

class College(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'college'
        idName = 'IDCollege'

    naam = UnicodeCol(dbName='College', dbEncoding='latin-1')
    lokaal = IntCol(dbName='Basis')
    def _get_lokaal(self):
        return bool(self._SO_get_lokaal())

class Aanstelling(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'bovenlokaalcollegeregentdetails'
        idName = 'IDBovenlokaalcollegeregentdetails'

    begindag = UnicodeCol(dbName='Begindag', dbEncoding='latin-1')
    beginmaand = UnicodeCol(dbName='Beginmaand', dbEncoding='latin-1')
    beginjaar = UnicodeCol(dbName='Beginjaar', dbEncoding='latin-1')
    einddag = UnicodeCol(dbName='Einddag', dbEncoding='latin-1')
    eindmaand = UnicodeCol(dbName='Eindmaand', dbEncoding='latin-1')
    eindjaar = UnicodeCol(dbName='Eindjaar', dbEncoding='latin-1')

    functie = IntCol(dbName='IDFunctie', foreignKey='Functie')
    regent = IntCol(dbName='IDRegent', foreignKey='Regent')
    college = IntCol(dbName='IDCollege', foreignKey='College')

    # Fake a proper boolean column
    vertegenwoordigend = IntCol(dbName='Vertegenwoordigend')
    def _get_vertegenwoordigend(self):
        return bool(self._SO_get_vertegenwoordigend())

    # Hacks to get to regio, provincie, lokaal and stand just right
    #
    # The values for these columns can either be NULL - which is OK, there's
    # no relation then, or 0.
    # 0 apparently *means* there's no relation as well, but how would we
    # know not to look for a record with id == 0 in the corresponding tables.
    lokaal = IntCol(dbName='IDLokaal')
    def _get_lokaal(self):
        id = self._SO_get_lokaal()
        if id is None or id == 0:
            return None
        return Lokaal.get(id)

    regio = IntCol(dbName='IDRegio')
    def _get_regio(self):
        id = self._SO_get_regio()
        if id is None or id == 0:
            return None
        return Regio.get(id)

    provincie = IntCol(dbName='IDProvinciaal')
    def _get_provincie(self):
        id = self._SO_get_provincie()
        if id is None or id == 0:
            return None
        return Provincie.get(id)

    stand = IntCol(dbName='IDStand')
    def _get_stand(self):
        id = self._SO_get_stand()
        if id is None or id == 0:
            return None
        return Stand.get(id)

    opmerkingen = UnicodeCol(dbName='Opmerkingen', dbEncoding='latin-1')

class Lokaal(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'lokaal'
        idName = 'IDlokaal'

    naam = UnicodeCol(dbName='lokaal', dbEncoding='latin-1')

class Regio(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'regio'
        idName = 'IDregio'

    naam = UnicodeCol(dbName='regio', dbEncoding='latin-1')

class Provincie(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'provinciaal'
        idName = 'IDProvinciaal'

    naam = UnicodeCol(dbName='provincie', dbEncoding='latin-1')

class Stand(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'stand'
        idName = 'IDstand'

    naam = UnicodeCol(dbName='stand', dbEncoding='latin-1')

class AdellijkeTitel(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'adellijketitel'
        idName = 'IDAdellijkeTitel'

    naam = UnicodeCol(dbName='AdellijkeTitel', dbEncoding='latin-1')

class AcademischeTitel(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'academischetitel'
        idName = 'IDAcademischeTitel'

    naam = UnicodeCol(dbName='AcademischeTitel', dbEncoding='latin-1')

class Alias(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'aliassen'

    naam = UnicodeCol(dbName='alias', dbEncoding='latin-1')
    regent = IntCol(dbName='IDRegent', foreignKey='Regent')

class BronDetails(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'bronregentdetails'
        idName = 'IDBronregentdetails'

    details = UnicodeCol(dbName='deel_en_paginanummer', dbEncoding='latin-1')

    bron = IntCol(dbName='IDBron', foreignKey='Bron')
    regent = IntCol(dbName='IDRegent', foreignKey='Regent')

    @property
    def naam(self):
        return '%s (pagina en deel: %s)' % (self.bron.naam, self.details)

class Bron(backendObject):

    class sqlmeta:
        registry = 'backend'
        table = 'bron'
        idName = 'IDBron'

    naam = UnicodeCol(dbName='bron', dbEncoding='latin-1')

    regenten = RelatedJoin(
        'Regent', joinColumn='IDBron', otherColumn='IDRegent',
        intermediateTable='bronregentdetails')

if __name__ == '__main__':
    url = 'mysql://root@localhost/ra_negentien?debug=True'
    hub.threadConnection = connectionForURI(url)
