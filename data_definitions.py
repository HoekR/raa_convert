
outdir = "./mdbdump/rawconvert"

# this is a list of all tables per database
# N.B. are there still tables missing????

coll = {' batfra': ['AcademischeTitel',
              'AdellijkeTitel',
              'aliassen',
              'Bron',
              'BronFunctieDetails',
              'BronRegentDetails',
              'College',
              'Data',
              'Functie',
              'FunctieBovenLokaal',
              'FunctieLokaal',
              'lokaal',
              'provinciaal',
              'Regent',
              'regionaal',
              'stand',
              'BovenLokaalCollegeRegentDetails',
              'Gewest'],
        ' negentiende eeuw': ['AcademischeTitel',
              'AdellijkeTitel',
              'aliassen',
              'BovenLokaalCollegeRegentDetails',
              'BronFunctieDetails',
              'BronRegentDetails',
              'College',
              'Data',
              'FunctieLokaal',
              'Gewest',
              'lokaal',
              'provinciaal',
              'regionaal',
              'stand',
              'Bron',
              'Functie',
              'Regent',
              'Temp'],
        ' me': ['AcademischeTitel',
              'AdellijkeTitel',
              'aliassen',
              'BovenLokaalCollegeRegentDetails',
              'BovenLokaalCollegeRegentDetails1',
              'BronFunctieDetails',
              'BronRegentDetails',
              'College',
              'Data',
              'Functie',
              'FunctieLokaal',
              'Gewest',
              'lokaal',
              'regionaal',
              'stand',
              'TempTable',
              'Bron',
              'FunctieBovenLokaal',
              'provinciaal',
              'Regent'],
        ' divperioden': ['AcademischeTitel',
              'AdellijkeTitel',
              'aliassen',
              'BovenLokaalCollegeRegentDetails',
              'Bron',
              'BronFunctieDetails',
              'College',
              'Data',
              'Functie',
              'FunctieBovenLokaal',
              'FunctieLokaal',
              'lokaal',
              'Regent',
              'regionaal',
              'stand',
              'BronRegentDetails',
              'provinciaal'],
        ' republiek': ['AcademischeTitel',
              'AdellijkeTitel',
              'aliassen',
              'BovenLokaalCollegeRegentDetails',
              'Bron',
              'BronRegentDetails',
              'College',
              'Data',
              'Functie',
              'FunctieBovenLokaal',
              'FunctieLokaal',
              'lokaal',
              'provinciaal',
              'Regent',
              'RegentOud',
              'regionaal',
              'BronFunctieDetails',
              'Gewest',
              'stand']}

# common tables are tables that appear in all or at least several databases 
# and that have to be merged
# make common_tables static here

common_tables = ['AcademischeTitel',
 'AdellijkeTitel',
 'aliassen',
 'Bron',
#  'BronFunctieDetails',
 'BronRegentDetails',
 'College',
 'Functie',
 'FunctieBovenLokaal',
 'FunctieLokaal',
 'lokaal',
 'provinciaal',
 'Regent',
 'regionaal',
 'stand',
 'BovenLokaalCollegeRegentDetails',
]




# ids in tables

# ids = {'AcademischeTitel': ['IDAcademischeTitel'],
# 'AdellijkeTitel': ['IDAdellijkeTitel'],
# 'aliassen': ['IDPersoon'],
# 'Bron': ['IDBron'],
# 'BronFunctieDetails': ['IDBron','IDBovenLokaalCollegeRegentDetails'],
# 'BronRegentDetails': ['IDRegent','IDBron'],
# 'College': ['IDCollege','Id'],
# 'Functie': ['IDFunctie','Id'],
# 'FunctieBovenLokaal': ['ID FunctieBovenLokaal'],
# 'FunctieLokaal': ['ID FunctieLokaal'],
# 'lokaal': ['IDlokaal'],
# 'provinciaal': ['IDprovincie'],
# 'Regent': ['IDRegent', 'IDAdellijkeTitel','IDAcademischeTitel'],
# 'regionaal': ['IDregio', 'IDRegio'],
# 'stand': ['IDstand'],
# 'BovenLokaalCollegeRegentDetails': ['ID','IDRegent','IDFunctie','IDCollege',
#         'lokaal', 'provinciaal', 'regio', 'stand',
#        'vertegenwoordigend'],
# 'Gewest': ['IDGewest'],
# 'Data':['ID']}




# because there is too little uniformity between tables, we describe the tables here
# fields: 
# 
# All tables have their owe properties:
# 
#   - id: the new id of the table. All new ids have the form {table_name}_id. and are 
#     created from a mapping of the old ids to a new consolidated version of the table
# 
#   - old_id: the old id of the table.  
#
#   - uniq: the unique content column (if any, 
#     sometimes tables are just relational tables or unique content is in a combination of fields)
# 
#   - reftables is a normative registry of which table refers to which other tables (reftable), 
#     in the following form:
#     - {reftables: refcolumn}} in which 
#     - refcolumn (name is implicit) is the column that is referring from the same oldid-new id mapping
#       (and that should be updated)
#     - all new reference columns are only explicitly named under the table itself, 
#       they have the canonic form "{reference_table}_id"
#   - is_reference: property indicating reference status. Only reference tables are explicitly deduplicated
#     other tables still need to get a new id, even if they are relation tables. If the 'old_id' property is None, 
#     the current index will be used as id (because it does not really matter)
#
# The reference tables are described under their own entry. Because of the myriad of different entries, the reference
# tables are dedeplicated and normalized, but this requires mapping multiple reference ids to new ones
#
# Note that some tables are used as references, but are not reference tables in themselves. 
#
# This is especially the case for the _persoon_ table. This does not require deduplication, but it does require id mapping
#
# 
# the oldids property refers to old ids, but is not used anymore, but we leave them for now


