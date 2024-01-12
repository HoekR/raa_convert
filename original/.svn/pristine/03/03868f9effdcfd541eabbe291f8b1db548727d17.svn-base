# -*- coding: utf-8 -*-
import cgi, urllib
from zope.interface import Interface
from zope.schema import vocabulary
from zope.schema import List, Set, TextLine, Choice, Date, Bool, SourceText
from zope.app import zapi # XXX not to be used anymore if we switch to Five-1.5
from zope.app.component.hooks import getSite
from zope.app.form.browser import itemswidgets

from zope.formlib.interfaces import IActions
from zope.formlib import form
from Products.Five.formlib.formbase import FormBase
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from Products.FiveSQLOS.interfaces import IFiveSQLObject

from Products.raa.interfaces import IQuery
from Products.raa import model
from Products.raa.container import Wrapper
from Products.raa.browser import widget

from batch import SQLObjectBatch
class Batch(SQLObjectBatch):

    def __init__(self, context, list, start=0, size=20):
        SQLObjectBatch.__init__(self, list, start, size)
        self.context = context

    def __iter__(self):
        return iter([
            Wrapper(i).__of__(self.context)
            for i in self.list[self.start:self.end+1]])

class dictinorder(dict):
    # XXX works if only key,values are *added* to the dict.
    # Other mutations are not tracked.

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.key_sequence = []

    def __setitem__(self, key, value):
        dict.__setitem__(self, key, value)
        self.key_sequence.append(key)

    def setdefault(self, key, value):
        if key not in self.key_sequence:
            self.key_sequence.append(key)
        return dict.setdefault(self, key, value)

    def keys(self):
        return self.key_sequence

def encode(value):
    if isinstance(value, unicode):
        return value.encode('utf-8')
    return value

def safeUrlencode(data):
    params = []
    for key, value in data.items():
        if value is None:
            continue
        if isinstance(value, list):
            for subvalue in value:
                params.append((key+':list', encode(subvalue)))
        else:
            params.append((key, encode(value)))
    return urllib.urlencode(params)

class SearchForm(FormBase):

    batch = None
    orderables = None
    query = IQuery
    errors = ()

    def render(self):
        # The raa forms are special: we always render the form and we
        # we never reset the form.
        self.form_result = self.template()
        return self.form_result

    def _getOrderBy(self):
        return self.request.form.get('order_by', 'geslachtsnaam')

    @form.action('zoeken')
    def search(self, action, data):
        order_by = self._getOrderBy()
        results = self.query(self.context).execute(data, orderBy=order_by)
        self.setCurrentBatch(results)

    def setCurrentBatch(self, results):
        form = self.request.form
        start = int(form.get('start', 0))
        size = int(form.get('size', 100))
        self.batch = Batch(
            self.context.aq_inner, results, start=start, size=size
            )

    def _url(self, data=None):
        if data is None:
            return self.request['URL0']
        return self.request['URL0'] + '?' + safeUrlencode(data)

    def groupableItems(self):
        return []

    def orderableItems(self):
        if self.orderables is None:
            raise StopIteration

        form = {}
        form.update(self.request.form)
        form['start'] = 0

        for name, order_key in self.orderables:
            form['order_by'] = order_key
            up_url = self._url(form)
            form['order_by'] = '-' + order_key
            down_url = self._url(form)
            yield {
                'name': name,
                'descending_url': down_url,
                'ascending_url': up_url
                }

    def nextBatchURL(self):
        next = self.batch.nextBatch()
        if next is None:
            return None
        form = self.request.form
        form['start'] = next.start
        return self._url(form)

    def previousBatchURL(self):
        prev = self.batch.prevBatch()
        if prev is None:
            return None
        form = self.request.form
        form['start'] = prev.start
        return self._url(form)

application_options = vocabulary.SimpleVocabulary([
    vocabulary.SimpleTerm('aanstelling', 'aanstelling', 'aanstellingsperiode'),
    vocabulary.SimpleTerm('leven', 'leven', 'geboorte- en overlijdensdatum')])

adel_options = vocabulary.SimpleVocabulary([
    vocabulary.SimpleTerm(True, 'van_adel', 'van adel'),
    vocabulary.SimpleTerm(False, 'niet_van_adel', 'niet van adel')])

select_list_options = vocabulary.SimpleVocabulary([
    vocabulary.SimpleTerm(False, 'any', 'of'),
    vocabulary.SimpleTerm(True, 'all', 'en')])


