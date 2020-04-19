# -*- coding: utf-8 -*-
# Copyright: (C) 2020 Lovac42
# Support: https://github.com/lovac42/HoochieBaby
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


from aqt import mw
from aqt.utils import tooltip


FILTERED_DECK = 3


class Tests:
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = -1


class LrnTest(Tests):
    def testWrap(self, checkbox):
        if mw.state != "review":
            tooltip("Baby can't run self-tests, you are not in the reviewer.", period=1200)
        elif not mw.col.sched.lrnCount:
            tooltip("Baby can't run self-tests, you don't have enough dLrn cards.", period=1200)
        else:
            self.reset()
            # Clears queue from blocking test. But this must be
            # reset to avoid double loading of the same card.
            mw.col.sched.lrnCount = 20
            mw.col.sched._lrnDayQueue = []
            try:
                mw.col.sched._fillLrnDay()
            finally:
                mw.reset()

            if self.state==FILTERED_DECK:
                tooltip("Baby doesn't work with filtered decks.", period=1200)
                return

            # (0,0) , (1,1) , (2,1)
            assert checkbox == self.state or (checkbox==2 and self.state==1), "\
HoochieBaby, self-test failed. Test value was not as expected."

            if checkbox:
                tooltip("Baby was wrapped successfully!", period=800)
            else:
                tooltip("Baby was unwrapped...", period=800)



class GetCardTest(Tests):
    def testWrap(self, checkbox):
        if mw.state != "review":
            tooltip("Baby can't run self-tests, you are not in the reviewer.", period=1200)
        elif not mw.col.sched.lrnCount and not mw.col.sched.newCount and not mw.col.sched.revCount:
            tooltip("Baby can't run self-tests, you don't have enough cards.", period=1200)
        else:
            self.reset()
            # Clears queue from blocking test. But this must be
            # reset to avoid double loading of the same card.
            mw.col.sched.lrnCount = 20
            try:
                mw.col.sched.getCard()
            finally:
                mw.reset()

            # Filtered decks never calls getCard.

            assert checkbox == self.state, "\
HoochieBaby, self-test failed. Test value was not as expected."

            if checkbox:
                tooltip("Baby was wrapped successfully!", period=800)
            else:
                tooltip("Baby was unwrapped...", period=800)


run_lrn_tests = LrnTest()
run_get_card_tests = GetCardTest()
