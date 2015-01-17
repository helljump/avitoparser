#!/usr/bin/env python
#-*- coding: UTF-8 -*-

__author__ = 'helljump'

from cx_Freeze import setup, Executable
from time import gmtime, strftime


base = None


setup(
    name='kg',
    version='1.0.0.0',
    executables=[Executable('keygen.py', base=base)]
)