class IPersonen(Interface):

    geslachtsnaam = TextLine(
        title=u'geslachtsnaam', required=False, description=(
            u'Beperk op geslachtsnaam of deel daarvan. '
            u'Gebruik "*" als wildcard. Meer woord(delen) worden gecombineerd.'
            )
        )

    searchable_geslachtsnaam = TextLine(
        title=u'geslachtsnaam', required=False, description=(
            u'Beperk op geslachtsnaam of deel daarvan. '
            u'Gebruik "*" als wildcard. Meer woord(delen) worden gecombineerd.'
            )
        )

    voornaam = TextLine(
        title=u'voornaam', required=False, description=(
            u'Beperk op voornaam of deel daarvan. '
            u'Gebruik "*" als wildcard. Meer woord(delen) worden gecombineerd.'
            )
        )

    alias = TextLine(
        title=u'naamsvariant', required=False, description=(
            u'Beperk op alias of deel daarvan. '
            u'Gebruik "*" als wildcard. Meer woord(delen) worden gecombineerd.'
            )
        )

    heerlijkheid = TextLine(
        title=u'heerlijkheid', required=False, description=(
            u'Beperk op heerlijkheid of deel daarvan. '
            u'Gebruik "*" als wildcard. Meer woord(delen) worden gecombineerd.'
            )
        )

    opmerkingen = TextLine(
        title=u'opmerkingen', required=False, description=(
            u'Beperk op opmerkingen of deel daarvan. '
            u'Gebruik "*" als wildcard. Meer woord(delen) worden gecombineerd.'
            )
        )

    adel = Choice(
        title=u'adel', required=False, vocabulary=adel_options, description=(
            u'Beperk op personen, evt met adelspredikaat'
            )
        )

    adellijketitel = List(
        title=u'adellijketitel', required=False,
        value_type=Choice(vocabulary=model.adellijketitels), description=(
            u'Beperk op adellijke titel en/of predikaat. Kies één of meer '
            u'titels uit de lijst.'), default=[''])

    academischetitel = List(
        title=u'academischetitel', required=False,
        value_type=Choice(vocabulary=model.academischetitels), description=(
            u'Beperk op academische titel. Kies één of meer titels uit '
            u'de lijst.'), default=[''])

    stand = List(
        title=u'stand', required=False,
        value_type=Choice(vocabulary=model.standen), description=(
            u'Beperk op stand. Kies één of meer standen uit de lijst.'),
            default=[''])

    timespan_birth = model.TimePeriod(
        title=u'geboortedatum', required=False, description=(
            u'Beperk op periode; op basis van de geboorte- en '
            u'overlijdendsdata of begin- einddata van de '
            u'aanstellingen die de betreffende personen bekleedden. Maand- en '
            u'dagaanduidingen zijn facultatief.'
            )
        )

    timespan_death = model.TimePeriod(
        title=u'overlijdensdatum', required=False, description=(
            u'Beperk op periode; op basis van de geboorte- en '
            u'overlijdendsdata of begin- einddata van de '
            u'aanstellingen die de betreffende personen bekleedden. Maand- en '
            u'dagaanduidingen zijn facultatief.'
            )
        )

    timespan_aanst = model.TimePeriod(
        title=u'aanstellingsdatum', required=False, description=(
            u'Beperk op periode; op basis van de geboorte- en '
            u'overlijdendsdata of begin- einddata van de '
            u'aanstellingen die de betreffende personen bekleedden. Maand- en '
            u'dagaanduidingen zijn facultatief.'
            )
        )

    functie = List(
        title=u'functie', required=False,
        value_type=Choice(vocabulary=model.functies), description=(
            u'Beperk op bekleedde functie. Kies één of meerdere functies uit '
            u'de lijst.'), max_length=5, default=[''])
    functie_and_query = Choice(
        title=u'', required=True, default=False, vocabulary=select_list_options)

    instelling = List(
        title=u'instelling', required=False,
        value_type=Choice(vocabulary=model.instellingen), description=(
            u'Beperk op instelling in welke de functie werd uitgeoefend. Kies één '
            u'of meer instellingen uit de lijst.'), max_length=5, default=[''])
    instelling_and_query = Choice(
        title=u'', required=True, default=False, vocabulary=select_list_options)

    provincie = List(
        title=u'provincie', required=False,
        value_type=Choice(vocabulary=model.provincien), description=(
            u'Beperk op functie. Kies één of meer functies uit '
            u'de lijst.'), default=[''])

    regio = List(
        title=u'regio', required=False,
        value_type=Choice(vocabulary=model.regios), description=(
            u'Beperk op functie. Kies één of meer functies uit '
            u'de lijst.'), default=[''])

    lokaal = List(
        title=u'lokaal', required=False,
        value_type=Choice(vocabulary=model.lokalen), description=(
            u'Beperk op functie. Kies één of meer functies uit '
            u'de lijst.'), default=[''])


