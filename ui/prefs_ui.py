# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prefs.ui'
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

class Ui_PrefsDialog(object):
    def setupUi(self, PrefsDialog):
        PrefsDialog.setObjectName(_fromUtf8("PrefsDialog"))
        PrefsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        PrefsDialog.resize(549, 203)
        self.gridLayout = QtGui.QGridLayout(PrefsDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.try_sb = QtGui.QSpinBox(PrefsDialog)
        self.try_sb.setMaximumSize(QtCore.QSize(102, 16777215))
        self.try_sb.setMinimum(1)
        self.try_sb.setProperty("value", 5)
        self.try_sb.setObjectName(_fromUtf8("try_sb"))
        self.gridLayout.addWidget(self.try_sb, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(PrefsDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.threads_sb = QtGui.QSpinBox(PrefsDialog)
        self.threads_sb.setMaximumSize(QtCore.QSize(102, 16777215))
        self.threads_sb.setMinimum(1)
        self.threads_sb.setProperty("value", 5)
        self.threads_sb.setObjectName(_fromUtf8("threads_sb"))
        self.gridLayout.addWidget(self.threads_sb, 2, 1, 1, 1)
        self.pause_sb = QtGui.QSpinBox(PrefsDialog)
        self.pause_sb.setMaximumSize(QtCore.QSize(102, 16777215))
        self.pause_sb.setProperty("value", 1)
        self.pause_sb.setObjectName(_fromUtf8("pause_sb"))
        self.gridLayout.addWidget(self.pause_sb, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(PrefsDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.proxy_cb = QtGui.QCheckBox(PrefsDialog)
        self.proxy_cb.setObjectName(_fromUtf8("proxy_cb"))
        self.gridLayout.addWidget(self.proxy_cb, 4, 0, 1, 1)
        self.label = QtGui.QLabel(PrefsDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.proxy_le = LineEditButton(PrefsDialog)
        self.proxy_le.setEnabled(False)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/page.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.proxy_le.setIcon(icon)
        self.proxy_le.setObjectName(_fromUtf8("proxy_le"))
        self.gridLayout.addWidget(self.proxy_le, 4, 1, 1, 1)
        self.label_4 = QtGui.QLabel(PrefsDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.imgpath_le = QtGui.QLineEdit(PrefsDialog)
        self.imgpath_le.setObjectName(_fromUtf8("imgpath_le"))
        self.gridLayout.addWidget(self.imgpath_le, 3, 1, 1, 1)

        self.retranslateUi(PrefsDialog)
        QtCore.QObject.connect(self.proxy_cb, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.proxy_le.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(PrefsDialog)
        PrefsDialog.setTabOrder(self.pause_sb, self.try_sb)
        PrefsDialog.setTabOrder(self.try_sb, self.threads_sb)
        PrefsDialog.setTabOrder(self.threads_sb, self.imgpath_le)
        PrefsDialog.setTabOrder(self.imgpath_le, self.proxy_cb)

    def retranslateUi(self, PrefsDialog):
        PrefsDialog.setWindowTitle(QtGui.QApplication.translate("PrefsDialog", "Настройки", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("PrefsDialog", "Потоков", None, QtGui.QApplication.UnicodeUTF8))
        self.pause_sb.setSuffix(QtGui.QApplication.translate("PrefsDialog", " сек.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("PrefsDialog", "Количество попыток", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_cb.setText(QtGui.QApplication.translate("PrefsDialog", "Использовать прокси", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("PrefsDialog", "Паузы между запросами", None, QtGui.QApplication.UnicodeUTF8))
        self.proxy_le.setPlaceholderText(QtGui.QApplication.translate("PrefsDialog", "файл прокси", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("PrefsDialog", "Путь экспорта изображений", None, QtGui.QApplication.UnicodeUTF8))
        self.imgpath_le.setText(QtGui.QApplication.translate("PrefsDialog", "images/", None, QtGui.QApplication.UnicodeUTF8))

from lineeditbutton import LineEditButton
import icons_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    PrefsDialog = QtGui.QDialog()
    ui = Ui_PrefsDialog()
    ui.setupUi(PrefsDialog)
    PrefsDialog.show()
    sys.exit(app.exec_())

