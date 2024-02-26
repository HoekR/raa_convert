import os
import pandas as pd
import numpy as np
from collections import defaultdict, OrderedDict

def sup(x):
    result = x[0]
    if x[1] not in [None, '']:
        result = ' en '.join(x)
    return result

def deldupids(joinedtable, val_column, old_id_column):
    xtbl = joinedtable.drop_duplicates([val_column])[[val_column] + [old_id_column]].reset_index(drop=True)
    xtbl.reset_index(inplace=True)
    xtbl.rename(columns={'index':f'{val_column}_id'},inplace=True)
    return xtbl

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

def get_unique_lower(tbln, joined_tables, uniq_per_table, clean_references):
    tbl = joined_tables[tbln]
    uniqcolumn = uniq_per_table[tbln]['uniq']
    if pd.api.types.is_numeric_dtype(tbl[uniqcolumn].dtype):
        uniqtitels = pd.DataFrame(list(tbl[uniqcolumn].unique()), columns=[uniqcolumn]).reset_index(drop=True)
    else:
        case_insensitive_column = case_insensitive_unique_list(list(tbl[uniqcolumn].unique()))
        uniqtitels = pd.DataFrame(case_insensitive_column, columns=[uniqcolumn]).reset_index(drop=True)
    uniqtitels['id'] = uniqtitels.index + 1 # 1 based indexing for sql compatibility
    if tbln != 'persoon':
        clean_references[tbln] = uniqtitels # this is what we need for our final db
    try:
        nwtable = pd.merge(left=uniqtitels.copy(), right=tbl, on=uniqcolumn, suffixes=('', 'nw'))
    except KeyError:
        print(uniqtitels.columns, tbl.columns)
    nwtable = nwtable.reset_index(drop=True)
    nwtable[f'{tbln}_id'] = nwtable.id
    return nwtable


def case_insensitive_unique_list(data):
    d = OrderedDict()
    for word in data:
        try:
            d.setdefault(word.lower(), word)
        except AttributeError:
            pass
    return d.values()

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