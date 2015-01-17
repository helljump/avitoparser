# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'query.ui'
#
# Created: Tue Feb 25 16:17:17 2014
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_QueryDialog(object):
    def setupUi(self, QueryDialog):
        QueryDialog.setObjectName(_fromUtf8("QueryDialog"))
        QueryDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        QueryDialog.resize(650, 393)
        self.gridLayout = QtGui.QGridLayout(QueryDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.links_te = QtGui.QPlainTextEdit(QueryDialog)
        self.links_te.setObjectName(_fromUtf8("links_te"))
        self.gridLayout.addWidget(self.links_te, 1, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(QueryDialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.label = QtGui.QLabel(QueryDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)

        self.retranslateUi(QueryDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), QueryDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), QueryDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(QueryDialog)

    def retranslateUi(self, QueryDialog):
        QueryDialog.setWindowTitle(QtGui.QApplication.translate("QueryDialog", "Ссылки", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("QueryDialog", "<html><head/><body><p>Укажите построчно ссылки на категории для парсинга. Например: http://www.avito.ru/lipetsk/noutbuki</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    QueryDialog = QtGui.QDialog()
    ui = Ui_QueryDialog()
    ui.setupUi(QueryDialog)
    QueryDialog.show()
    sys.exit(app.exec_())

