# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/HoochieBaby
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import aqt
import aqt.preferences
from aqt import mw
from aqt.qt import *
from anki.hooks import wrap

from .sort import CUSTOM_SORT
from .self_test import run_tests
from .lib.com.lovac42.anki.version import ANKI20
from .lib.com.lovac42.anki.gui.checkbox import TristateCheckbox
from .lib.com.lovac42.anki.gui import muffins


loaded = False


def setupUi(self, Preferences):
    global loaded
    loaded = False

    baby_groupbox = muffins.getMuffinsGroupbox(self, "Hoochie Baby!")
    baby_grid_layout = QGridLayout(baby_groupbox)

    r=0
    self.hoochieBaby = TristateCheckbox(baby_groupbox)
    self.hoochieBaby.setDescriptions({
        Qt.Unchecked:        "Hoochie Baby addon has been disabled",
        Qt.PartiallyChecked: "Randomize day-learning queue only",
        Qt.Checked:          "Randomize day-learning queue and jump between new-rev-lrn",
    })
    baby_grid_layout.addWidget(self.hoochieBaby, r, 0, 1, 3)
    self.hoochieBaby.clicked.connect(lambda:onClick(self))
    self.hoochieBaby.onClick = onClick

    r+=1
    self.hoochieBabySortLbl = QLabel(baby_groupbox)
    self.hoochieBabySortLbl.setText("      Sort day-learning cards by:")
    baby_grid_layout.addWidget(self.hoochieBabySortLbl, r, 0, 1, 1)

    self.hoochieBabySort = QComboBox(baby_groupbox)
    sort_itms = CUSTOM_SORT.iteritems if ANKI20 else CUSTOM_SORT.items
    for i,v in sort_itms():
        self.hoochieBabySort.addItem("")
        self.hoochieBabySort.setItemText(i, v[0])
    baby_grid_layout.addWidget(self.hoochieBabySort, r, 1, 1, 3)
    self.hoochieBabySort.currentIndexChanged.connect(lambda:onChanged(self.hoochieBabySort))

    r+=1
    self.baby_footnoteA = QLabel(baby_groupbox)
    self.baby_footnoteA.setText("&nbsp;&nbsp;&nbsp;<i>* This addon does not randomize intra-day learning cards, yet.</i>")
    baby_grid_layout.addWidget(self.baby_footnoteA, r, 0, 1, 3)

    r+=1
    self.baby_footnoteB = QLabel(baby_groupbox)
    self.baby_footnoteB.setText('&nbsp;&nbsp;&nbsp;<i>** Double check your settings for "Learn ahead limit" and RTFM.</i>')
    baby_grid_layout.addWidget(self.baby_footnoteB, r, 0, 1, 3)


def load(self, mw):
    global loaded
    qc = self.mw.col.conf
    cb = qc.get("hoochieBaby", Qt.Unchecked)
    self.form.hoochieBaby.setCheckState(cb)
    idx = qc.get("hoochieBabySort", 0)
    self.form.hoochieBabySort.setCurrentIndex(idx)
    _updateDisplay(self.form)
    loaded = True


def onClick(form):
    state = int(form.hoochieBaby.checkState())
    mw.col.conf['hoochieBaby'] = state
    _updateDisplay(form)
    run_tests.testWrap(state)


def _updateDisplay(form):
    state = form.hoochieBaby.checkState()
    if state == Qt.Checked:
        try: #no muffinTops addon
            if form.muffinTops.checkState():
                form.hoochieBaby.setCheckState(Qt.Unchecked)
                state = Qt.Unchecked
        except: pass
    grayout = state == Qt.Unchecked
    form.hoochieBabySort.setDisabled(grayout)
    form.hoochieBabySortLbl.setDisabled(grayout)
    form.baby_footnoteA.setDisabled(grayout)
    form.baby_footnoteB.setDisabled(grayout)


def onChanged(combobox):
    idx = combobox.currentIndex()
    mw.col.conf['hoochieBabySort'] = idx
    if loaded:
        run_tests.testSort(idx)


# Wrap Crap #################

# if point version < 23? Use old wrap
# TODO: Find the point version for these new hooks.

aqt.forms.preferences.Ui_Preferences.setupUi = wrap(
    aqt.forms.preferences.Ui_Preferences.setupUi, setupUi, "after"
)

aqt.preferences.Preferences.__init__ = wrap(
    aqt.preferences.Preferences.__init__, load, "after"
)

# aqt.preferences.Preferences.accept = wrap(
    # aqt.preferences.Preferences.accept, save, "before"
# )
