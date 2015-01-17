#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = 'helljump'

import logging
from PyQt4.QtGui import *
from PyQt4.QtCore import *


log = logging.getLogger(__name__)


class LineEditButton(QWidget):

    clicked = pyqtSignal()

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        layout = QHBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)

        self.button = QToolButton(maximumWidth=22, parent=self)
        self.button.setText("...")
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.setAutoRaise(True)
        self.button.clicked.connect(self.clicked)

        self.edit = QLineEdit(self)

        layout.addWidget(self.edit)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def __getattr__(self, attr):
        try:
            return getattr(self.edit, attr)
        except AttributeError:
            return getattr(self.button, attr)



if __name__ == "__main__":

    import sys

    def test():
        print 'clicked'

    app = QApplication(sys.argv)
    w = LineEditButton()
    w.clicked.connect(test)
    w.show()
    sys.exit(app.exec_())
