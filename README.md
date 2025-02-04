# cirunner

**cirunner** is a Python script to setup, capture and display crash in GitHub action,
for Linux, Windows, and MacOS.


A program is run via the script as follows (for all platforms):

```bash
python cirunner.py -t 3600 -- target_exe arg1 arg2 ..
```

The above does the following:

1. it sets up crash handler on the system
2. it forwards any stdout/stderr output from the program without buffering.
3. it collects and analyze crash dump and display the analysis using a debugger if the program crashes
4. it terminates the program and generate crash dump and display the analysis using a debugger
   if the program runs for more than 3606 seconds (default is six hours if timeout is not specified)
5. it returns using the return value of the program.


## Samples

For examples, see the GitHub action results and yml workflows for each platform in this repository.


## Windows Notes

**Installation**

The installation is done by both `installwindows.ps1` and `winrunner.py -i`. They do the following tasks.

1. Installing registry in `localdumps.reg`
2. Download [procdump](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump)
3. Make sure **cdb** (Microsoft console debugger) exists (it does on GitHub Windows runners)

If you're testing on your local Windows machine, you will need to install **cdb** by following these instructions:

1. Run Windows SDK 10 installer if you haven't installed it, or run from 
   **Add/Remove Program > Windows Software Development Kit -> Modify**.
2. Select component: **Debugging Tools for Windows**

**Handling crashes**

Once the registry settings in `localdumps.reg` is installed, any crashes will be stored as minidump
in `%localprofile%\Dumps` folder (e.g. `C:\Users\pjsip\Dumps`). **cirunner** then runs **cdb** to analyze
the crash. See sample output below.

**Handling timeout**

