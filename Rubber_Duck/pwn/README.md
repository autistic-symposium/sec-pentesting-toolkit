The Payloads
============

The scripts are written in PowerShell (only work against target machines with PowerShell installed, i.e. Windows 7/8, Windows Server 2008. Administrative access is also required.


The payloads are from three categories:

* Reconnaissance (reports are generated with information about the target computer):
Computer Information
User Information
USB Information
Shared Drive Information
Program Information
Installed Updates
User Document List
Basic Network Information
Network Scan
Port Scan
Copy Wireless Profile
Take Screen Captures
Copy FireFox Profile
Extract SAM File


* Exploitation:
Find and Upload File (FTP)
Disable Firewall
Add User
Open Firewall Port
Start Wi-Fi Access Point
Share C:\ Drive
Enable RDP
Create a Reverse Shell
Local DNS Poisoning
Delete a Windows Update


* Reporting (always together with the above items):
Save Report to Target Machine
FTP Report to External Host
Email Report to GMAIL Account
Save Files to USB Drive

We will use the last one in our payloads.

Note that we use the name QUACK for the usb stick.



Ducky Syntax
============

* Each command resides on a new line

* Commands are ALL CAPS

* Lines beginning with REM will not be processed

* DEFAULT_DELAY or DEFAULTDELAY is used to define how long (in milliseconds * 10) to wait between each subsequent command. DEFAULT_DELAY must be issued at the beginning of the ducky script and is optional.
  DEFAULT_DELAY 100
  REM delays 100ms between each subsequent command sequence

* DELAY creates a momentary pause in the ducky script.
  DELAY 500
  REM will wait 500ms before continuing to the next command.

* STRING processes the text following taking special care to auto-shift.
  GUI r
  DELAY 500ms
  STRING notepad.exe
  ENTER
  DELAY 1000
  STRING Hello World!

* WINDOWS or GUI emulates the Windows-Key:
  GUI r
  REM will hold the Windows-key and press r

* MENU or APP emulates the App key, sometimes referred to as the menu key or context menu key. On Windows systems this is similar to the SHIFT F10 key combo.
  GUI d
  MENU
  STRING v
  STRING d

* SHIFT: unlike CAPSLOCK, cruise control for cool, the SHIFT command can be used when navigating fields to select text, among other functions.
  SHIFT INSERT
  REM this is paste for most operating systems

* ALT key is instrumental in many automation operations:
  GUI r
  DELAY 50
  STRING notepad.exe
  ENTER
  DELAY 100
  STRING Hello World
  ALT f
  STRING s
  REM alt-f pulls up the File menu and s saves.

* CONTROL or CTRL:
  CONTROL ESCAPE
  REM this is equivalent to the GUI key in Windows

* Arrow Keys: ^ Command ^ | DOWNARROW or DOWN | | LEFTARROW or LEFT | | RIGHTARROW or RIGHT | | UPARROW or UP |


Compiling
==========

Ducky Scripts are compiled into hex files ready to be named inject.bin and moved to the root of a microSD card for execution by the USB Rubber Ducky.

This is done with the tool duckencoder.

duckencoder is a cross-platform command-line Java program which converts the Ducky Script syntax into hex files.

For example on a Linux system:

java -jar duckencoder.jar -i exploit.txt -o /media/microsdcard/inject.bin


Simple Ducky Payload Generator
=============================

Also a good option.
https://code.google.com/p/simple-ducky-payload-generator/downloads/list


Wiki
====
https://code.google.com/p/ducky-decode/wiki/Index?tm=6