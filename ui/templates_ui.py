# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'templates.ui'
#
# Created: Tue Feb 25 16:17:18 2014
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_TemplatesDialog(object):
    def setupUi(self, TemplatesDialog):
        TemplatesDialog.setObjectName(_fromUtf8("TemplatesDialog"))
        TemplatesDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        TemplatesDialog.resize(636, 458)
        self.gridLayout_4 = QtGui.QGridLayout(TemplatesDialog)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.frame_2 = QtGui.QFrame(TemplatesDialog)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.frame_2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.frame_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.name_cb = QtGui.QComboBox(self.frame_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_cb.sizePolicy().hasHeightForWidth())
        self.name_cb.setSizePolicy(sizePolicy)
        self.name_cb.setToolTip(_fromUtf8(""))
        self.name_cb.setInsertPolicy(QtGui.QComboBox.InsertAlphabetically)
        self.name_cb.setMinimumContentsLength(1)
        self.name_cb.setObjectName(_fromUtf8("name_cb"))
        self.gridLayout_2.addWidget(self.name_cb, 0, 1, 1, 1)
        self.reset_tb = QtGui.QToolButton(self.frame_2)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/update.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reset_tb.setIcon(icon)
        self.reset_tb.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        self.reset_tb.setAutoRaise(True)
        self.reset_tb.setObjectName(_fromUtf8("reset_tb"))
        self.gridLayout_2.addWidget(self.reset_tb, 0, 2, 1, 1)
        self.gridLayout_4.addWidget(self.frame_2, 0, 0, 1, 1)
        self.message_te = QtGui.QPlainTextEdit(TemplatesDialog)
        self.message_te.setPlainText(_fromUtf8(""))
        self.message_te.setObjectName(_fromUtf8("message_te"))
        self.gridLayout_4.addWidget(self.message_te, 1, 0, 1, 1)

        self.retranslateUi(TemplatesDialog)
        QtCore.QMetaObject.connectSlotsByName(TemplatesDialog)

    def retranslateUi(self, TemplatesDialog):
        TemplatesDialog.setWindowTitle(QtGui.QApplication.translate("TemplatesDialog", "Шаблоны", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("TemplatesDialog", "Расширение", None, QtGui.QApplication.UnicodeUTF8))
        self.name_cb.setWhatsThis(QtGui.QApplication.translate("TemplatesDialog", "<html><head/><body><p>Для добавления нового шаблона, введите его название и нажмите Enter.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.reset_tb.setToolTip(QtGui.QApplication.translate("TemplatesDialog", "Вернуть к исходному", None, QtGui.QApplication.UnicodeUTF8))
        self.reset_tb.setText(QtGui.QApplication.translate("TemplatesDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.message_te.setWhatsThis(QtGui.QApplication.translate("TemplatesDialog", "<html><head/><body><p>Возможные значения {email}, {firstname}, {lastname}.</p></body></html>", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    TemplatesDialog = QtGui.QDialog()
    ui = Ui_TemplatesDialog()
    ui.setupUi(TemplatesDialog)
    TemplatesDialog.show()
    sys.exit(app.exec_())

