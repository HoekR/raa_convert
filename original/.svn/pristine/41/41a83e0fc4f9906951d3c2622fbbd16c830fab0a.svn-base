from datetime import date, timedelta

import sqlobject
from sqlobject.dbconnection import ConnectionHub, connectionForURI

import backend
from feedfrontend import stringToDate

hub = ConnectionHub()

def dates_for_regent(r):
    d1 = d2 = None
    try:
        d1 = stringToDate(r.geboortejaar, r.geboortemaand, r.geboortedag)
    except ValueError, e:
        print 'geboortedatum:', e
    try:
        d2 = stringToDate(r.overlijdensjaar, r.overlijdensmaand, r.overlijdensdag)
    except ValueError, e:
        print 'overlijdensdatum:', e
    return d1, d2

def dates_for_aanstelling(r):
    d1 = d2 = None
    try:
        d1 = stringToDate(r.beginjaar, r.beginmaand, r.begindag)
    except ValueError, e:
        print 'begin:', e
    try:
        d2 = stringToDate(r.eindjaar, r.eindmaand, r.einddag)
    except ValueError, e:
        print 'eind:', e
    return d1, d2

def checkdates():
    for record in backend.Regent.select():
        dates = dates_for_regent(record)
    for record in backend.Aanstelling.select():
        dates = dates_for_aanstelling(record)

if __name__ == '__main__':
    import sys, optparse
    version = '1.0'
    usage = ('usage: %prog [options] SOURCE_DB_URL\n\n')
    parser = optparse.OptionParser(usage=usage, version=version)
    options, urls = parser.parse_args()

    backend.hub.threadConnection = connectionForURI(urls[0])
    checkdates()
