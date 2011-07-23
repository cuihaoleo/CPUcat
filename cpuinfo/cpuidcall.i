/*
    cpuinfo/cpuidcall.i: 调用CPUID汇编指令的C扩展的SWIG接口。
    This file is part of CPUcat.

    CPUcat
    类似Windows下CPU-Z的获取CPU和其他硬件信息的工具。
    Copyright (C) 2011  CUI Hao

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

    Author: 崔灏 (CUI Hao)
    Email: cuihao.leo@gmail.com
*/

%module cpuidcall
%{
#include "cpuidcall.h"
%}

struct CPUregs {
    int EAX, EBX, ECX, EDX;
};

extern struct CPUregs cpuid_call (const unsigned eax);
extern struct CPUregs cpuid_call_core (const unsigned eax, const unsigned long core);
extern char *getVendorID (const unsigned long core);
extern char *getBrandStr (const unsigned long core);

