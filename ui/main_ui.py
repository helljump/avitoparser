# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Tue Feb 25 16:17:16 2014
#      by: PyQt4 UI code generator 4.9.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(913, 705)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.table_tv = QtGui.QTableView(self.centralwidget)
        self.table_tv.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)
        self.table_tv.setAlternatingRowColors(True)
        self.table_tv.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.table_tv.setObjectName(_fromUtf8("table_tv"))
        self.table_tv.horizontalHeader().setMinimumSectionSize(30)
        self.table_tv.horizontalHeader().setStretchLastSection(True)
        self.gridLayout.addWidget(self.table_tv, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setIconSize(QtCore.QSize(32, 32))
        self.toolBar.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.toolBar_4 = QtGui.QToolBar(MainWindow)
        self.toolBar_4.setIconSize(QtCore.QSize(32, 32))
        self.toolBar_4.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBar_4.setObjectName(_fromUtf8("toolBar_4"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar_4)
        self.actionClean = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/cross.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClean.setIcon(icon)
        self.actionClean.setObjectName(_fromUtf8("actionClean"))
        self.actionDelete = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDelete.setIcon(icon1)
        self.actionDelete.setObjectName(_fromUtf8("actionDelete"))
        self.actionAbout = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/aaaa32.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon2)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionStart = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/cog.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/cog_go.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionStart.setIcon(icon3)
        self.actionStart.setObjectName(_fromUtf8("actionStart"))
        self.actionBuy = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/point_gold.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBuy.setIcon(icon4)
        self.actionBuy.setObjectName(_fromUtf8("actionBuy"))
        self.actionSettings = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/setting_tools.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSettings.setIcon(icon5)
        self.actionSettings.setObjectName(_fromUtf8("actionSettings"))
        self.actionExport = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/table_export.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExport.setIcon(icon6)
        self.actionExport.setObjectName(_fromUtf8("actionExport"))
        self.actionTemplates = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/web_template_editor.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionTemplates.setIcon(icon7)
        self.actionTemplates.setObjectName(_fromUtf8("actionTemplates"))
        self.toolBar.addAction(self.actionStart)
        self.toolBar.addAction(self.actionExport)
        self.toolBar.addAction(self.actionClean)
        self.toolBar_4.addAction(self.actionTemplates)
        self.toolBar_4.addAction(self.actionSettings)
        self.toolBar_4.addAction(self.actionBuy)
        self.toolBar_4.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Avito Parser", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Запуск", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar_4.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Помощь", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClean.setText(QtGui.QApplication.translate("MainWindow", "Очистить", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDelete.setText(QtGui.QApplication.translate("MainWindow", "Удалить", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "О программе", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStart.setText(QtGui.QApplication.translate("MainWindow", "Запуск", None, QtGui.QApplication.UnicodeUTF8))
        self.actionBuy.setText(QtGui.QApplication.translate("MainWindow", "Купить", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSettings.setText(QtGui.QApplication.translate("MainWindow", "Настройки", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport.setText(QtGui.QApplication.translate("MainWindow", "Экспорт", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTemplates.setText(QtGui.QApplication.translate("MainWindow", "Шаблоны", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

