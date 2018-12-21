# -*- coding: utf-8 -*-
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/HoochieBaby
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# Version: 0.0.3


# == User Config =========================================

# This is used to block lapsed cards from showing up
# as learning cards right away. 3-5 is a good range.
CARD_BLOCK = 3  # 1 or greater

# == End Config ==========================================
##########################################################

import random
import anki.sched
from aqt import mw
from anki.hooks import wrap

from anki import version
ANKI21 = version.startswith("2.1.")


def getCard(self, _old):
    qc = self.col.conf
    if qc.get("hoochieBaby", False):
        c=None #ret card
        self._fillLrn() #REQUIRED: Ensures lrn queue is built before any lapses are pushed onto the stack

        type=random.randint(0,3)
        if type==1:
            try: #Ensure cards don't repeat as lrn card back-to-back (from revQ to lrnQ)
                id=self._lrnQueue[0][1]
                lstIds=mw.reviewer._answeredIds[-CARD_BLOCK:]
                if id not in lstIds:
                    c = self._getLrnCard(collapse=True)
            except IndexError: pass
        elif type==2:
            c = self._getLrnDayCard()
        elif type==3:
            c = self._getNewCard()

        if not c:
            c = self._getRevCard()
        if c: return c
    return _old(self)


# day learning
def fillLrnDay(self, _old):
    if not self.lrnCount: return False
    if self._lrnDayQueue: return True

    qc = self.col.conf
    if not qc.get("hoochieBaby", False):
        return _old(self)

    self._lrnDayQueue = self.col.db.all("""
select id from cards where
did in %s and queue = 3 and due <= ?
order by due asc limit ?"""%self._deckLimit(),
                self.today, self.queueLimit)
    if self._lrnDayQueue:
        r = random.Random()
        r.shuffle(self._lrnDayQueue)
        return True


#REMOVED patch for: anki.schedv2.Scheduler._fillLrn
# v2 uses heappush with collapseTime in _answerLrnCard()
# v1 uses heappush with dayCutoff time, that blocks the patched queue from rebuilding.
# heappush and heappop are sorted, so can't add shuffle

anki.sched.Scheduler._getCard = wrap(anki.sched.Scheduler._getCard, getCard, 'around')
anki.sched.Scheduler._fillLrnDay = wrap(anki.sched.Scheduler._fillLrnDay, fillLrnDay, 'around')
if ANKI21:
    import anki.schedv2
    anki.schedv2.Scheduler._getCard = wrap(anki.schedv2.Scheduler._getCard, getCard, 'around')
    anki.schedv2.Scheduler._fillLrnDay = wrap(anki.schedv2.Scheduler._fillLrnDay, fillLrnDay, 'around')


##################################################
#
#  GUI stuff, adds preference menu options
#
#################################################
import aqt
import aqt.preferences
from aqt.qt import *


if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets

def setupUi(self, Preferences):
    r=self.gridLayout_4.rowCount()
    self.hoochieBaby = QtWidgets.QCheckBox(self.tab_1)
    self.hoochieBaby.setText(_('Hoochie Baby! Queue Controller'))
    self.gridLayout_4.addWidget(self.hoochieBaby, r, 0, 1, 3)

def __init__(self, mw):
    qc = self.mw.col.conf
    cb=qc.get("hoochieBaby", 0)
    self.form.hoochieBaby.setCheckState(cb)

def accept(self):
    qc = self.mw.col.conf
    qc['hoochieBaby']=self.form.hoochieBaby.checkState()

aqt.forms.preferences.Ui_Preferences.setupUi = wrap(aqt.forms.preferences.Ui_Preferences.setupUi, setupUi, "after")
aqt.preferences.Preferences.__init__ = wrap(aqt.preferences.Preferences.__init__, __init__, "after")
aqt.preferences.Preferences.accept = wrap(aqt.preferences.Preferences.accept, accept, "before")

