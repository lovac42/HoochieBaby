# -*- coding: utf-8 -*-
# Copyright: (C) 2018-2020 Lovac42
# Support: https://github.com/lovac42/HoochieBaby
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html


import aqt
import aqt.preferences
from aqt.qt import *
from anki.lang import _
from anki.hooks import wrap

from .sort import CUSTOM_SORT
from .lib.com.lovac42.anki.version import ANKI21, ANKI20
from .lib.com.lovac42.anki.gui.checkbox import TristateCheckbox
from .lib.com.lovac42.anki.gui import muffins


if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets


def setupUi(self, Preferences):
    grid_layout = muffins.getMuffinsTab(self)
    r = grid_layout.rowCount()

    baby_groupbox = QtWidgets.QGroupBox(self.lrnStage)
    baby_groupbox.setTitle("Hoochie Baby!")
    baby_grid_layout = QtWidgets.QGridLayout(baby_groupbox)
    grid_layout.addWidget(baby_groupbox, r, 0, 1, 3)

    self.hoochieBaby = TristateCheckbox(baby_groupbox)
    self.hoochieBaby.setDescriptions({
        Qt.Unchecked:        "Hoochie Baby addon has been disabled",
        Qt.PartiallyChecked: "Randomize day-learning queue only",
        Qt.Checked:          "Randomize day-learning queue and jump between new-rev-lrn",
    })
    baby_grid_layout.addWidget(self.hoochieBaby, r, 0, 1, 3)
    self.hoochieBaby.clicked.connect(lambda:toggle(self))

    r+=1
    self.hoochieBabySortLbl = QtWidgets.QLabel(baby_groupbox)
    self.hoochieBabySortLbl.setText(_("      Sort day-learning cards by:"))
    baby_grid_layout.addWidget(self.hoochieBabySortLbl, r, 0, 1, 1)

    self.hoochieBabySort = QtWidgets.QComboBox(baby_groupbox)
    sort_itms = CUSTOM_SORT.iteritems if ANKI20 else CUSTOM_SORT.items
    for i,v in sort_itms():
        self.hoochieBabySort.addItem("")
        self.hoochieBabySort.setItemText(i, _(v[0]))
    baby_grid_layout.addWidget(self.hoochieBabySort, r, 1, 1, 3)


def load(self, mw):
    qc = self.mw.col.conf
    cb=qc.get("hoochieBaby", Qt.Unchecked)
    self.form.hoochieBaby.setCheckState(cb)
    idx=qc.get("hoochieBabySort", 0)
    self.form.hoochieBabySort.setCurrentIndex(idx)
    toggle(self.form)


def save(self):
    toggle(self.form)
    qc = self.mw.col.conf
    qc['hoochieBaby']=int(self.form.hoochieBaby.checkState())
    qc['hoochieBabySort']=self.form.hoochieBabySort.currentIndex()


def toggle(self):
    state = self.hoochieBaby.checkState()
    if state == Qt.Checked:
        try: #no muffinTops addon
            if self.muffinTops.checkState():
                self.hoochieBaby.setCheckState(Qt.Unchecked)
                state = Qt.Unchecked
        except: pass
    self.hoochieBabySort.setDisabled(state == Qt.Unchecked)
    self.hoochieBabySortLbl.setDisabled(state == Qt.Unchecked)


# Wrap Crap #################

aqt.forms.preferences.Ui_Preferences.setupUi = wrap(
    aqt.forms.preferences.Ui_Preferences.setupUi, setupUi, "after"
)

aqt.preferences.Preferences.__init__ = wrap(
    aqt.preferences.Preferences.__init__, load, "after"
)

aqt.preferences.Preferences.accept = wrap(
    aqt.preferences.Preferences.accept, save, "before"
)
