#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# cpucat/cpucat_sth.py: CPUcat杂项。
# This file is part of CPUcat.
#
# CPUcat
# 类似Windows下CPU-Z的获取CPU和其他硬件信息的工具。
# Copyright (C) 2011  CUI Hao
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author: 崔灏 (CUI Hao)
# Email: cuihao.leo@gmail.com
##

PACKAGE="cpucat"
FRIENDLYNAME="CPUcat"
VERSION="0.001"

try:
    import gettext
except ImportError:
    translate = lambda x: x
else:
    gettext.bindtextdomain(PACKAGE, "./locale")
    gettext.textdomain(PACKAGE)
    translate = gettext.gettext

_ = translate
import sys

def depcheck ():
    try:
        import PyQt4
    except ImportError:
        sys.stderr.write(_("Please install PyQt4 first.\n"))
        exit(1)

    try:
        import dmidecode
    except ImportError:
        sys.stderr.write(_("Python module 'dmidecode' not found. "\
                           "Some infomation may be ignored.\n"))

    def check_lscpu ():
        import os
        for p in os.environ["PATH"].split(os.pathsep):
            fpath = os.path.join(p, "lscpu")
            if os.path.exists(fpath) and os.access(fpath, os.X_OK):
                return True
        return False

    if not check_lscpu():
        sys.stderr.write(_("The 'lscpu' command not found. "\
                           "Some infomation may be ignored.\n"))

