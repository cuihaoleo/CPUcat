#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# cpucat/motherboard.py: CPUcat主窗口中显示主板信息的标签页。
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

import sys
import glob
import re
try:
    from subprocess import getstatusoutput
except ImportError:
    from commands import getstatusoutput

from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL, SLOT

from cpucat.cpucat_sth import translate as _
from cpucat.cputab import NEBox

def getMoboInfo (what):
    try:
        return open("/sys/devices/virtual/dmi/id/%s" % what) \
                .read().strip()
    except:
        return "N/A"

class MotherboardGroup (QGroupBox):
    def __init__ (self, parent=None):
        QGroupBox.__init__(self, _("Motherboard"), parent)
        self._Global_grid = QGridLayout(self)

        self._Vendor_label = QLabel(_("Vendor"))
        self._Global_grid.addWidget(self._Vendor_label, 0, 0)
        self._Vendor_edit = NEBox()
        self._Global_grid.addWidget(self._Vendor_edit, 0, 1, 1, 8)

        self._Model_label = QLabel(_("Model"))
        self._Global_grid.addWidget(self._Model_label, 1, 0)
        self._Model_edit = NEBox()
        self._Global_grid.addWidget(self._Model_edit, 1, 1, 1, 5)
        self._Version_edit = NEBox()
        self._Global_grid.addWidget(self._Version_edit, 1, 6, 1, 3)

        self._Serial_label = QLabel(_("Serial"))
        self._Global_grid.addWidget(self._Serial_label, 2, 0)
        self._Serial_edit = NEBox()
        self._Global_grid.addWidget(self._Serial_edit, 2, 1, 1, 8)

    def refresh (self):
        self._Vendor_edit.setText(getMoboInfo("board_vendor"))
        self._Model_edit.setText(getMoboInfo("board_name"))
        self._Version_edit.setText(getMoboInfo("board_version"))
        self._Serial_edit.setText(getMoboInfo("board_serial"))


class BIOSGroup (QGroupBox):
    def __init__ (self, parent=None):
        QGroupBox.__init__(self, _("BIOS"), parent)
        self._Global_grid = QGridLayout(self)

        self._Vendor_label = QLabel(_("Vendor"))
        self._Global_grid.addWidget(self._Vendor_label, 0, 0)
        self._Vendor_edit = NEBox()
        self._Global_grid.addWidget(self._Vendor_edit, 0, 1)

        self._Version_label = QLabel(_("Version"))
        self._Global_grid.addWidget(self._Version_label, 1, 0)
        self._Version_edit = NEBox()
        self._Global_grid.addWidget(self._Version_edit, 1, 1)

        self._Date_label = QLabel(_("Date"))
        self._Global_grid.addWidget(self._Date_label, 2, 0)
        self._Date_edit = NEBox()
        self._Global_grid.addWidget(self._Date_edit, 2, 1)

    def refresh (self):
        self._Vendor_edit.setText(getMoboInfo("bios_vendor"))
        self._Version_edit.setText(getMoboInfo("bios_version"))
        self._Date_edit.setText(getMoboInfo("bios_date"))

class MotherboardTab (QWidget):
    def __init__ (self, parent=None):
        QWidget.__init__(self, parent)
        self._Global_vbox = QVBoxLayout(self)

        self._Mobo_group = MotherboardGroup()
        self._Global_vbox.addWidget(self._Mobo_group)

        self._BIOS_group = BIOSGroup()
        self._Global_vbox.addWidget(self._BIOS_group)

        self._Global_vbox.addStretch(0)

        self.refresh()

    def refresh (self):
        self._Mobo_group.refresh()
        self._BIOS_group.refresh()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MotherboardTab()
    window.show()
    exit(app.exec_())

