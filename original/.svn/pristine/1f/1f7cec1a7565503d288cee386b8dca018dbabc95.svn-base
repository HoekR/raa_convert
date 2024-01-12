# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.app import zapi # XXX not to be used anymore if we switch to Five-1.5
from zope.app.component.hooks import getSite
from Products.Five import BrowserView

class Layout(BrowserView):

    def site_url(self):
        return zapi.absoluteURL(getSite(), self.request)

class Persoon(BrowserView):

    def naam(self):
        adelspredikaat = ''
        adellijketitel = self.context.adellijketitel or ''
        # HACK: we make sure the jonkheer-predikaat (that is treated like
        # an adellijketitel in the database) is displayed before the complete
        # name instead of justr before the geslachtsnaam.
        if adellijketitel.lower() == 'jonkheer':
            adellijketitel = ''
            adelspredikaat = 'jonkheer'
        return '%s %s %s %s %s %s' % (
            adelspredikaat or '',
            self.context.academischetitel or '',
            self.context.voornaam or '',
            adellijketitel or '',
            self.context.tussenvoegsel or '',
            self.context.geslachtsnaam or '')

    def opmerkingen(self):
        if not self.context.opmerkingen:
            return ''
        return self.context.opmerkingen.replace('\n', '\n<br />')

    def bronnen(self):
        bronnen = list(self.context.bronnen)
        bronnen.sort(cmp=lambda x,y: cmp(x.naam, y.naam))
        return bronnen

    def lokale_aanstellingen(self):
        for aanstelling in self.context.aanstellingen:
            if aanstelling.vertegenwoordigend:
                yield aanstelling

    def aanstellingen_bovenlokaal(self):
        for aanstelling in self.context.aanstellingen:
            if not aanstelling.vertegenwoordigend:
                yield aanstelling

class Instelling(BrowserView):

    def functies(self):
        functies = list(self.context.unique_functies)
        functies.sort(cmp=lambda x,y: cmp(x.naam, y.naam))
        return functies
