#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# cpucat/memorytab.py: CPUcat主窗口中显示内存信息的标签页。
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

def friendly_print (num, unit=""):
    cov = {"":1.0, "K":1024.0, "M":1024.0**2, "G":1024.0**3}

    try:
        num = num * cov[unit]
    except TypeError:
        num = float(num) * cov[unit]

    if num < 8192:
        return "%d Bytes" % num
    elif num < 8192*1024:
        return "%.2f KB" % (num/1024)
    elif num < 8192*1024*1024:
        return "%.2f MB" % (num/1024/1024)
    elif num < 8192*1024*1024*1024:
        return "%.2f GB" % (num/1024/1024/1024)

class memoryinfo:
    def __init__ (self):
        ret, output = getstatusoutput("dmidecode -t memory")
        if ret:
            return

        infos = re.split("\n\n", output)
        ge = infos[1]
        sp = infos[2:]

        self._MaxCapacity = re.findall("Maximum Capacity: (.*)", ge)[0]
        self._NumOfDev = int(re.findall("Number Of Devices: (.*)", ge)[0])
        self._Slot = []

        for item in sp:
            info = {}
            info["Size"] = re.findall("Size: (.*)", item)[0]
            info["Type"] = "%s (%s)" % (re.findall("Type: (.*)", item)[0],
                                re.findall("Type Detail: (.*)", item)[0])
            info["Clock"] = re.findall("Speed: (.*)", item)[0]
            info["Width"] = (re.findall("Total Width: (.*)", item)[0],
                                re.findall("Data Width: (.*)", item)[0])
            self._Slot.append(info)

    def getMaxCapacity (self):
        try:
            return self._MaxCapacity
        except:
            return "N/A"

    def getNumOfDev (self):
        try:
            return self._NumOfDev
        except:
            return 0

    def getType (self, slot):
        try:
            return self._Slot[slot]["Type"]
        except:
            return "N/A"

    def getSize (self, slot):
        try:
            return self._Slot[slot]["Size"]
        except:
            return "N/A"

    def getWidth (self, slot):
        try:
            return self._Slot[slot]["Width"]
        except:
            return "N/A"

    def getClock (self, slot):
        try:
            return self._Slot[slot]["Clock"]
        except:
            return "N/A"

meminfo = memoryinfo()

class GeneralGroup (QGroupBox):
    def __init__ (self, parent=None):
        QGroupBox.__init__(self, _("General"), parent)
        self._Global_grid = QGridLayout(self)

        self._Physical_label = QLabel(_("Physical Memory"))
        self._Global_grid.addWidget(self._Physical_label, 0, 0)
        self._Physical_edit = NEBox()
        self._Global_grid.addWidget(self._Physical_edit, 0, 1)

        self._MaxCap_label = QLabel(_("Maximum Capacity"))
        self._Global_grid.addWidget(self._MaxCap_label, 1, 0)
        self._MaxCap_edit = NEBox()
        self._Global_grid.addWidget(self._MaxCap_edit, 1, 1)

        self._Swap_label = QLabel(_("Swap"))
        self._Global_grid.addWidget(self._Swap_label, 2, 0)
        self._Swap_edit = NEBox()
        self._Global_grid.addWidget(self._Swap_edit, 2, 1)


    def refresh (self):
        fin = open("/proc/meminfo")
        for line in fin:
            if "MemTotal" in line:
                self._Physical_edit.setText(
                        friendly_print(line.split()[1], "K"))
            elif "SwapTotal" in line:
                self._Swap_edit.setText(
                        friendly_print(line.split()[1], "K"))

        self._MaxCap_edit.setText(meminfo.getMaxCapacity())


class DeviceGroup (QGroupBox):
    def __init__ (self, parent=None):
        QGroupBox.__init__(self, _("Device"), parent)
        self._Global_grid = QGridLayout(self)

        self._Slot_label = QLabel(_("Slot"))
        self._Global_grid.addWidget(self._Slot_label, 0, 0)
        self._Slot_combo = QComboBox()
        for i in range(meminfo.getNumOfDev()):
            self._Slot_combo.addItem(_("Slot #%d") % i)
        self.connect(self._Slot_combo, 
                    SIGNAL("currentIndexChanged(int)"),
                    self.changeSlot)
        self._Global_grid.addWidget(self._Slot_combo, 0, 1)

        self._Type_label = QLabel(_("Type"))
        self._Global_grid.addWidget(self._Type_label, 0, 4)
        self._Type_edit = NEBox()
        self._Global_grid.addWidget(self._Type_edit, 0, 5, 1, 4)

        self._Size_label = QLabel(_("Size"))
        self._Global_grid.addWidget(self._Size_label, 1, 0)
        self._Size_edit = NEBox()
        self._Global_grid.addWidget(self._Size_edit, 1, 1, 1, 8)

        self._Clock_label = QLabel(_("Clock"))
        self._Global_grid.addWidget(self._Clock_label, 2, 0)
        self._Clock_edit = NEBox()
        self._Global_grid.addWidget(self._Clock_edit, 2, 1, 1, 8)

        self._TWidth_label = QLabel(_("Total Width"))
        self._Global_grid.addWidget(self._TWidth_label, 3, 0)
        self._TWidth_edit = NEBox()
        self._Global_grid.addWidget(self._TWidth_edit, 3, 1, 1, 3)

        self._DWidth_label = QLabel(_("Data Width"))
        self._Global_grid.addWidget(self._DWidth_label, 3, 5)
        self._DWidth_edit = NEBox()
        self._Global_grid.addWidget(self._DWidth_edit, 3, 6, 1, 3)

    def changeSlot (self, slot):
        self._Type_edit.setText(meminfo.getType(slot))
        self._Size_edit.setText(meminfo.getSize(slot))
        self._Clock_edit.setText(meminfo.getClock(slot))

        width = meminfo.getWidth(slot)
        self._TWidth_edit.setText(width[0])
        self._DWidth_edit.setText(width[1])

    def refresh (self):
        if meminfo.getNumOfDev():
            self.changeSlot(0)

class MemoryTab (QWidget):
    def __init__ (self, parent=None):
        QWidget.__init__(self, parent)
        self._Global_vbox = QVBoxLayout(self)

        self._General_group = GeneralGroup()
        self._Global_vbox.addWidget(self._General_group)

        self._Device_group = DeviceGroup()
        self._Global_vbox.addWidget(self._Device_group)

        self._Global_vbox.addStretch(0)

        self.refresh()

    def refresh (self):
        self._General_group.refresh()
        self._Device_group.refresh()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MemoryTab()
    window.show()
    exit(app.exec_())