tblregister = {
      'persoon': {'id': 'persoon_id',
        'old_id':'old_idregent',
        'uniq': 'persoon_id',
        'reftables': {'academischetitel': 'old_idacademischetitel',
                      'adellijketitel': 'old_idadellijketitel'},
        'is_reference':False,
        'oldids': ['IDRegent', 'IDAdellijkeTitel', 'IDAcademischeTitel']},
      'aliassen': {'id': 'alias_id',
        'old_id': None, 
        'uniq': 'alias',
        'reftables': {'persoon': 'old_idpersoon'},
        'is_reference':False,
        'oldids': ['IDPersoon']},
      'bronregentdetails': {'id': 'bronrd_id',
        'old_id': None,
        'uniq': 'deel_en_paginanummer',
        'reftables': {'bron': 'old_idbron', 
                      'persoon': 'old_idregent'},
        'is_reference':False,
        'oldids': ['IDRegent', 'IDBron']},
      'aanstelling': {'id': 'aanstelling_id',
        'old_id': None, #'id',                      
        'uniq': 'id',
        'reftables': {'college': 'old_idcollege',
                      'functie': 'old_idfunctie',
                      'lokaal': 'old_lokaal',
                      'provinciaal': 'old_provinciaal',
                      'regionaal': 'old_regio',
                      'stand': 'old_stand',
                      'persoon': 'old_idregent'},
        'is_reference':False,
        'oldids': ['ID',
                  'IDRegent',
                  'IDFunctie',
                  'IDCollege',
                  'lokaal',
                  'provinciaal',
                  'regio',
                  'stand',
                  'vertegenwoordigend']},
      'academischetitel': {'id': 'academischetitel_id',
        'old_id': 'old_idacademischetitel',
        'uniq': 'academischetitel',
        'is_reference': True,
        'oldids': ['IDAcademischeTitel']},
      'adellijketitel': {'id':'adellijketitel_id',
        'old_id': 'old_idadellijketitel',
        'uniq': 'adellijketitel',
        'is_reference': True,
        'oldids': ['IDAdellijkeTitel']},
      'bron': {'id': 'bron_id',
        'old_id': 'old_idbron',
        'uniq': 'bron',
        'is_reference': True,
        'oldids': ['IDBron']},
      'college': {'id':'college_id',
        'old_id': 'old_idcollege',
        'uniq': 'college',
        'is_reference': True,
        'oldids': ['IDCollege', 'Id']},
      'functie': {'id':'functie_id',
        'old_id': 'old_idfunctie',
        'uniq': 'functie',
        'is_reference': True,
        'oldids': ['IDFunctie', 'Id']},
      'functiebovenlokaal': {'id': 'functiebovenlokaal_id',
        'old_id': 'old_id functiebovenlokaal',
        'uniq': 'functiebovenlokaal',
        'is_reference': True,
        'oldids': ['ID FunctieBovenLokaal']},
      'functielokaal': {'id': 'functielokaal_id',
        'old_id': 'old_id functielokaal',
        'uniq': 'functielokaal',
        'is_reference': True,
        'oldids': ['ID FunctieLokaal']},
      'lokaal': {'id': 'lokaal_id',
        'old_id': 'old_idlokaal', 
        'uniq': 'lokaal', 
        'is_reference': True,
        'oldids': ['IDlokaal']},
      'provinciaal': {'id': 'provinciaal_id',
        'old_id': 'old_idprovincie',
        'uniq': 'provincie',
        'is_reference': True,
        'oldids': ['IDprovincie']},
      'regionaal': {'id':'regionaal_id',
        'old_id': 'old_idregio',
        'uniq': 'regio',
        'is_reference': True,
        'oldids': ['IDregio', 'IDRegio']},
      'stand': {'id':'stand_id',
        'old_id': 'old_idstand', 
        'uniq': 'stand', 
        'is_reference': True,
        'oldids': ['IDstand']}
    }
# 'bronfunctiedetails': {'id': 'id_bronfd',
#   'uniq': None,
#   'reftables': {'bron': 'old_idbron',
#   'aanstelling': 'old_idbovenlokaalcollegeregentdetails'},
#   'oldids': ['IDBron', 'IDBovenLokaalCollegeRegentDetails']},
# note: not used as far as I can tell, so commented out



replacements = {'regent':'persoon',
                'bovenlokaalcollegeregentdetails':'aanstelling'}

nids = {k.lower():[x.lower() for x in v.get('oldids') or []] for k,v in tblregister.items()}


# common_helptable = {'academischetitel':'academischetitel',
#  'adellijketitel': 'adellijketitel',
#  'aliassen' :'alias',
#  'bron' : 'bron', 
#  'college' : 'college',
#  'functie': 'functie',
#  'functiebovenlokaal':'functiebovenlokaal',
#  'functielokaal':'functielokaal',
#  'lokaal':'lokaal',
#  'provinciaal':'provincie',
#  'regionaal':'regio',
#  'stand': 'stand',
#  'gewest': 'gewest',
#  'aliassen':'alias'}


# following are columns that are candidates for date mangling

cols = ['geboortejaar','geslachtsnaam', 'heerlijkheid',
       'overlijdensjaar', 'overlijdensmaand',
       'tussenvoegsel','voornaam']

