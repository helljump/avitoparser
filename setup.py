#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = 'helljump'

from cx_Freeze import setup, Executable
from time import gmtime, strftime


base = 'Win32GUI'
ver = strftime("%y.%m.%d.%H%M", gmtime())


setup(
    name='zipta avito parser',
    description='zipta avito parser by helljump',
    version=ver,
    options={'build_exe': {
        'includes': ['lxml._elementpath', 'gzip', 'jinja2.ext', 'grab.transport.curl', 'persistent.dict'],
        'excludes': ['userdata'],
        'optimize': 2,
        'silent': True,
        'copy_dependent_files': True,
        'include_files': [
            ('tessdata', 'tessdata'),
            ('docs', 'docs'),
            (r'c:\Python26\Lib\site-packages\PyQt4\translations\qt_ru.qm', 'qt_ru.qm'),
        ],
    }},
    executables=[Executable('main.py', base=base, icon="aaaa32.ico", targetName="avitoparser.exe")]
)
