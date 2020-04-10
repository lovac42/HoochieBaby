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
# from .lib.com.lovac42.anki.gui.checkbox import TristateCheckbox
# from .lib.com.lovac42.anki.gui import muffins


if ANKI21:
    from PyQt5 import QtCore, QtGui, QtWidgets
else:
    from PyQt4 import QtCore, QtGui as QtWidgets


def setupUi(self, Preferences):
    try:
        grid=self.lrnStageGLayout
    except AttributeError:
        self.lrnStage=QtWidgets.QWidget()
        self.tabWidget.addTab(self.lrnStage, "Muffins")
        self.lrnStageGLayout=QtWidgets.QGridLayout()
        self.lrnStageVLayout=QtWidgets.QVBoxLayout(self.lrnStage)
        self.lrnStageVLayout.addLayout(self.lrnStageGLayout)
        spacerItem=QtWidgets.QSpacerItem(1, 1, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.lrnStageVLayout.addItem(spacerItem)

    r=self.lrnStageGLayout.rowCount()
    self.hoochieBaby=QtWidgets.QCheckBox(self.lrnStage)
    self.hoochieBaby.setTristate(True)
    self.hoochieBaby.setText(_('Hoochie Baby! Queue Controller'))
    self.lrnStageGLayout.addWidget(self.hoochieBaby, r, 0, 1, 3)
    self.hoochieBaby.clicked.connect(lambda:toggle(self))

    r+=1
    self.hoochieBabySortLbl=QtWidgets.QLabel(self.lrnStage)
    self.hoochieBabySortLbl.setText(_("      Sort DayLrnQ By:"))
    self.lrnStageGLayout.addWidget(self.hoochieBabySortLbl, r, 0, 1, 1)

    self.hoochieBabySort = QtWidgets.QComboBox(self.lrnStage)
    sort_itms = CUSTOM_SORT.iteritems if ANKI20 else CUSTOM_SORT.items
    for i,v in sort_itms():
        self.hoochieBabySort.addItem(_(""))
        self.hoochieBabySort.setItemText(i, _(v[0]))
    self.lrnStageGLayout.addWidget(self.hoochieBabySort, r, 1, 1, 2)


def load(self, mw):
    qc = self.mw.col.conf
    cb=qc.get("hoochieBaby", 0)
    self.form.hoochieBaby.setCheckState(cb)
    idx=qc.get("hoochieBabySort", 0)
    self.form.hoochieBabySort.setCurrentIndex(idx)
    toggle(self.form)


def save(self):
    toggle(self.form)
    qc = self.mw.col.conf
    qc['hoochieBaby']=self.form.hoochieBaby.checkState()
    qc['hoochieBabySort']=self.form.hoochieBabySort.currentIndex()


def toggle(self):
    checked=self.hoochieBaby.checkState()
    if checked==2:
        try: #no hoochieBaby addon
            if self.muffinTops.checkState():
                self.hoochieBaby.setCheckState(0)
                checked=0
        except: pass

    grayout=False
    if checked==1:
        txt='Hoochie Baby! Randomize DayLrnQ'
    elif checked==2:
        txt='Hoochie Baby! DayLrnQ + QController'
    else:
        grayout=True
        txt='Hoochie Baby! Queue Controller'

    self.hoochieBaby.setText(_(txt))
    self.hoochieBabySort.setDisabled(grayout)
    self.hoochieBabySortLbl.setDisabled(grayout)


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
