#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# cpucat/mainwindow.py: CPUcat主窗口。
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
import os

from cpucat.cpucat_sth import translate as _
from cpucat.cpucat_sth import FRIENDLYNAME, VERSION
from cpucat.cpucat_sth import depcheck
depcheck()

from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL, SLOT

from cpucat.cputab import CPUTab
from cpucat.motherboardtab import MotherboardTab
from cpucat.memorytab import MemoryTab
from cpucat.systemtab import SystemTab

class MainWindow (QWidget):
    def __init__ (self, parent=None):
        QWidget.__init__(self, parent)
        self.setWindowTitle(FRIENDLYNAME)
        self.resize(500, 400)

        if os.getuid() != 0:
            self.warnPerm()

        self.mainLayout = QVBoxLayout(self)
        self.mainTab = QTabWidget()
        self.bottomHBox = QHBoxLayout()

        self.aboutButton = QPushButton(_("About"))
        self.connect(self.aboutButton, SIGNAL("clicked()"),
                        self.showAbout)

        self.quitButton = QPushButton(_("Quit"))
        self.connect(self.quitButton, SIGNAL("clicked()"),
                        qApp, SLOT("quit()"))

        self.mainLayout.addWidget(self.mainTab)
        self.mainLayout.addLayout(self.bottomHBox)

        self.bottomHBox.addStretch(1)
        self.bottomHBox.addWidget(self.aboutButton)
        self.bottomHBox.addWidget(self.quitButton)

        self.tab_init()

    def showAbout (self):
        QMessageBox.about(self, _("About"),
                _("<h2>%s %s</h2>"
                  "An applicaton that shows information<br>"
                  "about CPU and other hardwares."
                 ) % (FRIENDLYNAME, VERSION))

    def warnPerm (self):
        QMessageBox.warning(self, "Warning",
                _("<h2>Root privileges are required "
                  "for getting some infomation.</h2>"
                  "If you want %s to get more detail infomation, "
                  "please use root account to run it. "
                  "It is safe, the applicaion will not damage your system."
                 ) % FRIENDLYNAME)

    def tab_init (self):
        self.tab0 = CPUTab()
        self.mainTab.addTab(self.tab0, _("Processor"))
        self.tab1 = MotherboardTab()
        self.mainTab.addTab(self.tab1, _("Motherboard"))
        self.tab2 = MemoryTab()
        self.mainTab.addTab(self.tab2, _("Memory"))
        self.tab3 = SystemTab()
        self.mainTab.addTab(self.tab3, _("System"))


def main ():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    exit(app.exec_())

if __name__ == "__main__":
    main()
