import datetime

from sqlobject.converters import registerConverter

# Override default date(time) converters with converters that can handle
# date(time)s before 1900.

def DateTimeConverter(value, db):
    return "'%4d-%02d-%02d %02d:%02d:%02d'" % (
        value.year, value.month, value.day, 
        value.hour, value.minute, value.second)
        
registerConverter(datetime.datetime, DateTimeConverter)

def TimeConverter(value, db):
    return "'%02d:%02d:%02d'" % (value.hour, value.minute, value.second)

registerConverter(datetime.time, TimeConverter)

def DateConverter(value, db):
    return "'%4d-%02d-%02d'" % (value.year, value.month, value.day)
        
registerConverter(datetime.date, DateConverter)
