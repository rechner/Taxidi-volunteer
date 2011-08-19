#!/usr/bin/env python
#-*- coding:utf-8 -*-

#read/write config values to config.ini
#Note: the if not os.path.exists(inifile) routine probably isn't a
# good idea.  I smell race conditions...

import os, sys
import configobj

appPath = os.path.abspath(os.path.dirname(os.path.join(sys.argv[0])))
inifile = os.path.join(appPath, 'config.ini')

def create():
	config = configobj.ConfigObj()
	config.fileName = inifile
	config['fullScren'] = False
	config['windowX'] = 2010
	config['windowY'] = 720
	config['banner'] = 'resources/banner.png'
	config['backgroundColour'] = '#E3D2B4'
	config['password'] = False
	conifg['hash'] = '0d890f617f6b897a3998b9f92138b70fda10a332'
	config.write()

def get():
    if not os.path.exists(inifile):
        create()
    return configobj.ConfigObj(inifile)
