# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2003 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""Batching Support
"""

from zope.interface import implements
from zope.interface.common.mapping import IItemMapping

class IBatch(IItemMapping):
    """A Batch represents a sub-list of the full enumeration.

    The Batch constructor takes a list (or any list-like object) of elements,
    a starting index and the size of the batch. From this information all
    other values are calculated.
    """

    def __len__():
        """Return the length of the batch. This might be different than the
        passed in batch size, since we could be at the end of the list and
        there are not enough elements left to fill the batch completely."""

    def __iter__():
        """Creates an iterator for the contents of the batch (not the entire
        list)."""

    def __contains__(key):
        """Checks whether the key (in our case an index) exists."""

    def nextBatch(self):
        """Return the next batch. If there is no next batch, return None."""

    def prevBatch(self):
        """Return the previous batch. If there is no previous batch, return
        None."""

    def first(self):
        """Return the first element of the batch."""

    def last(self):
        """Return the last element of the batch."""

    def total(self):
        """Return the length of the list (not the batch)."""

    def startNumber(self):
        """Give the start **number** of the batch, which is 1 more than the
        start index passed in."""

    def endNumber(self):
        """Give the end **number** of the batch, which is 1 more than the
        final index."""

class SQLObjectBatch(object):

    implements(IBatch)

    def __init__(self, list, start=0, size=20, list_size=None):
        self.list = list
        self.start = start
        if list_size is None:
            # XXX prevBatch and nextBatch will create batches for exactly the
            # same batch length, no need to query for it again and again. So, it
            # is passed in to the constructor.
            self.list_size = list_size = list.count()
        if list_size == 0:
            self.start = -1
        elif start >= list_size:
            raise IndexError, 'start index key out of range'
        self.size = size
        self.trueSize = size
        if start+size >= list_size:
            self.trueSize = list_size-start
        self.end = start+self.trueSize-1

    def __len__(self):
        return self.trueSize

    def __getitem__(self, key):
        if key >= self.trueSize:
            raise IndexError, 'batch index out of range'
        return self.list[self.start+key]

    def __iter__(self):
        return self.list[self.start:self.end+1]

    def __contains__(self, item):
        return item in self.__iter__()

    def nextBatch(self):
        start = self.start + self.size
        if start >= self.list_size:
            return None
        return SQLObjectBatch(self.list, start, self.size, self.list_size)

    def prevBatch(self):
        start = self.start - self.size
        if start < 0:
            return None
        return SQLObjectBatch(self.list, start, self.size, self.list_size)

    def first(self):
        return self.list[self.start]

    def last(self):
        return self.list[self.end]

    def total(self):
        return self.list_size

    def startNumber(self):
        return self.start+1

    def endNumber(self):
        return self.end+1
