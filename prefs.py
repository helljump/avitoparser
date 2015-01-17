#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = 'helljump'

import logging

log = logging.getLogger(__name__)


from PyQt4 import QtGui
from PyQt4 import QtCore
from ui.prefs_ui import Ui_PrefsDialog
import startup


class PrefsDialog(QtGui.QDialog, Ui_PrefsDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        if startup.CFG.contains("prefs/geometry"):
            self.restoreGeometry(startup.CFG.value("prefs/geometry").toByteArray())
        egg, rc = startup.CFG.value("prefs/pause", 1).toInt()
        self.pause_sb.setValue(egg)
        egg, rc = startup.CFG.value("prefs/try", 5).toInt()
        self.try_sb.setValue(egg)
        egg = startup.CFG.value("prefs/use_proxy", False).toBool()
        self.proxy_cb.setCheckState(egg and QtCore.Qt.Checked)
        egg = startup.CFG.value('prefs/proxyfile', u'').toString()
        self.proxy_le.setText(egg)
        egg, rc = startup.CFG.value("prefs/threads", 5).toInt()
        self.threads_sb.setValue(egg)
        egg = startup.CFG.value('prefs/imgpath', u'').toString()
        self.imgpath_le.setText(egg)

    @QtCore.pyqtSlot()
    def on_proxy_le_clicked(self):
        log.debug('set proxy')
        fname = QtGui.QFileDialog.getOpenFileName(self, u"Файл прокси", ".", u"Текстовый файл (*.txt)")
        if not fname:
            return
        self.proxy_le.setText(unicode(fname))

    def closeEvent(self, evt):
        startup.CFG.setValue("prefs/pause", self.pause_sb.value())
        startup.CFG.setValue("prefs/try", self.try_sb.value())
        startup.CFG.setValue("prefs/use_proxy", self.proxy_cb.checkState() == QtCore.Qt.Checked)
        startup.CFG.setValue('prefs/proxyfile', unicode(self.proxy_le.text()))
        startup.CFG.setValue("prefs/threads", self.threads_sb.value())
        startup.CFG.setValue("prefs/imgpath", unicode(self.imgpath_le.text()))
        startup.CFG.setValue('prefs/geometry', self.saveGeometry())
        evt.accept()

if __name__ == '__main__':
    dlg = PrefsDialog()
    startup.SPLASH.finish(dlg)
    dlg.exec_()
