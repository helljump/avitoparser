#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = 'helljump'

import logging
from PyQt4 import QtGui
import startup
from ui.query_ui import Ui_QueryDialog
import sys


log = logging.getLogger(__name__)


class QueryDialog(QtGui.QDialog, Ui_QueryDialog):
    def __init__(self, parent=None):
        super(QueryDialog, self).__init__(parent)
        self.setupUi(self)
        if startup.CFG.contains("query/geometry"):
            self.restoreGeometry(startup.CFG.value("query/geometry").toByteArray())
        if not hasattr(sys, "frozen"):
            self.links_te.setPlainText('http://www.avito.ru/lipetsk/chasy_i_ukrasheniya/yuvelirnye_izdeliya\n')

    def closeEvent(self, evt):
        startup.CFG.setValue('query/geometry', self.saveGeometry())
        evt.accept()

    def accept(self):
        if self.get_links():
            super(QueryDialog, self).accept()
        else:
            QtGui.QMessageBox.information(self, u'Парсинг', u'Укажите список ссылок для обработки.')

    def get_links(self):
        return [l for l in unicode(self.links_te.toPlainText()).split('\n') if l.strip()]


if __name__ == '__main__':
    dlg = QueryDialog()
    startup.SPLASH.finish(dlg)
    dlg.exec_()
