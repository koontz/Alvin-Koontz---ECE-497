MAKE)
file are located at in make directory

1) target = app.o
2) dependency = app.c
3) command = gcc

from man gcc
-c  Compile or assemble the source files, but do not link.  The linking stage simply is not
           done.  The ultimate output is in the form of an object file for each source file.


CROSS-COMPILING)

host)

koontz$ gcc helloWorld.c koontz@koontz-Z170X-UD3:~/Desktop/ECE_497/AlvinKoontz_ECE-497/hw05/cross-compiling$ file a.out 
a.out: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=e83a5cdeda736aa8a894f8b5783b270974e72cb0, not stripped
koontz$ ./a.out 
Hello, World! Main is executing at 0x400596
This address (0x7ffc54d494d0) is in our stack frame
This address (0x601048) is in our bss section
This address (0x601040) is in our data section

cross)

koontz@koontz-Z170X-UD3:$ ${CROSS_COMPILE}gcc helloWorld.c 
koontz@koontz-Z170X-UD3:$ file a.out
a.out: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), dynamically linked, interpreter /lib/ld-linux-armhf.so.3, for GNU/Linux 2.6.32, BuildID[sha1]=282dc6a83882bdf15af29b95fa2ace91127a834e, not stripped
koontz@koontz-Z170X-UD3:$ scp a.out root@bone:~
Debian GNU/Linux 8
BeagleBoard.org Debian Image 2016-08-28
Support/FAQ: http://elinux.org/Beagleboard:BeagleBoneBlack_Debian
default username:password is [debian:temppwd]
a.out                                                              100%   10KB  10.1KB/s   00:00    
koontz@koontz-Z170X-UD3:$ ssh root@bone
Debian GNU/Linux 8
BeagleBoard.org Debian Image 2016-08-28
Support/FAQ: http://elinux.org/Beagleboard:BeagleBoneBlack_Debian
default username:password is [debian:temppwd]
Last login: Sat Sep 24 18:16:21 2016 from 192.168.7.1
root@koontz_bone:~# ./a.out 
Hello, World! Main is executing at 0x103d5
This address (0xbeebb4d4) is in our stack frame
This address (0x20668) is in our bss section
This address (0x20660) is in our data section
root@koontz_bone:~# 

PUSHING TO CLOUD)
saves to an intermetary data.json for debugging i guess
was demoed in class

KERNEL)
I successfully compiled to kernel, took about 9 minutes on my desktop
installing it was more tricky, i tried to just plug in the sd card to my desktop 
and install that way, but it failed both times, moutning using sshfs worked though

==========
Prof. Yoder's comments
Looks good and complete.
I don't know why plugging in the SD card didn't work, though I haven't tried it recently.


Grade:  10/10
