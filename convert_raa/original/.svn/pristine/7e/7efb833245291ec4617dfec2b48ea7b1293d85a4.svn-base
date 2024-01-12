import os, os.path
import lxml.etree

import sqlobject
from sqlobject import *
from sqlobject.dbconnection import ConnectionHub, connectionForURI

import frontend

hub = ConnectionHub()

NS = {
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'awml': 'http://www.abisource.com/2004/xhtml-awml/'
    }

def extract_body_content(filename):
    doc = lxml.etree.parse(filename)
    divs = doc.xpath('//xhtml:body/xhtml:div', NS)
    return '\n'.join([lxml.etree.tostring(c) for c in divs])

def feed_toelichting_for_instelling(name, filename):
    r = frontend.Instelling.select(
        LIKE(frontend.Instelling.q.naam, name))
    if not r.count():
        print '#### not found for', name
    for instelling in r:
        instelling.toelichting = extract_body_content(filename)

if __name__ == '__main__':
    import sys, optparse
    version = '1.0'
    usage = ('usage: %prog [options] SOURCE_DIR FRONTEND_DB_URL\n\n')
    parser = optparse.OptionParser(usage=usage, version=version)
    options, urls = parser.parse_args()

    source_dir = urls[0]
    frontend.hub.threadConnection = connectionForURI(urls[1])

    filenames = os.listdir(source_dir)
    for filename in filenames:
        name, ext = os.path.splitext(filename)
        if ext != '.html':
            continue
        feed_toelichting_for_instelling(name, os.path.join(source_dir, filename))
