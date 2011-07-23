#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# cpucat/cputab.py: CPUcat主窗口中显示系统信息的标签页。
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
import platform
import re
try:
    from subprocess import getstatusoutput
except ImportError:
    from commands import getstatusoutput

from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL, SLOT, PYQT_VERSION_STR, qVersion

from cpucat.cpucat_sth import translate as _
from cpucat.cputab import NEBox

def getXorgVersion ():
    command = getstatusoutput("Xorg -version")
    try:
        return re.findall("X\.Org X Server (.*)", command[1])[0]
    except Exception:
        return "N/A"

def getGCCVersion ():
    command = getstatusoutput("gcc --version")
    try:
        return re.findall("gcc \(GCC\) (.*)", command[1])[0]
    except Exception:
        return "N/A"


class OSGroup (QGroupBox):
    def __init__ (self, parent=None):
        QGroupBox.__init__(self, _("Operating System"), parent)
        self._Global_grid = QGridLayout(self)

        self._Arch_label = QLabel(_("Architecture"))
        self._Global_grid.addWidget(self._Arch_label, 0, 0)
        self._Arch_edit = NEBox()
        self._Global_grid.addWidget(self._Arch_edit, 0, 1)

        self._Kernel_label = QLabel(_("Kernel"))
        self._Global_grid.addWidget(self._Kernel_label, 1, 0)
        self._Kernel_edit = NEBox()
        self._Global_grid.addWidget(self._Kernel_edit, 1, 1)

        self._Dist_label = QLabel(_("Distribution"))
        self._Global_grid.addWidget(self._Dist_label, 2, 0)
        self._Dist_edit = NEBox()
        self._Global_grid.addWidget(self._Dist_edit, 2, 1)

        self._ComputerName_label = QLabel(_("Computer Name"))
        self._Global_grid.addWidget(self._ComputerName_label, 3, 0)
        self._ComputerName_edit = NEBox()
        self._Global_grid.addWidget(self._ComputerName_edit, 3, 1)

        self._libcVersion_label = QLabel(_("C Library"))
        self._Global_grid.addWidget(self._libcVersion_label, 4, 0)
        self._libcVersion_edit = NEBox()
        self._Global_grid.addWidget(self._libcVersion_edit, 4, 1)

        self._GCCVersion_label = QLabel(_("GCC Version"))
        self._Global_grid.addWidget(self._GCCVersion_label, 5, 0)
        self._GCCVersion_edit = NEBox()
        self._Global_grid.addWidget(self._GCCVersion_edit, 5, 1)

        self._XVersion_label = QLabel(_("Xorg Version"))
        self._Global_grid.addWidget(self._XVersion_label, 6, 0)
        self._XVersion_edit = NEBox()
        self._Global_grid.addWidget(self._XVersion_edit, 6, 1)

        self._QtVersion_label = QLabel(_("Qt4 Version"))
        self._Global_grid.addWidget(self._QtVersion_label, 7, 0)
        self._QtVersion_edit = NEBox()
        self._Global_grid.addWidget(self._QtVersion_edit, 7, 1)

    def refresh (self):
        self._Arch_edit.setText(platform.machine())
        self._Kernel_edit.setText("%s %s" % \
                (platform.system(), platform.release()))
        self._Dist_edit.setText(" ".join(platform.linux_distribution()))
        self._ComputerName_edit.setText(platform.node())
        self._libcVersion_edit.setText(" ".join(platform.libc_ver()))
        self._GCCVersion_edit.setText(getGCCVersion())
        self._XVersion_edit.setText(getXorgVersion())
        self._QtVersion_edit.setText(qVersion())

class PythonGroup (QGroupBox):
    def __init__ (self, parent=None):
        QGroupBox.__init__(self, _("Python"), parent)
        self._Global_grid = QGridLayout(self)

        self._Implementation_label = QLabel(_("Implementation"))
        self._Global_grid.addWidget(self._Implementation_label, 0, 0)
        self._Implementation_edit = NEBox()
        self._Global_grid.addWidget(self._Implementation_edit, 0, 1)

        self._Version_label = QLabel(_("Version"))
        self._Global_grid.addWidget(self._Version_label, 1, 0)
        self._Version_edit = NEBox()
        self._Global_grid.addWidget(self._Version_edit, 1, 1)

        self._PyQtVersion_label = QLabel(_("PyQt4 Version"))
        self._Global_grid.addWidget(self._PyQtVersion_label, 2, 0)
        self._PyQtVersion_edit = NEBox()
        self._Global_grid.addWidget(self._PyQtVersion_edit, 2, 1)

    def refresh (self):
        self._Implementation_edit.setText(platform.python_implementation())
        self._Version_edit.setText(platform.python_version())
        self._PyQtVersion_edit.setText(PYQT_VERSION_STR)

class SystemTab (QWidget):
    def __init__ (self, parent=None):
        QWidget.__init__(self, parent)

        self._Global_vbox = QVBoxLayout(self)

        self._OS_group = OSGroup()
        self._Global_vbox.addWidget(self._OS_group)

        self._Python_group = PythonGroup()
        self._Global_vbox.addWidget(self._Python_group)

        self._Global_vbox.addStretch(0)

        self.refresh()

    def refresh (self):
        self._Python_group.refresh()
        self._OS_group.refresh()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SystemTab()
    window.show()
    exit(app.exec_())