class PersoonSearchForm(SearchForm):

    prefix = 'persoon'

    template = ZopeTwoPageTemplateFile('templates/personen.pt')

    label = u'personen'

    form_fields = form.Fields(IPersonen)
    form_fields['functie'].custom_widget = widget.ListWidget
    form_fields['functie_and_query'].custom_widget = widget.HorizontalRadioWidget

    form_fields['instelling'].custom_widget = widget.ListWidget
    form_fields['instelling_and_query'].custom_widget = widget.HorizontalRadioWidget

    form_fields['lokaal'].custom_widget = widget.ListWidget
    form_fields['provincie'].custom_widget = widget.ListWidget
    form_fields['regio'].custom_widget = widget.ListWidget
    form_fields['stand'].custom_widget = widget.FittedListWidget

    form_fields['adellijketitel'].custom_widget = widget.ShortListWidget
    form_fields['academischetitel'].custom_widget = widget.ShortListWidget

    # form_fields['timespan_application'].custom_widget = widget.HorizontalRadioWidget
    form_fields['adel'].custom_widget = widget.HorizontalRadioWidget

    # XXX gros hack
    form_fields['geslachtsnaam'].custom_widget = widget.EmptyHidden

    orderables = [
        ('voornaam', 'voornaam'), ('geslachtsnaam', 'geslachtsnaam'),
        ('geboortedatum', 'geboortedatum'),('overlijdensdatum','overlijdensdatum')
        ]
    groupables = None

_GET_query_string_personen = (
    # omit:
    #'persoon.geslachtsnaam=&'
    #'persoon.voornaam=&'
    #'persoon.functie=&'
    #'persoon.instelling=&'
    #'persoon.searchable_geslachtsnaam=&'
    'persoon.functie_and_query=any&'
    'persoon.functie_and_query-empty-marker=1&'
    'persoon.instelling_and_query=any&'
    'persoon.instelling_and_query-empty-marker=1&'
    'persoon.alias=&'
    'persoon.heerlijkheid=&'
    'persoon.adel-empty-marker=1&'
    'persoon.adellijketitel-empty-marker=1&'
    'persoon.academischetitel-empty-marker=1&'
    'persoon.birth-empty-marker=1&'
    'persoon.timespan_birth.day=0&persoon.timespan_birth.month=0&persoon.timespan_birth.year=&'
    'persoon.timespan_birth.to.day=0&persoon.timespan_birth.to.month=0&persoon.timespan_birth.to.year=&'
    'persoon.death-empty-marker=1&'
    'persoon.timespan_death.day=0&persoon.timespan_death.month=0&persoon.timespan_death.year=&'
    'persoon.timepsan_death.to.day=0&persoon.timespan_death.to.month=0&persoon.timespan_death.to.year=&'
    'persoon.periode-empty-marker=1&'
    'persoon.timespan_inst.day=0&persoon.timespan_inst.month=0&persoon_.timespan_inst.year=&'
    'persoon.timepsan_inst.to.day=0&persoon.timespan_inst.to.month=0&persoon.timespan_inst.to.year=&'
#    'persoon.timespan_application=aanstelling&'
#    'persoon.timespan_application-empty-marker=1&'
    'persoon.functie-empty-marker=1&'
    'persoon.instelling-empty-marker=1&'
    'persoon.lokaal-empty-marker=1&'
    'persoon.provincie-empty-marker=1&'
    'persoon.stand-empty-marker=1&'
    'persoon.regio-empty-marker=1&'
    'persoon.actions.zoeken=zoeken'
    )

class PersonenBy(FormBase):

    def __call__(self):
        # XXX hardcode submit URL for now
        form = self.request.form
        query = _GET_query_string_personen + '&' + safeUrlencode({
            'persoon.voornaam': form.get('persoon.voornaam', ''),
            'persoon.geslachtsnaam': form.get('persoon.geslachtsnaam', ''),
            'persoon.searchable_geslachtsnaam': form.get('persoon.searchable_geslachtsnaam', ''),
            'persoon.functie': form.get('persoon.functie'),
            'persoon.instelling': form.get('persoon.instelling'),
            })
        url = self.request['URL1'] + '?' + query
        response = self.request.response
        response.redirect(url)

    application_options = vocabulary.SimpleVocabulary([
    vocabulary.SimpleTerm('aanstelling', 'aanstelling', 'aanstellingsperiode'),
    vocabulary.SimpleTerm('leven', 'leven', 'geboorte- en overlijdensdatum')])

