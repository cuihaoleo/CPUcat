#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# cpucat/cputab.py: CPUcat主窗口中显示CPU信息的标签页。
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

import os
import sys
import glob

from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL, SLOT

from cpucat.cpucat_sth import translate as _
import cpuinfo

def whichlogo (cpu):
    basepath = os.path.split(__file__)[0]
    if cpu.isAMD():
        return os.path.join(basepath, "logos", "amd.png")
    if cpu.isIntel():
        return os.path.join(basepath, "logos", "intel.png")

class NEBox (QLineEdit):
    def __init__ (self, parent=None):
        QLineEdit.__init__(self, parent)
        self.setReadOnly(True)

class ProcessorGroup (QGroupBox):
    def __init__ (self, parent=None):
        QGroupBox.__init__(self, _("Processor"), parent)
        self._Global_grid = QGridLayout(self)

        self._VendorID_label = QLabel(_("Vendor ID"))
        self._Global_grid.addWidget(self._VendorID_label, 0, 0)
        self._VendorID_edit = NEBox()
        self._Global_grid.addWidget(self._VendorID_edit, 0, 1, 1, 3)

        self._ModelName_label = QLabel(_("Model Name"))
        self._Global_grid.addWidget(self._ModelName_label, 1, 0)
        self._ModelName_edit = NEBox()
        self._Global_grid.addWidget(self._ModelName_edit, 1, 1, 1, 3)

        self._Logo_label = QLabel()
        self._Global_grid.addWidget(self._Logo_label, 0, 4, 3, 2)

        self._Slot_label = QLabel(_("Slot"))
        self._Global_grid.addWidget(self._Slot_label, 2, 0)
        self._Slot_edit = NEBox()
        self._Global_grid.addWidget(self._Slot_edit, 2, 1)
        
        self._OpMode_label = QLabel(_("Op-Mode"))
        self._Global_grid.addWidget(self._OpMode_label, 2, 2)
        self._OpMode_edit = NEBox()
        self._Global_grid.addWidget(self._OpMode_edit, 2, 3)

        self._Sub1_hbox = QHBoxLayout()
        self._Global_grid.addLayout(self._Sub1_hbox, 3, 0, 1, 5)

        self._Family_label = QLabel(_("Family"))
        self._Sub1_hbox.addWidget(self._Family_label)
        self._Family_edit = NEBox()
        self._Sub1_hbox.addWidget(self._Family_edit)

        self._Model_label = QLabel(_("Model"))
        self._Sub1_hbox.addWidget(self._Model_label)
        self._Model_edit = NEBox()
        self._Sub1_hbox.addWidget(self._Model_edit)

        self._Stepping_label = QLabel(_("Stepping"))
        self._Sub1_hbox.addWidget(self._Stepping_label)
        self._Stepping_edit = NEBox()
        self._Sub1_hbox.addWidget(self._Stepping_edit)

        self._Sub2_hbox = QHBoxLayout()
        self._Global_grid.addLayout(self._Sub2_hbox, 4, 0, 1, 5)

        self._ExtFamily_label = QLabel(_("Ext. Family"))
        self._Sub2_hbox.addWidget(self._ExtFamily_label)
        self._ExtFamily_edit = NEBox()
        self._Sub2_hbox.addWidget(self._ExtFamily_edit)

        self._ExtModel_label = QLabel(_("Ext. Model"))
        self._Sub2_hbox.addWidget(self._ExtModel_label)
        self._ExtModel_edit = NEBox()
        self._Sub2_hbox.addWidget(self._ExtModel_edit)

        self._BogoMIPS_label = QLabel(_("BogoMIPS"))
        self._Sub2_hbox.addWidget(self._BogoMIPS_label)
        self._BogoMIPS_edit = NEBox()
        self._Sub2_hbox.addWidget(self._BogoMIPS_edit)

        self._Instruction_label = QLabel(_("Inst. Set"))
        self._Global_grid.addWidget(self._Instruction_label, 5, 0)
        self._Instruction_edit = NEBox()
        self._Global_grid.addWidget(self._Instruction_edit, 5, 1, 1, 5)

    def refresh_cpuinfo (self, info):
        self._VendorID_edit.setText(
                info.getModelInfo().get("VendorID", ""))
        self._ModelName_edit.setText(
                info.getModelInfo().get("BrandStr", ""))
        self._Logo_label.setPixmap(
                QPixmap(whichlogo(info)))
        self._Slot_edit.setText(
                info.getSlot())
        self._OpMode_edit.setText(
                " ".join(info.getOpMode()))
        self._Family_edit.setText(
                "%X" % info.getModelInfo().get("Family", 0))
        self._Model_edit.setText(
                "%X" % info.getModelInfo().get("Model", 0))
        self._Stepping_edit.setText(
                "%X" % info.getModelInfo().get("Stepping", 0))
        self._ExtFamily_edit.setText(
                "%02X" % info.getModelInfo().get("ExtFamily", 0))
        self._ExtModel_edit.setText(
                "%X" % info.getModelInfo().get("ExtModel", 0))
        self._BogoMIPS_edit.setText(
                "%.2f" % info.getBogoMIPS())
        self._Instruction_edit.setText(
                " ".join(info.MMX_3DNow_support() +
                         info.SSE_support() +
                         info.x86Virt_support() +
                         (["AES"] if info.AES_ifsupport() else [])))

