# -*- coding: utf-8 -*-
from datetime import date, datetime, timedelta
from xml.sax.saxutils import escape
from zope.interface import implements

from zope.app import zapi
from zope.app.form.interfaces import IInputWidget, IDisplayWidget
from zope.app.form import InputWidget
from zope.app.form.browser.interfaces import ITerms

from zope.app.form.browser import TextWidget
from zope.app.form.browser.widget import renderElement, BrowserWidget, DisplayWidget
from zope.app.form.browser import RadioWidget as RadioWidget_
from zope.app.form.browser import MultiSelectWidget
from zope.app.form.browser import CheckBoxWidget

from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

import source_widget

def centered_truncate(string, max_length=100):
    string = escape(string)
    if len(string) < max_length:
        return string
    part_length = (max_length - 3) / 2
    return '%s...%s' % (string[:part_length], string[-part_length:])

class Alphabet(TextWidget):
    pass

class EmptyHidden(TextWidget):

    def hidden(self):
        return renderElement(
            self.tag,
            type='hidden',
            name=self.name,
            id=self.name,
            value='',
            cssClass=self.cssClass,
            extra=self.extra)

# XXX the widgets situation for sources and vocabularies in Zope-3.2 is not
# really, well, uhm, clear... And the behaviour actually changed when migrating
# from Zope-294 to Zope-296, since it apparently came with an slightly newer
# version of Zope-3.2 as well.
#
# The message factory stuff is be able to customize the very first 'empty' item
# in the select field. _toFieldValue is overrided to handle the situation where
# the 'empty' element is actually selected by the user.
#
# This is all a bit hairy
from zope.app.i18n import ZopeMessageFactory as _
no_value_msg = _("foobar", "(geen selectie)")

class EmptySelectionHelper(object):

    def _toFieldValue(self, input):
        if input is None:
            return []
        if not isinstance(input, list):
            input = [input]
        return self.convertTokensToValues([i for i in input if i])

class ListWidget(EmptySelectionHelper, MultiSelectWidget):
    _displayItemForMissingValue = True
    _messageNoValue = no_value_msg
    required = False
    cssClass = 'inlineme'
    size = 9

    def __init__(self, field, request):
        super(ListWidget, self).__init__(
            field, field.value_type.vocabulary, request)

class ShortListWidget(ListWidget):
    cssClass = 'inlineme short'
    size = 3

class FittedListWidget(ListWidget):
    cssClass = 'inlineme short'

    @property
    def size(self):
        return len(self.vocabulary) + 1

class RadioWidget(RadioWidget_):

    _messageNoValue = no_value_msg

    def __init__(self, field, request):
        super(RadioWidget, self).__init__(field, field.vocabulary, request)

class HorizontalRadioWidget(RadioWidget):
    orientation = 'horizontal'

class TimePeriodWidget(BrowserWidget, InputWidget):

    # XXX this is not a proper widget yet, but works for the application
    # at hand.

    implements(IInputWidget)

    def getInputValue(self):
        """Return value suitable for the widget's field.

        The widget must return a value that can be legally assigned to
        its bound field or otherwise raise ``WidgetInputError``.

        The return value is not affected by `setRenderedValue()`.
        """

        form = self.request.form
        year, month, day = [
            form.get(self.name+'.year'),
            form.get(self.name+'.month'),
            form.get(self.name+'.day')]
        to_year, to_month, to_day = [
            form.get(self.name+'.to.year'),
            form.get(self.name+'.to.month'),
            form.get(self.name+'.to.day')]

        from_ = self._dateFromInput(year, month, day)
        to = self._dateFromInput(to_year, to_month, to_day, as_end_date=True)
        return from_, to

    def _dateFromInput(self, year, month, day, as_end_date=False):
        # XXX taken from feedfrontend.py - there's probably a better way
        # to package this.
        try:
            year = int(year)
            if not datetime.min.year <= year <= datetime.max.year:
                raise ValueError
        except (ValueError, TypeError), e:
            # If we do not even have a year, we just don't have a reasonable
            # datetime value at all.
            return None

        try:
            month = int(month)
            if not 1 <= month <= 12:
                raise ValueError
        except (ValueError, TypeError), e:
            if as_end_date:
                return datetime(year, 12, 31)
            return datetime(year, 1, 1)

        try:
            day = int(day)
            if not 1 <= day <= 31:
                raise ValueError
        except (ValueError, TypeError), e:
            if as_end_date:
                return datetime(year, month+1, 1) - timedelta(days=1)
            return datetime(year, month, 1)

        return datetime(year, month, day)

    def hasInput(self):
        form = self.request.form
        for key, value in form.items():
            if key.startswith(self.name+'.'):
                return True
        return False

    def __call__(self):
        form = self.request.form
        widget = 'tussen %s-%s-%s en %s-%s-%s'
        return widget % (
            self._renderDaySelect(self.name+'.day'),
            self._renderMonthSelect(self.name+'.month'),
            renderElement(
                'input',
                type='text',
                name=self.name+'.year',
                id=self.name+'.year',
                value=form.get(self.name+'.year', ''),
                size=4,
                cssClass='year'
                ),
            self._renderDaySelect(self.name+'.to.day'),
            self._renderMonthSelect(self.name+'.to.month'),
            renderElement(
                'input',
                type='text',
                name=self.name+'.to.year',
                id=self.name+'.to.year',
                value=form.get(self.name+'.to.year', ''),
                size=4,
                cssClass='year'
                ),
            )

    def _renderMonthSelect(self, name):
        contents  = []
        months = [
            '--', 'jan', 'feb', 'maart', 'apr', 'mei', 'jun',
            'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        for i in range(len(months)):
            if str(i) == self.request.form.get(name, None):
                extra = 'selected="selected"'
            else:
                extra = ''
            contents.append(
                renderElement(
                    'option', value=i, contents=months[i], extra=extra))
        return renderElement(
            'select', name=name, id=name, contents='\n'.join(contents))

    def _renderDaySelect(self, name):
        contents  = []
        contents.append(
            renderElement('option', value=0, contents='--'))
        for i in range(1,32):
            if str(i) == self.request.form.get(name, None):
                extra = 'selected="selected"'
            else:
                extra = ''
            contents.append(
                renderElement(
                    'option', value=i, contents=i, extra=extra))
        return renderElement(
            'select', name=name, id=name, contents='\n'.join(contents))

    def hidden(self):
        """Render the widget as a hidden field."""
        raise NotImplementedError # not yet

    def error(self):
        """Render the validation error for the widget, or return
        an empty string if no error"""
        return '' # not yet

class TimePeriodDisplayWidget(DisplayWidget):

    def __call__(self):
        return repr((datetime(1664,1,1), datetime(1700,1,1)))
