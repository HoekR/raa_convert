# -*- coding: utf-8 -*-
# Monkey patches...

def execute(self, operation, parameters=None):
    """Executes an operation, registering the underlying
    connection with the transaction system.
    """
    if isinstance(operation, unicode):
        operation = operation.encode('UTF-8')
    self.connection.registerForTxn()
    if parameters is None:
        return self.cursor.execute(operation)
    return self.cursor.execute(operation, parameters)

from zope.app.rdb import ZopeCursor
ZopeCursor.execute = execute

def getEncoding(self):
   return 'utf8'

from mysqldbda.adapter import MySQLdbAdapter
MySQLdbAdapter.getEncoding = getEncoding
MySQLdbAdapter.encoding = getEncoding

def isConnected(self):
    """ XXX Quick hack to see if we can resolve the disappearing connection
    problem. For the RAA application we're reasonably safe here since
    we use the database for reading only.

    See for more info:

      http://mail.zope.org/pipermail/zope3-dev/2005-December/017152.html
   """
    try:
        self._v_connection.ping()
    except:
        # not connected or ping did not restore MySQL connection
        if self._v_connection is not None:
            self._v_connection.close()
            self._v_connection = None
        return False
    return True

MySQLdbAdapter.isConnected = isConnected

from sqlos.adapter import MySQLAdapter
MySQLAdapter.encoding = 'utf-8'
MySQLAdapter.need_unicode = True

# next patch shows more information on UnicodeDecodeError in trace
from StringIO import StringIO 
def getvalue(self):
    if self.buflist:
         try:
              self.buf += ''.join(self.buflist)
         except UnicodeDecodeError:
             # decorate zope traceback with reason for unicode error
             __traceback_info__ = self.pt_parts()
             raise
         self.buflist = []
    return self.buf
def pt_parts(self):
    sl = ['unicode and 8-bit string parts of above page template']
    for x in self.buflist:
        if type(x) == type(''):
            maxcode = 0
            for c in x:
                maxcode = max(ord(c), maxcode)
        # show only unicode objects and non-ascii strings
        if type(x) == type('') and maxcode > 127:
            t = '****NonAsciiStr: '
        elif type(x) == type(u''):
            t = '*****UnicodeStr: '
        else:
            t = None
        if t:
            sl.append(t + repr(x))
    s = '\n'.join(sl)
    return s
StringIO.getvalue = getvalue
StringIO.pt_parts = pt_parts
