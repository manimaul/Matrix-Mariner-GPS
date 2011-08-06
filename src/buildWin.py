#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

from cx_Freeze import setup, Executable
from UserSettings import version as ver
import sys
import os

#python setup.py build
debug = "Console"
release = "Win32GUI"

if sys.platform == 'win32':
    exe = Executable('MMG.py', base=release, icon='rc/mmg.ico')
 
#buildOptions = dict(compressed = True, path = sys.path + ["rc", "icon"])
buildOptions = dict(compressed = True)

 
setup(name='MMG', 
        version = '1.0.5', 
        author = 'Will Kamp', 
        author_email = 'manimaul@gmail.com', 
        url = 'http://matrixmariner.com',
        description = 'GPS Instruments Panel',
        zip_safe = True,
        options = dict(build_exe = buildOptions),
        executables = [exe]
      )

from distutils.dir_util import copy_tree
copy_tree('.//rc', './/build//exe.win32-2.7//rc')
#os.remove('.//build//exe.win32-2.7//rc//linuxlicence.txt')

#Create Nullsoft Installer with appropriate version info
nsi = open('.//nsi.txt', 'r')
nsitxt = nsi.read() %(ver)
nsi.close()

fname = './/build//Installer-%s.nsi' %(ver)
nsi = open(fname, 'w')
nsi.write(nsitxt)
nsi.close
