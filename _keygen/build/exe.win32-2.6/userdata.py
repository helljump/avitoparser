#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = 'helljump'


from PyQt4 import QtCore
from codecs import open
from persistent.dict import PersistentDict
#from helpers import get_md5


def demo_export(self, fname, env, firms):
    with open(fname, 'w', 'utf-8') as fout:
        ext = fname.split('.')[-1]
        template = env.get_template('%s.tmpl' % ext)
        text = template.render({'items': firms})
        fout.write(text)


def addItem(self, item):
    egg = len(self._data)
    h = get_md5(item, None)
    if h in self._hash:
        return egg
    self.beginInsertRows(QtCore.QModelIndex(), egg, egg)
    v = PersistentDict(item)
    self._data.append(v)
    self._hash.insert(h)
    self.endInsertRows()
    return egg


def myfilter(params):
    pass