class IAanstellingen(Interface):

    periode = model.TimePeriod(
        title=u'periode', required=False, description=(
            u'Beperk op  periode; gebaseerd op begin- einddata van de '
            u'aanstellingen die de betreffende personen bekleedden. Maand- en '
            u'dagaanduidingen zijn optioneel.'))

    functie = List(
        title=u'functie', required=False,
        value_type=Choice(vocabulary=model.functies), description=(
            u'Beperk op bekleedde functie. Kies één of meerdere functies uit '
            u'de lijst.'), max_length=5, default=[''])

    functie_and_query = Choice(
        title=u'', required=True, default=False, vocabulary=select_list_options)

    instelling = List(
        title=u'instelling', required=False,
        value_type=Choice(vocabulary=model.instellingen), description=(
            u'Beperk op instelling waarbinnen de functie werd bekleed. Kies één '
            u'of meerdere instellingen uit de lijst.'), max_length=5, default=[''])

    instelling_and_query = Choice(
        title=u'', required=True, default=False, vocabulary=select_list_options)

    provincie = List(
        title=u'provincie', required=False,
        value_type=Choice(vocabulary=model.provincien), description=(
            u'Beperk op bekleedde functie. Kies één of meerdere functies uit '
            u'de lijst.'), default=[''])

    regio = List(
        title=u'regio', required=False,
        value_type=Choice(vocabulary=model.regios), description=(
            u'Beperk op bekleedde functie. Kies één of meerdere functies uit '
            u'de lijst.'), default=[''])

    lokaal = List(
        title=u'lokaal', required=False,
        value_type=Choice(vocabulary=model.lokalen), description=(
            u'Beperk op bekleedde functie. Kies één of meerdere functies uit '
            u'de lijst.'), default=[''])

    stand = List(
        title=u'stand', required=False,
        value_type=Choice(vocabulary=model.standen), description=(
            u'Beperk op stand. Kies één of meer standen uit de lijst.'),
            default=[''])

    adel = Choice(
        title=u'adel', required=False, vocabulary=adel_options, description=(
            u'Beperk op personen, evt met adelspredikaat'
            )
        )



class AanstellingSearchForm(SearchForm):

    prefix = 'aanstelling'
    label = u'aanstellingen'
    template = ZopeTwoPageTemplateFile('templates/aanstellingen.pt')

    form_fields = form.Fields(IAanstellingen)
    
    form_fields['functie'].custom_widget = widget.ListWidget
    form_fields['functie_and_query'].custom_widget = widget.HorizontalRadioWidget

    form_fields['instelling'].custom_widget = widget.ListWidget
    form_fields['instelling_and_query'].custom_widget = widget.HorizontalRadioWidget


    form_fields['lokaal'].custom_widget = widget.ListWidget
    form_fields['provincie'].custom_widget = widget.ListWidget
    form_fields['regio'].custom_widget = widget.ListWidget
    form_fields['stand'].custom_widget = widget.FittedListWidget
    form_fields['adel'].custom_widget = widget.HorizontalRadioWidget

    orderables = [
        ('datum van aanstelling', 'van'),
        ('voornaam', 'voornaam'), ('geslachtsnaam', 'geslachtsnaam'),
        ('geboortedatum', 'geboortedatum'),
        ('overlijdensdatum', 'overlijdensdatum'),
        ]
    groupables = ['instelling', 'functie']

    def _getGrouping(self):
        grouping = self.request.form.get('grouping_by') or 'instelling'
        idx = self.groupables.index(grouping)
        return self.groupables[idx], self.groupables[idx-1]

    def groupableItems(self):
        form = {}
        form.update(self.request.form)
        form['start'] = 0
        for grouping_key in self.groupables:
            form['grouping_by'] = grouping_key
            yield {'name': grouping_key, 'url': self._url(form)}

    def _getOrderBy(self):
        # ordering depends on the grouping as well
        outer, inner = self._getGrouping()
        order_by = ['%s.naam'%outer, '%s.naam'%inner]
        # by default order on 'van'
        order_by.append(self.request.form.get('order_by', 'van'))
        return order_by

    def groupedItems(self):
        outer_attr, inner_attr = self._getGrouping()
        grouped = dictinorder()
        for item in self.batch:
            outer = getattr(item, outer_attr)
            inner = getattr(item, inner_attr)
            inner_group = grouped.setdefault(outer, dictinorder())
            items = inner_group.setdefault(inner, [])
            items.append(item)
        return grouped

    def wrappit(self, item):
        return Wrapper(item).__of__(self.context) # to make sqlobjects traverable

