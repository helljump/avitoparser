#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = 'helljump'

import logging
from PyQt4 import QtCore, QtGui
from ui.templates_ui import Ui_TemplatesDialog
import startup
from jinja2 import Environment


log = logging.getLogger(__name__)


templates = [
    ('MS Excel 97 (*.xls)', '.xls', ':/html.tmpl', 'templates/html'),
    ('HTML files (*.html)', '.html', ':/html.tmpl', 'templates/html'),
    ('Text files (*.txt)', '.txt', ':/txt.tmpl', 'templates/txt'),
]


def reset(i=None):
    if i is None:
        r = range(len(templates))
    else:
        r = [i]
    for t in r:
        log.debug('reset %i', t)
        tstr = unicode(QtCore.QResource(templates[t][2]).data(), 'utf8')
        startup.CFG.setValue(templates[t][3], tstr)


if not startup.CFG.contains(templates[0][3]):
    reset()


def render(fname, context):
    env = Environment(extensions=["jinja2.ext.loopcontrols"], cache_size=0, trim_blocks=True,
                      lstrip_blocks=True)
    for t in templates:
        if fname.endswith(t[1]):
            tstr = unicode(startup.CFG.value(t[3]).toString())
            break
    else:
        tstr = unicode(startup.CFG.value(templates[0][3]).toString())
    template = env.from_string(tstr)
    return template.stream(context)


class HighLighter(QtGui.QSyntaxHighlighter):

    def __init__(self, doc):
        super(HighLighter, self).__init__(doc)
        self.color = QtGui.QTextCharFormat()
        self.color.setFontWeight(QtGui.QFont.Bold)
        self.color.setForeground(QtCore.Qt.darkBlue)
        self.expression = QtCore.QRegExp("(\{\{[^>]+\}\})|(\{%[^>]+%\})|(\{#[^>]+#\})")

    def highlightBlock(self, text):
        index = self.expression.indexIn(text)
        while index >= 0:
            length = self.expression.matchedLength()
            self.setFormat(index, length, self.color)
            index = self.expression.indexIn(text, index + length)


class TemplatesDialog(QtGui.QDialog, Ui_TemplatesDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
        log.debug('highlight')
        HighLighter(self.message_te.document())
        if startup.CFG.contains("templates/geometry"):
            self.restoreGeometry(startup.CFG.value("templates/geometry").toByteArray())
        self.current_index = None
        for t in templates:
            self.name_cb.addItem(t[0])

    @QtCore.pyqtSlot()
    def on_reset_tb_clicked(self):
        log.debug('reset')
        i = self.name_cb.currentIndex()
        reset(i)
        tsrt = unicode(startup.CFG.value(templates[i][3]).toString())
        self.message_te.setPlainText(tsrt)

    def save_current(self):
        if self.current_index is not None and self.message_te.document().isModified():
            log.debug('save')
            tstr = unicode(self.message_te.toPlainText())
            startup.CFG.setValue(templates[self.current_index][3], tstr)

    @QtCore.pyqtSlot(int)
    def on_name_cb_currentIndexChanged(self, i):
        log.debug('changed')
        self.save_current()
        tsrt = unicode(startup.CFG.value(templates[i][3]).toString())
        self.message_te.setPlainText(tsrt)
        self.current_index = i

    def closeEvent(self, evt):
        self.save_current()
        startup.CFG.setValue('templates/geometry', self.saveGeometry())
        evt.accept()


if __name__ == '__main__':
    dlg = TemplatesDialog()
    startup.SPLASH.finish(dlg)
    dlg.exec_()
