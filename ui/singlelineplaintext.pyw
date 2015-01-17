#!/usr/bin/env python
#-*- coding: UTF-8 -*-


__author__ = "helljump"


from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt


class SingleLinePlainText(QtGui.QPlainTextEdit):

    def __init__(self, parent=None):
        super(SingleLinePlainText, self).__init__(parent)
        self.setTabChangesFocus(True)
        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        self.setFixedHeight(self.sizeHint().height())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            event.ignore()
        else:
            QtGui.QPlainTextEdit.keyPressEvent(self, event)

    def sizeHint(self):
        fm = QtGui.QFontMetrics(self.font())
        h = max(fm.height(), 14) + 4
        w = fm.width(QtCore.QChar('x')) * 17 + 4
        opt = QtGui.QStyleOptionFrameV2()
        opt.initFrom(self)
        return self.style().sizeFromContents(QtGui.QStyle.CT_LineEdit, opt,
            QtCore.QSize(w, h).expandedTo(QtGui.QApplication.globalStrut()), self)


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    w = SingleLinePlainText()
    w.show()
    sys.exit(app.exec_())
