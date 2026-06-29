import os
import re
import pandas as pd
import numpy as np
from collections import defaultdict, OrderedDict
from sqlalchemy.engine import make_url

from data_definitions import gewest_periods

# MySQL databases that must never receive to_sql writes from the consolidate notebook.
PROTECTED_MYSQL_DATABASES = frozenset({'raa_nw', 'raa_old'})


def mysql_database_name(connection_string: str) -> str:
    name = make_url(connection_string).database
    if not name:
        raise ValueError(f"No database name in connection URL: {connection_string!r}")
    return name


def assert_mysql_write_target(read_url: str, write_url: str, *, protected=None) -> str:
    """Return the write database name or raise if the target is not safe."""
    protected = protected or PROTECTED_MYSQL_DATABASES
    read_db = mysql_database_name(read_url)
    write_db = mysql_database_name(write_url)
    if write_db in protected:
        raise ValueError(
            f"Refusing to write to protected MySQL database {write_db!r}. "
            "Point connection.json raa_out at a new name, e.g. raa_nw_YYYYMMDD."
        )
    if write_db == read_db:
        raise ValueError(
            f"Refusing to write to the same database used for reads ({read_db!r})."
        )
    return write_db


def sup(x):
    result = x[0]
    if x[1] not in [None, '']:
        result = ' en '.join(x)
    return result



def deldupids(joinedtable, val_column, old_id_column):
    """deduplicate a joined table by grouping by values. 
       Note that this does not try to do anything smart with deduplication"""
    idname = f"{val_column}_id"
    tt = joinedtable.groupby(val_column).agg({old_id_column:list}).reset_index()
    tt = tt.reset_index() # this sets new ids to the the grouped index
    tt = tt.rename(columns={'index':idname})
    return tt

def make_idmapping(deduptable, old_id_column, id, is_nested=True):
    """make an id mapping from a deduplicated joined table
    note that there is a difference for tables with and without duplicate previous ('nested') ids"""
    if not id: # hack for tables without previous id
        id = old_id_column
    dtt = deduptable #.to_dict() 
    if is_nested is True:
        revdtt = {x:k for k,v in dtt[[id, old_id_column]].to_records(index=False) for x in v}
    else:
        revdtt = {v:k for k,v in dtt[[id, old_id_column]].to_records(index=False)}
    return revdtt

def alt_idmapping(deduptable, val_column, old_id_column):
    ps = deduptable[[old_id_column,val_column]]
    dtt = ps.to_dict() 
    revdtt = {x:k for k,v in dtt[old_id_column].items() for x in [v]}
    return revdtt

def my_conv(x):
    try:
        return pd.Period(x, freq="D")
    except ValueError:
        pass

def try_padding(possible_int):
    """I stole this from the original code  by Jan Wijbrand"""
    try:
        possible_int = int(possible_int)
        return '%02d'%possible_int
    except (ValueError, TypeError) as e:
        if possible_int.find('?')>-1: #they put a ? in a year!!!!!
            return possible_int
        elif not np.isnan(possible_int):
            return possible_int

def makedate_from_givendate(givendate, start=True):
    """we make a date from any given date using the following rules:
    - make a pandas period from anything with day month year
    - anydate without a year will be turned into either a start or a closing date by filling 
    in month and day: 1-1 for startdate 31-12 for closing date
    - dates with question marks for a final year will get replaced by 9 for closing date and 
    0 for startdate
    """
    #months = {'1':'January','2':'February','3':'March','4':'April','5':'May','6':'June',
    #         '7':'July','8':'August','9':'September','10':'October','11':'November','12':'December'}
    if not givendate or type(givendate) != str:
        return
    year = 1000
    if start==True:
        month = 1
        day = 1
        questionmark = '0'
    else:
        month = 12
        day = 31
        questionmark = '9'
    
    parts = givendate.split('-')
    if len(parts) == 0:
        return

    if len(parts)==3:
        day,month,year = parts
    else:
        year = parts[-1] #I don't think there are dates with only years and months
    year = year.replace('?', questionmark)
    try:
        year = int(year)
    except (TypeError, ValueError):
        #import pdb; pdb.set_trace()
        if year == '':
            return
        
    try:
        month = int(month)
        if int(month) > 12:
            month = 12
    except TypeError:
        pass
    try:
        day = int(day)
    except TypeError:
        if type(month)==int:
            if start:
                day = 1
            else:
                day = 31
    
    try:
        result = pd.Period(year=year, month=month, day=day,freq="D")
    except (ValueError, TypeError):
        #import pdb; pdb.set_trace()
        if month==2 and int(day) == 29:
            corrected_day = int(day) - 1 # out of bounds day for february
        else:
            if start == True:
                corrected_day = 1
            else:
                corrected_day = 28
        result = pd.Period(year=year, month=month, day=corrected_day,freq="D")
    except:
        import pdb; pdb.set_trace()
        print(givendate)
        result = None
        raise
    return result.strftime("%Y-%m-%d")




