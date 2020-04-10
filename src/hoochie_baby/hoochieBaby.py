# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/HoochieBaby
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


# == User Config =========================================

# This is used to block lapsed cards from showing up
# as learning cards right away. 3-5 is a good range.
CARD_BLOCK = 3  # 1 or greater

# == End Config ==========================================


import random
import anki.sched
from aqt import mw
from anki.hooks import wrap

from .sort import CUSTOM_SORT
from .lib.com.lovac42.anki.version import ANKI20


def getCard(self, _old):
    qc = self.col.conf
    if qc.get("hoochieBaby", 0) == 2:
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
    if not qc.get("hoochieBaby",0):
        return _old(self)

    sortLevel=qc.get("hoochieBabySort", 0)
    assert sortLevel < len(CUSTOM_SORT)
    sortBy=CUSTOM_SORT[sortLevel][1]

    self._lrnDayQueue = self.col.db.list("""
select id from cards where
did in %s and queue = 3 and due <= ?
%s limit ?"""%(self._deckLimit(),sortBy),
               self.today, self.queueLimit)

    if self._lrnDayQueue:
        if sortLevel:
            self._lrnDayQueue.reverse() #preserve order
        else:
            r = random.Random()
            r.shuffle(self._lrnDayQueue)
        return True


#REMOVED patch for: anki.schedv2.Scheduler._fillLrn
# v2 uses heappush with collapseTime in _answerLrnCard()
# v1 uses heappush with dayCutoff time, that blocks the patched queue from rebuilding.
# heappush and heappop are sorted, so can't add shuffle

anki.sched.Scheduler._getCard = wrap(anki.sched.Scheduler._getCard, getCard, 'around')
anki.sched.Scheduler._fillLrnDay = wrap(anki.sched.Scheduler._fillLrnDay, fillLrnDay, 'around')
if not ANKI20:
    import anki.schedv2
    anki.schedv2.Scheduler._getCard = wrap(anki.schedv2.Scheduler._getCard, getCard, 'around')
    anki.schedv2.Scheduler._fillLrnDay = wrap(anki.schedv2.Scheduler._fillLrnDay, fillLrnDay, 'around')