On timeout, **cirunner** executes [procdump](https://learn.microsoft.com/en-us/sysinternals/downloads/procdump)
to create minidump of the program's state, then runs **cdb** to analyze the minidump.

**Sample crash dump output**

The output of **cdb** is quite extensive, and useful. It shows crash location, stack trace, and stack trace
of all threads. Click **Show output** below for sample output with bug induced `pjlib-test`.

<details>
  <summary>Show output</summary>

```
Microsoft (R) Windows Debugger Version 10.0.19041.685 AMD64
Copyright (c) Microsoft Corporation. All rights reserved.


Loading Dump File [C:\Users\bennylp\Dumps\pjlib-test-i386-Win32-vc14-Debug.exe.5644.dmp]
User Mini Dump File: Only registers, stack and portions of memory are available

Symbol search path is: srv*
Executable search path is:
Windows 10 Version 19045 MP (4 procs) Free x86 compatible
Product: WinNt, suite: SingleUserTS
19041.1.amd64fre.vb_release.191206-1406
Machine Name:
Debug session time: Tue Feb  4 09:51:15.000 2025 (UTC + 7:00)
System Uptime: not available
Process Uptime: 0 days 0:00:06.000
........................
This dump file has an exception of interest stored in it.
The stored exception information can be accessed via .ecxr.
(160c.2e90): Access violation - code c0000005 (first/second chance not available)
For analysis of this file, run !analyze -v
eax=00000000 ebx=00000000 ecx=00000f9c edx=00e23600 esi=00000003 edi=00000003
eip=770b358c esp=00afdc58 ebp=00afdde8 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000202
ntdll!NtWaitForMultipleObjects+0xc:
770b358c c21400          ret     14h
0:000> cdb: Reading initial command '!analyze -v; ~* k; q'
*******************************************************************************
*                                                                             *
*                        Exception Analysis                                   *
*                                                                             *
*******************************************************************************


KEY_VALUES_STRING: 1

    Key  : AV.Fault
    Value: Write

    Key  : Analysis.CPU.Sec
    Value: 1

    Key  : Analysis.DebugAnalysisProvider.CPP
    Value: Create: 8007007e on DESKTOP-8I1RHUB

    Key  : Analysis.DebugData
    Value: CreateObject

    Key  : Analysis.DebugModel
    Value: CreateObject

    Key  : Analysis.Elapsed.Sec
    Value: 1

    Key  : Analysis.Memory.CommitPeak.Mb
    Value: 87

    Key  : Analysis.System
    Value: CreateObject

    Key  : Timeline.Process.Start.DeltaSec
    Value: 6


NTGLOBALFLAG:  0

APPLICATION_VERIFIER_FLAGS:  0

CONTEXT:  (.ecxr)
eax=00000064 ebx=009ff000 ecx=00000f9c edx=00e23600 esi=00000f9c edi=001e114a
eip=001ffbc8 esp=00afe590 ebp=00afe59c iopl=0         nv up ei pl nz ac pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010216
pjlib_test_i386_Win32_vc14_Debug!capacity_test+0x78:
001ffbc8 c70100000000    mov     dword ptr [ecx],0    ds:002b:00000f9c=????????
Resetting default scope

EXCEPTION_RECORD:  (.exr -1)
ExceptionAddress: 001ffbc8 (pjlib_test_i386_Win32_vc14_Debug!capacity_test+0x00000078)
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000001
   Parameter[1]: 00000f9c
Attempt to write to address 00000f9c

PROCESS_NAME:  pjlib-test-i386-Win32-vc14-Debug.exe

WRITE_ADDRESS:  00000f9c

ERROR_CODE: (NTSTATUS) 0xc0000005 - The instruction at 0x%p referenced memory at 0x%p. The memory could not be %s.

EXCEPTION_CODE_STR:  c0000005

EXCEPTION_PARAMETER1:  00000001

EXCEPTION_PARAMETER2:  00000f9c

STACK_TEXT:
00afe59c 001ffa8b 00afe604 00afe604 00afe604 pjlib_test_i386_Win32_vc14_Debug!capacity_test+0x78
00afe5ac 002454a3 001e4a16 0022ecab 332a1299 pjlib_test_i386_Win32_vc14_Debug!pool_test+0xb
00afe604 0024565e 00afe724 00000000 00afe9c4 pjlib_test_i386_Win32_vc14_Debug!run_test_case+0xb3
00afe61c 00244b58 00afe724 00afe750 00aff988 pjlib_test_i386_Win32_vc14_Debug!basic_runner_main+0x3e
00afe62c 002150ca 00afe724 00afe750 001e114a pjlib_test_i386_Win32_vc14_Debug!pj_test_run+0x98
00aff988 00215603 00aff9a4 00000001 00dfc4a0 pjlib_test_i386_Win32_vc14_Debug!essential_tests+0x83a
00affca0 002146b9 00000001 00dfc4a0 00000004 pjlib_test_i386_Win32_vc14_Debug!test_inner+0xe3
00affd00 001fe881 00000001 00dfc4a0 002a314e pjlib_test_i386_Win32_vc14_Debug!test_main+0x49
00affd30 00248ae3 00000001 00dfc4a0 00dfe8e0 pjlib_test_i386_Win32_vc14_Debug!main+0x241
00affd50 00248937 a6ec9253 001e114a 001e114a pjlib_test_i386_Win32_vc14_Debug!invoke_main+0x33
00affdac 002487cd 00affdbc 00248b68 00affdcc pjlib_test_i386_Win32_vc14_Debug!__scrt_common_main_seh+0x157
00affdb4 00248b68 00affdcc 7618fcc9 009ff000 pjlib_test_i386_Win32_vc14_Debug!__scrt_common_main+0xd
00affdbc 7618fcc9 009ff000 7618fcb0 00affe28 pjlib_test_i386_Win32_vc14_Debug!mainCRTStartup+0x8
00affdcc 770a809e 009ff000 5b0833c3 00000000 kernel32!BaseThreadInitThunk+0x19
00affe28 770a806e ffffffff 770c9137 00000000 ntdll!__RtlUserThreadStart+0x2f
00affe38 00000000 001e114a 009ff000 00000000 ntdll!_RtlUserThreadStart+0x1b


FAULTING_SOURCE_LINE:  C:\Users\bennylp\Desktop\project\pjproject\pjlib\src\pjlib-test\pool.c

FAULTING_SOURCE_FILE:  C:\Users\bennylp\Desktop\project\pjproject\pjlib\src\pjlib-test\pool.c

FAULTING_SOURCE_LINE_NUMBER:  69

SYMBOL_NAME:  pjlib_test_i386_Win32_vc14_Debug!capacity_test+78

MODULE_NAME: pjlib_test_i386_Win32_vc14_Debug

IMAGE_NAME:  pjlib-test-i386-Win32-vc14-Debug.exe

STACK_COMMAND:  ~0s ; .ecxr ; kb

FAILURE_BUCKET_ID:  NULL_CLASS_PTR_WRITE_c0000005_pjlib-test-i386-Win32-vc14-Debug.exe!capacity_test

OS_VERSION:  10.0.19041.1

BUILDLAB_STR:  vb_release

OSPLATFORM_TYPE:  x86

OSNAME:  Windows 10

FAILURE_ID_HASH:  {296b5e72-5b8d-2395-c93f-74f7e3cb5d90}

Followup:     MachineOwner
---------


.  0  Id: 160c.2e90 Suspend: 0 Teb: 00802000 Unfrozen
ChildEBP RetAddr
00afdc54 7536a823 ntdll!NtWaitForMultipleObjects+0xc
00afdde8 7536a708 KERNELBASE!WaitForMultipleObjectsEx+0x103
00afde04 761d800b KERNELBASE!WaitForMultipleObjects+0x18
00afdeb0 761d7c3c kernel32!WerpReportFaultInternal+0x3b7
00afdecc 761ad2e9 kernel32!WerpReportFault+0x9d
00afded4 75428180 kernel32!BasepReportFault+0x19
00afdf74 770e48a5 KERNELBASE!UnhandledExceptionFilter+0x290
00affe28 770a806e ntdll!__RtlUserThreadStart+0x3c836
00affe38 00000000 ntdll!_RtlUserThreadStart+0x1b

   1  Id: 160c.1980 Suspend: 1 Teb: 00805000 Unfrozen
ChildEBP RetAddr
00dbfd88 77075c30 ntdll!NtWaitForWorkViaWorkerFactory+0xc
00dbff48 7618fcc9 ntdll!TppWorkerThread+0x2a0
00dbff58 770a809e kernel32!BaseThreadInitThunk+0x19
00dbffb4 770a806e ntdll!__RtlUserThreadStart+0x2f
00dbffc4 00000000 ntdll!_RtlUserThreadStart+0x1b

   2  Id: 160c.1f0 Suspend: 1 Teb: 00808000 Unfrozen
ChildEBP RetAddr
00fefb60 77075c30 ntdll!NtWaitForWorkViaWorkerFactory+0xc
00fefd20 7618fcc9 ntdll!TppWorkerThread+0x2a0
00fefd30 770a809e kernel32!BaseThreadInitThunk+0x19
00fefd8c 770a806e ntdll!__RtlUserThreadStart+0x2f
00fefd9c 00000000 ntdll!_RtlUserThreadStart+0x1b

   3  Id: 160c.282c Suspend: 1 Teb: 0080b000 Unfrozen
ChildEBP RetAddr
0112f6dc 77075c30 ntdll!NtWaitForWorkViaWorkerFactory+0xc
0112f89c 7618fcc9 ntdll!TppWorkerThread+0x2a0
0112f8ac 770a809e kernel32!BaseThreadInitThunk+0x19
0112f908 770a806e ntdll!__RtlUserThreadStart+0x2f
0112f918 00000000 ntdll!_RtlUserThreadStart+0x1b
quit:
NatVis script unloaded from 'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\Visualizers\atlmfc.natvis'
NatVis script unloaded from 'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\Visualizers\concurrency.natvis'
NatVis script unloaded from 'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\Visualizers\cpp_rest.natvis'
NatVis script unloaded from 'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\Visualizers\stl.natvis'
NatVis script unloaded from 'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\Visualizers\Windows.Data.Json.natvis'
NatVis script unloaded from 'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\Visualizers\Windows.Devices.Geolocation.natvis'
NatVis script unloaded from 'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\Visualizers\Windows.Devices.Sensors.natvis'
NatVis script unloaded from 'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\Visualizers\Windows.Media.natvis'
NatVis script unloaded from 'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\Visualizers\windows.natvis'
NatVis script unloaded from 'C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\Visualizers\winrt.natvis'
09:51:26 cirunner: Exiting with exit code 3221225477
```

</details>


**Limitations/TODO**

1. Maybe we can use **cdb** to generate the crash dump, to avoid using third party **procdump**.
2. It will be nice if the callstack includes the parameter values like the one produced by **gdb** or **lldb**.


## Linux Notes

**Installation**

The `installlinux.sh` and `linuxrunner.py -i` need to be called once on the target machine to perform
the following:

1. install **gdb**
2. sets `/proc/sys/kernel/core_pattern` to `core.%p`

**Handling crashes**

The `linuxrunner.py` will take care of setting `ulimit -c` before running the program.
Any crashes will generate file `core.PID` in the directory where the program is run. 
**cirunner** then runs **gdb** to analyze the crash. See sample output below.

**Handling timeout**

The `linuxrunner.py` will take care of setting `ulimit -c` before running the program.
On timeout, **cirunner** sends `SIGQUIT` which (should) cause the program to crash and generate
core. It then runs **gdb** to analyze the minidump.

**Sample crash dump output**

The output of **gdb** is quite extensive, and very useful. It shows crash location, stack trace, and stack trace
of all threads, **along with values of all parameters**. Click **Show output** below for sample output with bug induced `pjlib-test` running with `-w 4`.

<details>
  <summary>Show output</summary>

```
Reading symbols from /home/bennylp/Desktop/project/pjproject/pjlib/bin/pjlib-test-x86_64-unknown-linux-gnu...
[New LWP 959143]
[New LWP 959142]
[New LWP 958137]
[New LWP 959145]
[New LWP 959144]
[Thread debugging using libthread_db enabled]
Using host libthread_db library "/lib/x86_64-linux-gnu/libthread_db.so.1".
Core was generated by `/home/bennylp/Desktop/project/pjproject/pjlib/bin/pjlib-test-x86_64-unknown-lin'.
Program terminated with signal SIGSEGV, Segmentation fault.
#0  timestamp_test () at ../src/pjlib-test/timestamp.c:139
139	    *(long*)(long)rc = 0x1234;
[Current thread is 1 (Thread 0x7d25bc000640 (LWP 959143))]
+where
#0  timestamp_test () at ../src/pjlib-test/timestamp.c:139
#1  0x00005b4a14f14f9e in run_test_case (runner=0x5b4a1c50c098, tid=2, tc=0x5b4a1516eec0 <test_app+960>) at ../src/pj/unittest.c:542
#2  0x00005b4a14f154e7 in text_runner_thread_proc (arg=0x5b4a1c50c258) at ../src/pj/unittest.c:741
#3  0x00005b4a14ef0d77 in thread_main (param=0x5b4a1c50c268) at ../src/pj/os_core_unix.c:701
#4  0x00007d25c1c94ac3 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:442
#5  0x00007d25c1d26850 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81
+thread apply all bt

Thread 5 (Thread 0x7d25bca00640 (LWP 959144)):
+bt
#0  0x00007d25c1ce57f8 in __GI___clock_nanosleep (clock_id=clock_id@entry=0, flags=flags@entry=0, req=req@entry=0x7d25bc9ffd40, rem=rem@entry=0x0) at ../sysdeps/unix/sysv/linux/clock_nanosleep.c:78
#1  0x00007d25c1cea677 in __GI___nanosleep (req=req@entry=0x7d25bc9ffd40, rem=rem@entry=0x0) at ../sysdeps/unix/sysv/linux/nanosleep.c:25
#2  0x00007d25c1d1bf2f in usleep (useconds=<optimized out>) at ../sysdeps/posix/usleep.c:31
#3  0x00005b4a14ef1232 in pj_thread_sleep (msec=100) at ../src/pj/os_core_unix.c:948
#4  0x00005b4a14f154fc in text_runner_thread_proc (arg=0x5b4a1c50c328) at ../src/pj/unittest.c:746
#5  0x00005b4a14ef0d77 in thread_main (param=0x5b4a1c50c338) at ../src/pj/os_core_unix.c:701
#6  0x00007d25c1c94ac3 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:442
#7  0x00007d25c1d26850 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81

Thread 4 (Thread 0x7d25bd400640 (LWP 959145)):
+bt
#0  0x00007d25c1ce57f8 in __GI___clock_nanosleep (clock_id=clock_id@entry=0, flags=flags@entry=0, req=req@entry=0x7d25bd3ffd40, rem=rem@entry=0x0) at ../sysdeps/unix/sysv/linux/clock_nanosleep.c:78
#1  0x00007d25c1cea677 in __GI___nanosleep (req=req@entry=0x7d25bd3ffd40, rem=rem@entry=0x0) at ../sysdeps/unix/sysv/linux/nanosleep.c:25
#2  0x00007d25c1d1bf2f in usleep (useconds=<optimized out>) at ../sysdeps/posix/usleep.c:31
#3  0x00005b4a14ef1232 in pj_thread_sleep (msec=100) at ../src/pj/os_core_unix.c:948
#4  0x00005b4a14f154fc in text_runner_thread_proc (arg=0x5b4a1c50c3f8) at ../src/pj/unittest.c:746
#5  0x00005b4a14ef0d77 in thread_main (param=0x5b4a1c50c408) at ../src/pj/os_core_unix.c:701
#6  0x00007d25c1c94ac3 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:442
#7  0x00007d25c1d26850 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81

Thread 3 (Thread 0x7d25c24bd540 (LWP 958137)):
+bt
#0  0x00007d25c1ce57f8 in __GI___clock_nanosleep (clock_id=clock_id@entry=0, flags=flags@entry=0, req=req@entry=0x7fff1cca6e50, rem=rem@entry=0x0) at ../sysdeps/unix/sysv/linux/clock_nanosleep.c:78
#1  0x00007d25c1cea677 in __GI___nanosleep (req=req@entry=0x7fff1cca6e50, rem=rem@entry=0x0) at ../sysdeps/unix/sysv/linux/nanosleep.c:25
#2  0x00007d25c1d1bf2f in usleep (useconds=<optimized out>) at ../sysdeps/posix/usleep.c:31
#3  0x00005b4a14ef1232 in pj_thread_sleep (msec=100) at ../src/pj/os_core_unix.c:948
#4  0x00005b4a14f154fc in text_runner_thread_proc (arg=0x7fff1cca6f10) at ../src/pj/unittest.c:746
#5  0x00005b4a14f15591 in text_runner_main (base=0x5b4a1c50c098) at ../src/pj/unittest.c:770
#6  0x00005b4a14f1445c in pj_test_run (runner=0x5b4a1c50c098, suite=0x5b4a1516eb30 <test_app+48>) at ../src/pj/unittest.c:235
#7  0x00005b4a14ee5300 in ut_run_tests (ut_app=0x5b4a1516eb00 <test_app>, title=0x5b4a14f1e84e "features tests", argc=1, argv=0x7fff1cca79f8) at ../src/pjlib-test/test_util.h:202
#8  0x00005b4a14ee6734 in features_tests (argc=1, argv=0x7fff1cca79f8) at ../src/pjlib-test/test.c:350
#9  0x00005b4a14ee68e2 in test_inner (argc=1, argv=0x7fff1cca79f8) at ../src/pjlib-test/test.c:397
#10 0x00005b4a14ee6a70 in test_main (argc=1, argv=0x7fff1cca79f8) at ../src/pjlib-test/test.c:445
#11 0x00005b4a14ebced7 in main (argc=1, argv=0x7fff1cca79f8) at ../src/pjlib-test/main.c:172

Thread 2 (Thread 0x7d25bb600640 (LWP 959142)):
+bt
#0  0x00007d25c1ce57f8 in __GI___clock_nanosleep (clock_id=clock_id@entry=0, flags=flags@entry=0, req=req@entry=0x7d25bb5ffd40, rem=rem@entry=0x0) at ../sysdeps/unix/sysv/linux/clock_nanosleep.c:78
#1  0x00007d25c1cea677 in __GI___nanosleep (req=req@entry=0x7d25bb5ffd40, rem=rem@entry=0x0) at ../sysdeps/unix/sysv/linux/nanosleep.c:25
#2  0x00007d25c1d1bf2f in usleep (useconds=<optimized out>) at ../sysdeps/posix/usleep.c:31
#3  0x00005b4a14ef1232 in pj_thread_sleep (msec=100) at ../src/pj/os_core_unix.c:948
#4  0x00005b4a14f154fc in text_runner_thread_proc (arg=0x5b4a1c50c188) at ../src/pj/unittest.c:746
#5  0x00005b4a14ef0d77 in thread_main (param=0x5b4a1c50c198) at ../src/pj/os_core_unix.c:701
#6  0x00007d25c1c94ac3 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:442
#7  0x00007d25c1d26850 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81

Thread 1 (Thread 0x7d25bc000640 (LWP 959143)):
+bt
#0  timestamp_test () at ../src/pjlib-test/timestamp.c:139
#1  0x00005b4a14f14f9e in run_test_case (runner=0x5b4a1c50c098, tid=2, tc=0x5b4a1516eec0 <test_app+960>) at ../src/pj/unittest.c:542
#2  0x00005b4a14f154e7 in text_runner_thread_proc (arg=0x5b4a1c50c258) at ../src/pj/unittest.c:741
#3  0x00005b4a14ef0d77 in thread_main (param=0x5b4a1c50c268) at ../src/pj/os_core_unix.c:701
#4  0x00007d25c1c94ac3 in start_thread (arg=<optimized out>) at ./nptl/pthread_create.c:442
#5  0x00007d25c1d26850 in clone3 () at ../sysdeps/unix/sysv/linux/x86_64/clone3.S:81
+quit
10:38:27 cirunner: Exiting with exit code -11
```

</details>


## MacOS Notes

**Installation**

The `installmac.sh` and `macrunner.py -i` don't do anything. We use `lldb` which is already installed
and existing core pattern `/cores/core.%P`.

**Handling crashes**

The `macrunner.py` will take care of setting `ulimit -c` before running the program.
Any crashes will generate file `core.PID` in `/cores` directory. 
**cirunner** then runs **lldb** to analyze the crash. See sample output below.

**Handling timeout**

The `macrunner.py` will take care of setting `ulimit -c` before running the program.
On timeout, **cirunner** sends `SIGQUIT` which (should) cause the program to crash and generate
core. It then runs **lldb** to analyze the minidump.

**Sample crash dump output**

The output of **lldb** is quite extensive, and useful. It shows stack trace
of all threads along with values of all parameters. 

**lldb** output is okay, it shows crash location, stack trace, and stack trace
of all threads, **along with values of all parameters**.
Click **Show output** below for sample output with bug induced `pjlib-test` running with `-w 4`.

<details>
  <summary>Show output</summary>

```
(lldb) target create "/Users/runner/work/pjproject/pjproject/pjlib/bin/pjlib-test-arm-apple-darwin23.6.0" --core "/cores/core.18011"
Core file '/cores/core.18011' (arm64) was loaded.
(lldb) bt all
warning: could not execute support code to read Objective-C class data in the process. This may reduce the quality of type information available.

* thread #1, stop reason = ESR_EC_DABORT_EL0 (fault address: 0x0)
  * frame #0: 0x0000000100e64ef0 pjlib-test-arm-apple-darwin23.6.0`timestamp_test at timestamp.c:139:22
  thread #2
    frame #0: 0x00000001932643c8 libsystem_kernel.dylib`__semwait_signal + 8
    frame #1: 0x0000000193145568 libsystem_c.dylib`nanosleep + 220
    frame #2: 0x0000000193145480 libsystem_c.dylib`usleep + 68
    frame #3: 0x0000000100e6eb60 pjlib-test-arm-apple-darwin23.6.0`pj_thread_sleep(msec=100) at os_core_unix.c:948:5
    frame #4: 0x0000000100e9ef90 pjlib-test-arm-apple-darwin23.6.0`text_runner_thread_proc(arg=0x00000001378134f0) at unittest.c:746:13
    frame #5: 0x0000000100e6e5dc pjlib-test-arm-apple-darwin23.6.0`thread_main(param=0x0000000137813500) at os_core_unix.c:701:27
    frame #6: 0x00000001932a1f94 libsystem_pthread.dylib`_pthread_start + 136
  thread #3
    frame #0: 0x00000001932643c8 libsystem_kernel.dylib`__semwait_signal + 8
    frame #1: 0x0000000193145568 libsystem_c.dylib`nanosleep + 220
    frame #2: 0x0000000193145480 libsystem_c.dylib`usleep + 68
    frame #3: 0x0000000100e6eb60 pjlib-test-arm-apple-darwin23.6.0`pj_thread_sleep(msec=100) at os_core_unix.c:948:5
    frame #4: 0x0000000100e9ef90 pjlib-test-arm-apple-darwin23.6.0`text_runner_thread_proc(arg=0x00000001378135d8) at unittest.c:746:13
    frame #5: 0x0000000100e6e5dc pjlib-test-arm-apple-darwin23.6.0`thread_main(param=0x00000001378135e8) at os_core_unix.c:701:27
    frame #6: 0x00000001932a1f94 libsystem_pthread.dylib`_pthread_start + 136
(lldb) quit
08:50:39 cirunner: Exiting with exit code -11
```

</details>


**TODO**

Maybe someone can improve **lldb** commands to dump more info about the crash (similar to `where`
command in **gdb**).