_GET_query_string_aanstellingen = (
    'aanstelling.periode-empty-marker=1&'
    'aanstelling.periode.day=0&aanstelling.periode.month=0&aanstelling.periode.year=&'
    'aanstelling.functie-empty-marker=1&'
    'aanstelling.functie_and_query=any&'
    'aanstelling.functie_and_query-empty-marker=1&'
    'aanstelling.instelling-empty-marker=1&'
    'aanstelling.instelling_and_query=any&'
    'aanstelling.instelling_and_query-empty-marker=1&'
    'aanstelling.lokaal-empty-marker=1&'
    'aanstelling.provincie-empty-marker=1&'
    'aanstelling.regio-empty-marker=1&'
    'aanstelling.stand-empty-marker=1&'
    'aanstelling.adel-empty-marker=1&'
    'aanstelling.actions.zoeken=zoeken'
    'aanstelling.actions.reset=wissen'
    )

class AanstellingenBy(FormBase):

    prefix = 'aanstelling'

    def __call__(self):
        form = self.request.form
        query = _GET_query_string_aanstellingen + '&' + safeUrlencode({
            'aanstelling.instelling': form.get('aanstelling.instelling'),
            'aanstelling.functie': form.get('aanstelling.functie')
            })
        url = self.request['URL1'] + '?' + query
        response = self.request.response
        response.redirect(url)

apply_result_options = vocabulary.SimpleVocabulary([
    vocabulary.SimpleTerm(True, 'do_apply', 'ja')])

class INamedSearch(Interface):

    naam = TextLine(
        title=u'naam', required=False, description=(
            u'Gebruik "*" als wildcard. Meerdere woord(delen) worden '
            u'gecombineerd.'))

    apply = Bool(
        title=u'', required=True, default=False, description=(
            u'gebruik het resultaat om aanstellingen te vinden.'))

class NamedSearchForm(SearchForm):

    prefix= None
    label = None

    orderables = [('naam', 'naam')]
    template = ZopeTwoPageTemplateFile('templates/named_search.pt')

    form_fields = form.Fields(INamedSearch)

    def apply_url(self):
        pass

    @form.action('zoeken')
    def search(self, action, data):
        modifiers = {}
        order_by = self._getOrderBy()
        if order_by is not None:
            modifiers['orderBy'] = order_by.encode('utf-8')
        results = self.query(self.context).execute(data, **modifiers)

        count = results.count()
        if data.get('apply') and 0 < count <= 5:
            ids = [item.id for item in results]
            query = _GET_query_string_aanstellingen + '&' + safeUrlencode({
                'aanstelling.%s'%self.prefix: ids})
            site_url = zapi.absoluteURL(getSite(), self.request)
            url = site_url + '/aanstellingen?' + query
            self.request.response.redirect(url)
            return 'will-be-redirected'

        self.setCurrentBatch(results)

class FunctieSearchForm(NamedSearchForm):
    prefix= 'functie'
    label = 'Functies'

class InstellingSearchForm(NamedSearchForm):
    prefix= 'instelling'
    label = 'Instellingen'

class IToelichtingEdit(Interface):

    toelichting = SourceText(
        title=u'toelichting', required=False, description=u'')

class EditToelichtingForm(FormBase):
    prefix= 'edit_toelichting'
    label = 'Edit Institutionele Toelcihting'

    template = ZopeTwoPageTemplateFile('templates/edit_toelichting.pt')

    form_fields = form.Fields(IToelichtingEdit)

    @property
    def toelichting(self):
        return self.context.toelichting

    def save_toelichting(self, data):
        self.context.context.toelichting = data

    @form.action('save')
    def save(self, action, data):
        self.save_toelichting(data.get('toelichting', ''))
        url = zapi.absoluteURL(self.context, self.request)
        self.request.response.redirect(url)
        return 'will-be-redirected'

    @form.action('save and edit')
    def save_and_edit(self, action, data):
        self.save_toelichting(data.get('toelichting', ''))