class ClockGroup (QGroupBox):
    def __init__ (self, parent=None):
        QGroupBox.__init__(self, _("Clock"), parent)
        self._Global_grid = QGridLayout(self)

        self._SpeedReal_label = QLabel(_("Speed (Real)"))
        self._Global_grid.addWidget(self._SpeedReal_label, 0, 0)
        self._SpeedReal_edit = NEBox()
        self._Global_grid.addWidget(self._SpeedReal_edit, 0, 1)

        self._SpeedBIOS_label = QLabel(_("Speed (BIOS)"))
        self._Global_grid.addWidget(self._SpeedBIOS_label, 1, 0)
        self._SpeedBIOS_edit = NEBox()
        self._Global_grid.addWidget(self._SpeedBIOS_edit, 1, 1)

        self._Multiplier_label = QLabel(_("Multiplier"))
        self._Global_grid.addWidget(self._Multiplier_label, 2, 0)
        self._Multiplier_edit = NEBox()
        self._Global_grid.addWidget(self._Multiplier_edit, 2, 1)

        self._ExtClock_label = QLabel(_("Ext. Clock"))
        self._Global_grid.addWidget(self._ExtClock_label, 3, 0)
        self._ExtClock_edit = NEBox()
        self._Global_grid.addWidget(self._ExtClock_edit, 3, 1)

    def refresh_cpuinfo (self, info):
        self._SpeedReal_edit.setText(info.getCurrentSpeed())
        sinfo = info.getBIOSSpeedInfo()
        self._SpeedBIOS_edit.setText(sinfo["SpeedBIOS"])
        self._Multiplier_edit.setText(sinfo["Multiplier"])
        self._ExtClock_edit.setText(sinfo["ExternalClock"])

class CacheGroup (QGroupBox):
    def __init__ (self, parent=None):
        QGroupBox.__init__(self, _("Cache"), parent)
        self._Global_grid = QGridLayout(self)

        self._L1Data_label = QLabel(_("L1 Data"))
        self._Global_grid.addWidget(self._L1Data_label, 0, 0)
        self._L1Data_edit = NEBox()
        self._Global_grid.addWidget(self._L1Data_edit, 0, 1)

        self._L1Inst_label = QLabel(_("L1 Inst."))
        self._Global_grid.addWidget(self._L1Inst_label, 1, 0)
        self._L1Inst_edit = NEBox()
        self._Global_grid.addWidget(self._L1Inst_edit, 1, 1)

        self._L2_label = QLabel(_("Level 2"))
        self._Global_grid.addWidget(self._L2_label, 2, 0)
        self._L2_edit = NEBox()
        self._Global_grid.addWidget(self._L2_edit, 2, 1)

        self._L3_label = QLabel(_("Level 3"))
        self._Global_grid.addWidget(self._L3_label, 3, 0)
        self._L3_edit = NEBox()
        self._Global_grid.addWidget(self._L3_edit, 3, 1)

    def refresh_cpuinfo (self, info):
        cinfo = info.getCache()
        loop = ((self._L1Data_edit, "L1Data",),
                (self._L1Inst_edit, "L1Instruction"),
                (self._L2_edit, "L2Unified"),
                (self._L3_edit, "L3Unified"))

        for edit, name in loop:
            if name in cinfo:
                s = cinfo[name]["size"]
                if len(cinfo[name]["shared_cpu_list"]) > 1:
                    s += _(" (Processor %s shares)") % \
                                " ".join(cinfo[name]["share"])
                edit.setText(s)
            else:
                edit.setText("N/A")

class CPUTab (QWidget):
    def __init__ (self, parent=None):
        QWidget.__init__(self, parent)
        self._Global_vbox = QVBoxLayout(self)

        self._Processor_group = ProcessorGroup()
        self._Global_vbox.addWidget(self._Processor_group)

        self._ClockCache_hbox = QHBoxLayout()
        self._Global_vbox.addLayout(self._ClockCache_hbox)

        self._Clock_group = ClockGroup()
        self._ClockCache_hbox.addWidget(self._Clock_group)

        self._Cache_group = CacheGroup()
        self._ClockCache_hbox.addWidget(self._Cache_group)

        self._Select_frame = QFrame()
        self._Global_vbox.addWidget(self._Select_frame)
        self._Select_hbox = QHBoxLayout(self._Select_frame)

        self._Processor_lable = QLabel(_("Processor"))
        self._Select_hbox.addWidget(self._Processor_lable)
        self._Processor_combo = QComboBox()
        for i in range(len(
                    glob.glob("/sys/devices/system/cpu/cpu[0-9]*/"))):
            self._Processor_combo.addItem(_("Processor #%d") % i)
        self.connect(self._Processor_combo, 
                    SIGNAL("currentIndexChanged(int)"),
                    self.changeCPU)
        self._Select_hbox.addWidget(self._Processor_combo)

        self._PhysicalID_lable = QLabel(_("Physical ID"))
        self._Select_hbox.addWidget(self._PhysicalID_lable)
        self._PhysicalID_edit = NEBox()
        self._Select_hbox.addWidget(self._PhysicalID_edit)

        self._CoreID_lable = QLabel(_("Core ID"))
        self._Select_hbox.addWidget(self._CoreID_lable)
        self._CoreID_edit = NEBox()
        self._Select_hbox.addWidget(self._CoreID_edit)

        self._Global_vbox.addStretch(0)

        self.changeCPU(0)

    def changeCPU (self, cpu):
        self._CurrCPU = cpu
        self.refresh()

    def refresh (self):
        cinfo = cpuinfo.cpuinfo_plus(self._CurrCPU)
        self._Processor_group.refresh_cpuinfo(cinfo)
        self._Clock_group.refresh_cpuinfo(cinfo)
        self._Cache_group.refresh_cpuinfo(cinfo)
        self._PhysicalID_edit.setText(
                str(cinfo.getTopology()["Physical"]))
        self._CoreID_edit.setText(
                str(cinfo.getTopology()["Core"]))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CPUTab()
    window.show()
    exit(app.exec_())
