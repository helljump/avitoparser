#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = 'helljump'


SOFT_ID = 'avito-parser'


import win32api
import marshal
from Crypto.Cipher import Blowfish
from Crypto.Hash import SHA
from struct import pack
import os
import types
import sys
import py_compile


'''

hash = SHA.new()
d, p = splitdrive(win32api.GetSystemDirectory())
hash.update(str(win32api.GetSystemInfo()))
hash.update('2gis_parser3')
hash.update(str(win32api.GetVolumeInformation(d+'\\')))
self.tralyalya = hash.hexdigest()
cipher = Blowfish.new(self.tralyalya)

try:
    m = open(join(config.ROOT, 'userdata.pye'), 'rb').read()
    b = cipher.decrypt(m)
    c = marshal.loads(b)
    f = types.FunctionType(c, globals())
    self.demo_export = types.MethodType(f, self)
except (IOError, ValueError):
    pass



'''


def gen_key():
    hash = SHA.new()
    d, p = os.path.splitdrive(win32api.GetSystemDirectory())
    hash.update(str(win32api.GetSystemInfo()))
    hash.update(SOFT_ID)
    hash.update(str(win32api.GetVolumeInformation(d + '/')))
    return hash.hexdigest()


def encrypt(key, data):
    cipher = Blowfish.new(key)
    plen = Blowfish.block_size - divmod(len(data), Blowfish.block_size)[1]
    padding = [plen]*plen
    padding = pack('b'*plen, *padding)
    return cipher.encrypt(data + padding)


def encode(key=None):
    py_compile.compile('userdata.py')
    data = open('userdata.pyc', 'rb').read()
    if key is None:
        key = gen_key()
    enc = encrypt(key, data[8:])
    open('userdata.pye', 'wb').write(enc)


def test(key):
    cipher = Blowfish.new(key)
    enc = open('userdata.pye', 'rb').read()
    data = cipher.decrypt(enc)
    m = types.ModuleType('userdata')
    sys.modules['userdata'] = m
    code = marshal.loads(data)
    exec code in m.__dict__


if __name__ == '__main__':
    hwinfo = raw_input('enter hw info:')
    if not hwinfo:
        hwinfo = gen_key()
    print 'hwinfo:', hwinfo
    encode(hwinfo)
    raw_input('done')

    #test(gen_key())
    #import userdata
    #print userdata.get_text('ewf piidc oi              wifdb sdfv')
    #userdata.simple()
