#!/usr/bin/env python
# -*- coding: utf-8 -*-

##
# cpuinfo/__init__.py: cpuinfo获取CPU信息的模块的主程序。
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

import re
import os
try:
    from subprocess import getstatusoutput
except ImportError:
    from commands import getstatusoutput
from cpuinfo.cpuidcall import *

def getBit (n, start, end=None):
    length = end-start if end else 0
    return (n >> start) & ((2 << length) - 1)

class cpuinfo (object):
    def __init__ (self, cpu):
        self._ProcessorID = cpu

        cinfo = self.CPUIDinfo = {}
        for i in range(0, 6):
            self.CPUIDinfo[i] = cpuid_call_core(i, cpu)
        for i in range(0x80000000, 0x80000008):
            self.CPUIDinfo[i] = cpuid_call_core(i, cpu)

        # Model
        self._ModelInfo = {}
        self._ModelInfo["VendorID"] = getVendorID(cpu)
        self._ModelInfo["BrandStr"] = getBrandStr(cpu)
        self._ModelInfo["Stepping"] = getBit(cinfo[1].EAX, 0, 3)
        self._ModelInfo["Model"] = getBit(cinfo[1].EAX, 4, 7)
        self._ModelInfo["Family"] = getBit(cinfo[1].EAX, 8, 11)
        self._ModelInfo["Type"] = getBit(cinfo[1].EAX, 12, 13)
        self._ModelInfo["ExtModel"] = getBit(cinfo[1].EAX, 16, 19)
        self._ModelInfo["ExtFamily"] = getBit(cinfo[1].EAX, 20, 27)

        # Topology
        self._Topology = {}
        path = "/sys/devices/system/cpu/cpu%d/topology/" % self._ProcessorID
        self._Topology["Physical"] = \
                int(open(path + "physical_package_id").read())
        self._Topology["Core"] = \
                int(open(path + "core_id").read())

        # Cache
        self._Cache = {}
        path = "/sys/devices/system/cpu/cpu%d/cache/" % self._ProcessorID
        for di in next(os.walk(path))[1]:
            name = "L%s%s" % (
                    open(os.path.join(path,di,"level")).read().strip(),
                    open(os.path.join(path,di,"type")).read().strip())
            self._Cache[name] = {
                "size":
                    open(os.path.join(path,di,"size")).read().strip(),
                "ways_of_associativity":
                    int(open(os.path.join(\
                        path,di,"ways_of_associativity")).read().strip()),
                "coherency_line_size":
                    int(open(os.path.join(
                        path,di,"coherency_line_size")).read().strip()),
                "shared_cpu_list":
                    [int(x) for x in open(os.path.join(
                        path,di,"shared_cpu_list")).read().split("-")],
            }

    def isAMD (self):
        return "AMD" in self._ModelInfo["VendorID"]

    def isIntel (self):
        return "Intel" in self._ModelInfo["VendorID"]

    def MMX_3DNow_support (self):
        ret = []
        if getBit(self.CPUIDinfo[1].EDX, 23): ret.append("MMX")
        if getBit(self.CPUIDinfo[0x80000001].EDX, 22): ret.append("MMXExt")
        if getBit(self.CPUIDinfo[0x80000001].EDX, 31): ret.append("3DNow")
        if getBit(self.CPUIDinfo[0x80000001].EDX, 30): ret.append("3DNowExt")
        return ret

    def SSE_support (self):
        ret = []
        if getBit(self.CPUIDinfo[1].EDX, 25): ret.append("SSE")
        if getBit(self.CPUIDinfo[1].EDX, 26): ret.append("SSE2")
        if getBit(self.CPUIDinfo[1].ECX, 0): ret.append("SSE3")
        if getBit(self.CPUIDinfo[1].ECX, 9): ret.append("SSSE3")
        if getBit(self.CPUIDinfo[1].ECX, 11): ret.append("XOP")
        if getBit(self.CPUIDinfo[1].ECX, 12): ret.append("FMA3")
        if getBit(self.CPUIDinfo[1].ECX, 16): ret.append("FMA4")
        if getBit(self.CPUIDinfo[1].ECX, 19): ret.append("SSE41")
        if getBit(self.CPUIDinfo[1].ECX, 20): ret.append("SSE42")
        if getBit(self.CPUIDinfo[1].ECX, 28): ret.append("AVX")
        if getBit(self.CPUIDinfo[1].ECX, 29): ret.append("CVT16")
        return ret

    def x86Virt_support (self):
        ret = []
        if getBit(self.CPUIDinfo[1].ECX, 5): ret.append("VT-x")
        if getBit(self.CPUIDinfo[0x80000001].ECX, 2): ret.append("AMD-V")
        return ret

    def AES_ifsupport (self):
        return getBit(self.CPUIDinfo[1].ECX, 25)==1

    def EMT64T_LM_ifsupport (self):
        return getBit(self.CPUIDinfo[0x80000001].EDX, 29)==1

    def getTopology (self):
        return self._Topology

    def getModelInfo (self):
        return self._ModelInfo

    def getCache (self):
        return self._Cache

class cpuinfo_plus (cpuinfo):
    def __init__ (self, cpu):
        cpuinfo.__init__(self, cpu)

        self._getinfo_from_dmidecode()
        self._getinfo_fron_lscpu()

    def _getinfo_fron_lscpu (self): 
        ret, output = getstatusoutput("lscpu")
        if ret: return

        self._OpMode = re.findall(r"CPU op-mode\(s\):[\s]*(.*)",
                                output)[0].split(",")
        self._BogoMIPS = float(re.findall(r"BogoMIPS:[\s]*([\S]*)",
                                output)[0])

    def _getinfo_from_dmidecode (self):
        if os.getuid(): return

        ret, output = getstatusoutput("dmidecode -t processor")
        if ret: return

        extclock = re.findall(r"External Clock: (.*)", output)[0]
        currspeed = re.findall(r"Current Speed: (.*)", output)[0]

        self._Speed = {
                "ExternalClock": extclock,
                "SpeedBIOS": currspeed,
                "Multiplier": "x%.1f" % \
                                (int(currspeed.split()[0])/
                                 int(extclock.split()[0]))
            }
        self._Slot = re.findall(r"Socket Designation: (.*)", output)[0]

    def getCurrentSpeed (self):
        text = open("/proc/cpuinfo"). \
                read().split("\n\n")[self._ProcessorID]
        return "%s MHz" % re.compile(
                r"cpu MHz[\s]*:[\s]*([\S]*)\.").findall(text)[0]

    def getBIOSSpeedInfo (self):
        try:
            return self._Speed
        except:
            return { "ExternalClock": "N/A",
                     "SpeedBIOS": "N/A",
                     "Multiplier": "N/A"}

    def getSlot (self):
        try:
            return self._Slot
        except AttributeError:
            return "N/A"

    def getOpMode (self):
        try:
            return self._OpMode
        except AttributeError:
            return ["N/A"]

    def getBogoMIPS (self):
        try:
            return self._BogoMIPS
        except AttributeError:
            return 0