#test
# but commented out here
# for item in ['02-03-1493',
#             '03-1632',
#             '1721',
#             '143?',
#             '',
#             '22-12-1293',
#             '96-06-1841',
#              '02-28-1650',
#              '29-02-1650',
#              '39-4-1802'
#              '31-02-1734',
#              '31-06-1703',
#              np.nan]:
#     print('begin result: ', makedate_from_givendate(item, start=True))

def get_unique_lower(tbln, joined_tables, uniq_per_table):
    tbl = joined_tables[tbln]
    uniqcolumn = uniq_per_table[tbln]['uniq']
    if pd.api.types.is_numeric_dtype(tbl[uniqcolumn].dtype):
        uniqtitels = pd.DataFrame(list(tbl[uniqcolumn].unique()), columns=[uniqcolumn]).reset_index(drop=True)
    else:
        case_insensitive_column = case_insensitive_unique_list(list(tbl[uniqcolumn].unique()))
        uniqtitels = pd.DataFrame(case_insensitive_column, columns=[uniqcolumn]).reset_index(drop=True)
    # uniqtitels['id'] = uniqtitels.index + 1 # 1 based indexing for sql compatibility
    # if tbln != 'persoon':
    #     clean_references[tbln] = uniqtitels # this is what we need for our final db
    try:
        nwtable = pd.merge(left=uniqtitels.copy(), right=tbl, on=uniqcolumn, suffixes=('', 'nw'))
    except KeyError:
        print(uniqtitels.columns, tbl.columns)
    nwtable = nwtable.reset_index(drop=True)
    nwtable[f'{tbln}_id'] = nwtable.index + 1
    return {'newtable':nwtable}


def case_insensitive_unique_list(data):
    d = OrderedDict()
    for word in data:
        try:
            d.setdefault(word.lower(), word)
        except AttributeError:
            pass
    return d.values()

def load_gewest_tables(connection_string, periods=None) -> pd.DataFrame:
    """Load and concatenate Gewest lookup tables for republiek-period MDBs."""
    from sqlalchemy import create_engine, inspect

    periods = periods or gewest_periods
    engine = create_engine(connection_string)
    table_names = {t.lower(): t for t in inspect(engine).get_table_names()}

    def resolve_table(periode: str) -> str | None:
        for candidate in (f'{periode}_Gewest', f'{periode}_gewest'):
            if candidate.lower() in table_names:
                return table_names[candidate.lower()]
        if periode == 'republiek_friezen':
            for candidate in ('republiek_Gewest', 'republiek_gewest'):
                if candidate.lower() in table_names:
                    return table_names[candidate.lower()]
        return None

    parts = []
    for periode in periods:
        sql_name = resolve_table(periode)
        if sql_name is None:
            print(f'no Gewest table for {periode}, skipping')
            continue
        print(f'getting {sql_name}')
        dftable = pd.read_sql_table(table_name=sql_name, con=engine)
        dftable = dftable.rename(columns={c: c.lower() for c in dftable.columns})
        dftable.reset_index(inplace=True)
        dftable['old_idgewest'] = dftable['idgewest'].astype('Int64').apply(
            lambda x: f'{periode}_{x}'
        )
        parts.append(dftable)
        print(f'adding gewest from {periode}')
    if not parts:
        raise ValueError('No Gewest tables loaded — check raa_old import')
    return pd.concat(parts, ignore_index=True)


def fix_republiek_gewest_provincie(aanstelling: pd.DataFrame) -> pd.DataFrame:
    """Prefer gewest_id over provinciaal_id for republiek-period appointments.

    In republiek MDBs the aanstelling.provinciaal field references Gewest, not
    provinciaal. IDs 11-14 are reused in provinciaal for Southern Netherlands.
    """
    if 'gewest_id' not in aanstelling.columns or 'old_provinciaal' not in aanstelling.columns:
        return aanstelling
    out = aanstelling.copy()
    old_prov = out['old_provinciaal'].astype('string')
    for period in gewest_periods:
        has_gewest = old_prov.str.startswith(f'{period}_', na=False) & out['gewest_id'].notna()
        out.loc[has_gewest, 'provinciaal_id'] = pd.NA
    return out


def replace_ids(worktable=None, wtbln='', reftable=''):
    """replace reference ids in a worktable. We need to pass both worktable itself as its name
    in order to be able to loop this """
    left_on = tblregister[wtbln]['reftables'][reftable]  # join column for worktable
    right_on = uniq_per_table[reftable]['id'] # join column for reftable
    targetcolumn = reftable + '_id'
    rtable = references[reftable][[right_on, reftable + '_id']] # reftable itself
    print(f"updating worktable {wtbln} from {reftable} on {right_on}={left_on}")
    updated = worktable.merge(rtable, how='left', left_on=left_on, right_on=right_on, suffixes=('', '_new')).reset_index(drop=True)
    updated[targetcolumn] = np.where(pd.notnull(updated[targetcolumn]), updated[targetcolumn], None)
    updated.drop([c for c in updated.columns if '_new' in c], axis=1, inplace=True) # reset old table
    origcols = updated.columns
    updated.reset_index(inplace=True, drop=True) # to be sure
    updated = updated[[c for c in origcols]]
    return updated