# New RAA

This is a conversion of the Repertory of Officeholders from the original MSAccess (mdb) databases. I kept everything in Jupyter notebooks in order to be able to follow and influence the process if necessary. 

N.B. This conversion procedure is a result of *much* trial and error. I have tried to comment on all important steps for better understanding. 
The technical conversion procedure is vulnerable due to the arcane nature of MSAccess databases, but these have been in use since the 2000s.

## steps

The conversion procedure (should) follow these steps:

- update MSAccess databases from their HuC repository
- convert the original databases using [mdb_read.ipynb]
- merge to new database using [raa_table_consolidate.ipynb]

N.B. for connecting to the database use a connection string like
'mysql+pymysql://<user>:<password>@localhost/raa_old'
raa_old will be the mysql database name the tables will be written to

## remarks and additions

- Old references and ids are omitted from the final database
- All tables have now period indications for the web interface in columns 0-5 in which 1 indicated they should be included in the searchinterface (and the results)
- The instelling table is now supplemented with html descriptions and (for the Bataafs-Franse period) with links to the external guide database. These are absolute urls as yet
- the updates to reference tables are overhauled and more complete 