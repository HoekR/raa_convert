import re

def pandas_match(patlist=[],df=None,field=''):
    t_pat = re.compile(r"(%s)" % r")\b|\b(".join(patlist),  flags=re.I|re.U)
    ps = df[field].str.extract(t_pat)
    molten = ps.melt(ignore_index=False)
    result = molten[molten.value.notna()]
    return result
    
def merge_pat(patlist=[],df=None,field=''):
    molten = pandas_match(patlist=patlist,df=df,field=field)
    result = molten.merge(df, left_on='value', right_on=field)
    return result