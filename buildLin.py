#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2010 by Will Kamp <manimaul!gmail.com>

import os
from distutils.dir_util import copy_tree
import shutil
from UserSettings import version as ver

shutil.rmtree('./build/DEB')
os.makedirs('./build/DEB/DEBIAN')
os.makedirs('./build/DEB/usr/bin')
os.makedirs('./build/DEB/usr/lib/mmgps')
os.makedirs('./build/DEB/usr/share/fonts/truetype/mmgps')
os.makedirs('./build/DEB/usr/share/applications')
os.makedirs('./build/DEB/usr/share/mmgps')

copy_tree('./rc', './build/DEB/usr/lib/mmgps/rc')
os.remove('./build/DEB/usr/lib/mmgps/rc/windowslicense.txt')
shutil.rmtree('./build/DEB/usr/lib/mmgps/rc/SetupVSPE')


shutil.move('./build/DEB/usr/lib/mmgps/rc/LCDDotMatrix5x8.ttf', './build/DEB/usr/share/fonts/truetype/mmgps')
shutil.copyfile('./icon/mmg-icon.png', './build/DEB/usr/share/mmgps/mmgps.png')

shutil.copy('./getIPlin.py', './build/DEB/usr/lib/mmgps')
shutil.copy('./Gpscom.py', './build/DEB/usr/lib/mmgps')
shutil.copy('./GUI.py', './build/DEB/usr/lib/mmgps')
shutil.copy('./Kml.py', './build/DEB/usr/lib/mmgps')
shutil.copy('./kmlControl.py', './build/DEB/usr/lib/mmgps')
shutil.copy('./RecordGps.py', './build/DEB/usr/lib/mmgps')
shutil.copy('./scanLin.py', './build/DEB/usr/lib/mmgps')
shutil.copy('./Tcp.py', './build/DEB/usr/lib/mmgps')
shutil.copy('./UserSettings.py', './build/DEB/usr/lib/mmgps')
shutil.copy('./VSPLin.py', './build/DEB/usr/lib/mmgps')
shutil.copy('./MMG.py', './build/DEB/usr/lib/mmgps')
shutil.copy('./instance.py', './build/DEB/usr/lib/mmgps')

cf = open('./build/DEB/DEBIAN/control', 'w')
control = '\
Package: MMG \n\
Version: %s \n\
Section: utils \n\
Priority: optional \n\
Architecture: all \n\
Depends: python-wxgtk2.8 (>= 2.8.7.1-0ubuntu3), python-serial (>=2.3-1) \n\
Installed-Size: \n\
Maintainer: Will Kamp <manimaul@gmail.com> \n\
Conflicts: \n\
Replaces: Gippy\n\
Description: GPS instruments panel in python\n' %(ver)
cf.write(control)
cf.close()

df = open('./build/DEB/usr/share/applications/mmgps.desktop', 'w')
dtxt = '\
#!/usr/bin/env xdg-open\n\n\
[Desktop Entry]\n\
Version=1.0\n\
Type=Application\n\
Terminal=false\n\
Icon=/usr/share/mmgps/mmgps.png\n\
Name=Matrix Mariner GPS\n\
Exec=mmgps\n\
Comment=GPS Instruments Panel\n\
Name=Matrix Mariner GPS\n\
Comment=GPS Instruments Panel\n\
Icon=/usr/share/mmgps/mmgps.png'

df.write(dtxt)
df.close()

binf = open('./build/DEB/usr/bin/mmgps', 'w')
bintxt = '\
#!/bin/bash \n\
cd /usr/lib/mmgps \n\
python MMG.py'
binf.write(bintxt)
binf.close()

os.chmod('./build/DEB/usr/bin/mmgps', 0777)


