from zope.interface import Interface, Attribute
from zope.schema.interfaces import IField

from sqlos.interfaces import IISQLObject

class IRaa(Interface):
    pass

class IContainer(Interface):
    pass

class INamed(Interface):
    pass

class INamedContainer(Interface):
    pass

class IQuery(Interface):

    def execute(data, **modifiers):
        """
        Construct a query based on key/value in the data mapping and the
        modifiers provided.
        """

class ITimePeriod(IField):
    u"""A Field containing a tuple from start Datetime to end Datetime.

    Start Datetime *or* end Datetime may be None, but not both.
    """
