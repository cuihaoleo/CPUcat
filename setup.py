#!/usr/bin/env python
#! -*- coding: utf-8 -*-

##
# setup.py: CPUcat软件包安装脚本
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

from distutils.core import setup, Extension
from cpucat.cpucat_sth import PACKAGE, VERSION

setup(name="CPUcat",
      version=VERSION,
      description="Just like CPU-Z on Windows.",
      author="CUI Hao",
      author_email="cuihao.leo@gmail.com",
      ext_modules = [Extension("cpuinfo._cpuidcall", 
                    ["cpuinfo/cpuidcall.i", "cpuinfo/cpuidcall.c"])],
      packages=["cpucat", "cpuinfo"],
      package_dir={"cpucat": "cpucat"},
      package_data={"cpucat":["logos/*.png"]},
      py_modules=["cpuinfo.cpuidcall"],
      scripts=["bin/cpucat"],
      #data_files=[('share/cpucat', ["share/cpucat/*"])]
)
