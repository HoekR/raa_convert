# sandbox
from sqlobject.dbconnection import ConnectionHub, connectionForURI
from sqlobject.sqlbuilder import *

import frontend, backend

def play():
    pass
    
if __name__ == '__main__':
    frontend.hub.threadConnection = connectionForURI(
        'mysql://root@localhost/raa_web?debug=True')
    backend.hub.threadConnection = connectionForURI(
        'mysql://root@localhost/raa?debug=True')
    play()
