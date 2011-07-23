/*
    cpuinfo/cpuidcall.c: 调用CPUID汇编指令的C扩展。
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

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <pthread.h>
#include <sched.h>
#include "cpuidcall.h"

struct CPUregs cpuid_call (const unsigned eax)
{
    struct CPUregs ret;

    __asm__ ("cpuid"
        :"=a"(ret.EAX), "=b"(ret.EBX), 
         "=c"(ret.ECX), "=d"(ret.EDX)
        :"a"(eax));

    return ret;
}

void *__cpuid_call_core (void *args)
{
    struct {
        int eax;
        cpu_set_t cpuset;
    } *p = args;

    if (pthread_setaffinity_np(pthread_self(), 
            sizeof(p->cpuset), &(p->cpuset)) < 0)
        perror("pthread_setaffinity_np");

    struct CPUregs *ret = malloc(sizeof(struct CPUregs));
    *ret = cpuid_call(p->eax);

    return ret;
}

struct CPUregs cpuid_call_core (const unsigned eax, const unsigned long core)
{
    cpu_set_t mask;
    CPU_ZERO(&mask);
    CPU_SET(core, &mask);

    struct {
        int eax;
        cpu_set_t cpuset;
    } p = {eax, mask};

    pthread_t pid;
    if (pthread_create(&pid, NULL, __cpuid_call_core, &p))
        perror("pthread_create");
    
    struct CPUregs *ret;
    pthread_join(pid, (void*)&ret);

    return *ret;
}

char *getVendorID (const unsigned long core)
{
    union {
        struct {
            int HighestBasicFunc;
            char VendorID[12];
        } INFO;
        struct CPUregs RAW;
    } info;

    info.RAW = cpuid_call_core(0, core);

    char *ret = malloc(13*sizeof(char));
    memcpy(ret, info.INFO.VendorID, 4*sizeof(char));
    memcpy(ret+4, info.INFO.VendorID+8, 4*sizeof(char));
    memcpy(ret+8, info.INFO.VendorID+4, 4*sizeof(char));
    ret[12] = 0;

    return ret;
}

char *getBrandStr (const unsigned long core)
{
    union {
        struct {
            char BrandStr[48];
        } INFO;
        struct CPUregs RAW[4];
    } info;

    info.RAW[0] = cpuid_call_core(0x80000002, core);
    info.RAW[1] = cpuid_call_core(0x80000003, core);
    info.RAW[2] = cpuid_call_core(0x80000004, core);

    char *ret = malloc(49*sizeof(char));
    memcpy(ret, info.INFO.BrandStr, 48*sizeof(char));
    ret[48] = 0;

    return ret;
}
