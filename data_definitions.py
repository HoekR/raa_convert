
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
 'BronFunctieDetails',
 'BronRegentDetails',
 'College',
#  'Data',
 'Functie',
 'FunctieBovenLokaal',
 'FunctieLokaal',
 'lokaal',
 'provinciaal',
 'Regent',
 'regionaal',
 'stand',
 'BovenLokaalCollegeRegentDetails',
 'Gewest']




# ids in tables

ids = {'AcademischeTitel': ['IDAcademischeTitel'],
'AdellijkeTitel': ['IDAdellijkeTitel'],
'aliassen': ['IDPersoon'],
'Bron': ['IDBron'],
'BronFunctieDetails': ['IDBron','IDBovenLokaalCollegeRegentDetails'],
'BronRegentDetails': ['IDRegent','IDBron'],
'College': ['IDCollege','Id'],
'Functie': ['IDFunctie','Id'],
'FunctieBovenLokaal': ['ID FunctieBovenLokaal'],
'FunctieLokaal': ['ID FunctieLokaal'],
'lokaal': ['IDlokaal'],
'provinciaal': ['IDprovincie'],
'Regent': ['IDRegent', 'IDAdellijkeTitel','IDAcademischeTitel'],
'regionaal': ['IDregio', 'IDRegio'],
'stand': ['IDstand'],
'BovenLokaalCollegeRegentDetails': ['ID','IDRegent','IDFunctie','IDCollege',
        'lokaal', 'provinciaal', 'regio', 'stand',
       'vertegenwoordigend'],
'Gewest': ['IDGewest'],
'Data':['ID']}

nids = {k.lower():[x.lower() for x in v] for k,v in ids.items()}


# in addition to the id columns we also need the name of the content tables

content_cols = {'academischetitel':'academischetitel',
 'adellijketitel': 'adellijketitel',
 'aliassen' :'alias',
 'bron' : 'bron', 
 'college' : 'college',
 'functie': 'functie',
 'functiebovenlokaal':'functiebovenlokaal',
 'functielokaal':'functielokaal',
 'lokaal':'lokaal',
 'provinciaal':'provincie',
 'regionaal':'regio',
 'stand': 'stand',
 'gewest': 'gewest',
 'aliassen':'alias'}

#but we also need to know which column contains the unique values
# and what the name is of the old id 
uniq_per_table = {
'academischetitel':{'uniq':'academischetitel','id':'old_idacademischetitel'},
'adellijketitel': {'uniq':'adellijketitel', 'id':'old_idadellijketitel'},
'bron':{'uniq':'bron','id':'old_idbron'},
'college':{'uniq':'college','id':'old_idcollege'},
'aanstelling':{'uniq':'id','id':'old_id'},
'functie':{'uniq':'functie','id':'old_idfunctie'},
'functiebovenlokaal':{'uniq':'functiebovenlokaal','id':'old_id functiebovenlokaal'}, 
'functielokaal': {'uniq':'functielokaal','id':'old_id functielokaal'},
'lokaal': {'uniq':'lokaal','id':'old_idlokaal'},
'gewest':{'uniq':'gewest','id':'old_idgewest'},
'persoon':{'uniq':'persoon_id','id':'old_idregent'},
'provinciaal':{'uniq':'provincie','id':'old_idprovincie'},
'regionaal':{'uniq':'regio','id':'old_idregio'},
'stand':{'uniq':'stand','id':'old_idstand'}
}

# because there is too little uniformity between tables, we adapt the reversed table to a 
# normative registry of which table refers to which other tables (reftable), in the following form
# table: {reftables: refcolumn}} in which refcolumn is the column that is referring
# (and that should be updated)
tblregister = {'persoon': 
               {'reftables':
                    {'academischetitel':'old_idacademischetitel',
                     'adellijketitel':'old_idadellijketitel'}
                },
             'aliassen': 
                {'reftables':
                    {'persoon':'old_idpersoon'}
                },
              'bronfunctiedetails':
               {'reftables':
                   {'bron':'old_idbron',
                    'aanstelling':'old_idbovenlokaalcollegeregentdetails'}
               },
             'bronregentdetails': 
                {'reftables':
                    {'bron':'old_idbron',
                    'persoon':'old_idregent'}
                },
             'aanstelling': 
               {'reftables':
                    {'college':'old_idcollege',
                    'functie':'old_idfunctie',
                    'lokaal':'old_lokaal',
                    'provinciaal':'old_provinciaal',
                    'regionaal':'old_regio',
                    'stand':'old_stand',
                    'persoon':'old_idregent',}
               }
              }


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

