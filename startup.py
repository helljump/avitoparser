#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = "helljump"


APPNAME = 'avito-parser'


from PyQt4 import QtCore
from PyQt4 import QtGui
from ui import icons_rc  # noqa
import sys


app = QtGui.QApplication(sys.argv)
app.setWindowIcon(QtGui.QIcon(':/aaaa32.png'))


class MySplash(QtGui.QSplashScreen):
    def __init__(self):
        pm = QtGui.QPixmap(":/aaaa.png")
        super(MySplash, self).__init__(pm)

    def message(self, s):
        self.showMessage(s, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop, QtCore.Qt.white)
        QtGui.qApp.processEvents()


SPLASH = MySplash()
SPLASH.show()
SPLASH.message(u'Инициализация')


import logging
import logging.handlers
import os
import atexit
from ZODB.FileStorage import FileStorage
from ZODB.DB import DB as ZDB


from Crypto.Hash import SHA
import win32api
import marshal
from Crypto.Cipher import Blowfish
import types
hash = SHA.new()
d, p = os.path.splitdrive(win32api.GetSystemDirectory())
hash.update(str(win32api.GetSystemInfo()))
hash.update(APPNAME)
hash.update(str(win32api.GetVolumeInformation(d + '/')))
HWINFO = hash.hexdigest()
cipher = Blowfish.new(HWINFO)


egg = os.path.expanduser('~/' + APPNAME)
HOMEDIR = unicode(egg, encoding=sys.getfilesystemencoding())
if not os.path.isdir(HOMEDIR):
    os.mkdir(HOMEDIR)


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(module)s: %(message)s")
logname = os.path.expanduser(os.path.join(HOMEDIR, APPNAME + '.log'))
handler1 = logging.handlers.RotatingFileHandler(logname, maxBytes=100000, backupCount=2)
handler1.setFormatter(formatter)
logger.addHandler(handler1)
if not hasattr(sys, "frozen"):
    handler2 = logging.StreamHandler(sys.stdout)
    handler2.setFormatter(formatter)
    logger.addHandler(handler2)
log = logging.getLogger(__name__)

CFG = QtCore.QSettings('zipta.ru', APPNAME)


SPLASH.message(u'Оптимизируем базу')


storage = FileStorage(os.path.join(HOMEDIR, 'db'), blob_dir=os.path.join(HOMEDIR, 'blobs'))
DB = ZDB(storage)
DB.pack(days=3)


def zodbclose():
    DB.close()
    storage.close()

atexit.register(zodbclose)

'''
# пример замены метода
try:
    u = __import__('userdata')
    model.add_item = types.MethodType(u.add_item, model)
except ImportError:
    pass
'''
try:
    finp = os.path.join(HOMEDIR, 'userdata.pye')
    if os.path.isfile(finp):
        enc = open(finp, 'rb').read()
        data = cipher.decrypt(enc)
        m = types.ModuleType('userdata')
        sys.modules['userdata'] = m
        code = marshal.loads(data)
        exec code in m.__dict__
        log.debug('ok')
except:
    log.exception('ohh')

SPLASH.message(u'Запуск интерфейса')

