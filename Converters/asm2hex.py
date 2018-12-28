from binascii import unhexlify
import binascii
import sys
import os
from shell import shell
import time


if len (sys.argv) != 2 :
    print "\r"
    print "Read Assembly, compile and output shellcode in hex format"
    print "Usage: python asm2hex.py winexec.asm\r\n"
    sys.exit (1)

asmfile = sys.argv[1]
binfile = asmfile[:-4]

genbin = 'nasm %s' % asmfile
delbin = 'rm %s' % binfile
shell(genbin)



# writeasm = shell('nasm %s')
# print "Creating shellcode..."

bindshell = 'shellcode = "'
length = 0
with open(binfile, "rb") as f:
    byte = f.read(1)
    while byte != "":
        if len(byte) > 0:
            bindshell += '\\x' + '%02.X' % ord(byte)
            length += 1
        byte = f.read(1)
bindshell += '"'
print "Length: %s bytes\n " % str(length)
print bindshell

shell(delbin)
