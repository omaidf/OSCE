from binascii import unhexlify
import binascii
import sys
import os
from capstone import *

chars = []
goodchars = []
converted = ""
characters =""
md = Cs(CS_ARCH_X86, CS_MODE_32)

badchars = ("\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3c\x3d\x3e\x3f\x40"
"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")

chars+=['01', '02', '03', '04', '05', '06']
chars+=['07', '08', '09', '0a', '0b', '0c', '0d', '0e', 'a4', '10', '11', '12', '13', 'b6', 'a7', '16']
chars+=['17', '18', '19', '1a', '1b', '1c', '1d', '1e', '1f', '20', '21', '22', '23', '24', '25', '26']
chars+=['27', '28', '29', '2a', '2b', '2c', '2d', '2e', '5c', '30', '31', '32', '33', '34', '35', '36']
chars+=['37', '38', '39', '3a', '3c', '3d', '3e', '3f', '40', '41', '42', '43', '44', '45', '46', '47']
chars+=['48', '49', '4a', '4b', '4c', '4d', '4e', '4f', '50', '51', '52', '53', '54', '55', '56', '57']
chars+=['58', '59', '5a', '5b', '5d', '5e', '5f', '60', '61', '62', '63', '64', '65', '66', '67', '68']
chars+=['69', '6a', '6b', '6c', '6d', '6e', '6f', '70', '71', '72', '73', '74', '75', '76', '77', '78']
chars+=['79', '7a', '7b', '7c', '7d', '7e', '7f', 'c7', 'fc', 'e9', 'e2', 'e4', 'e0', 'e5', 'e7', 'ea']
chars+=['eb', 'e8', 'ef', 'ee', 'ec', 'c4', 'c5', 'c9', 'e6', 'c6', 'f4', 'f6', 'f2', 'fb', 'f9', 'ff']
chars+=['d6', 'dc', 'a2', 'a3', 'a5', '50', '83', 'e1', 'ed', 'f3', 'fa', 'f1', 'd1', 'aa', 'ba', 'bf']
chars+=['ac', 'ac', 'bd', 'bc', 'a1', 'ab', 'bb', 'a6', 'a6', 'a6', 'a6', 'a6', 'a6', 'a6', '2b', '2b']
chars+=['a6', 'a6', '2b', '2b', '2b', '2b', '2b', '2b', '2d', '2d', '2b', '2d', '2b', 'a6', 'a6', '2b']
chars+=['2b', '2d', '2d', 'a6', '2d', '2b', '2d', '2d', '2d', '2d', '2b', '2b', '2b', '2b', '2b', '2b']
chars+=['2b', '2b', 'a6', '5f', 'a6', 'a6', 'af', '61', 'df', '47', '70', '53', '73', 'b5', '74', '46']
chars+=['54', '4f', '64', '38', '66', '65', '6e', '3d', 'b1', '3d', '3d', '28', '29', 'f7', '98', 'b0']
chars+=['b7', 'b7', '76', '6e', 'b2', 'a6', 'a0']

for char in chars:
    converted += char
converted = binascii.unhexlify(converted)

def BadChars(original,result):
    for old,new in zip(original,result):
        if old == new:
            print old.encode('hex')
            md = Cs(CS_ARCH_X86, CS_MODE_32)
            for insn in md.disasm(old, 0x1000):
                print "%s : \t%s\t%s " %(old.encode('hex'), insn.mnemonic, insn.op_str)
        else:
            # md = Cs(CS_ARCH_X86, CS_MODE_32)
            # for insn in md.disasm(new, 0x1000):
                # print "%s : \t%s\t%s " %(new.encode('hex'), insn.mnemonic, insn.op_str)
            #this line prints the conversion table
            print "%s ==> %s" % (old.encode('hex'),new.encode('hex')) 
            #this line allows you to programmatically replace bad characters without converting them
            # print "payload = payload.replace('\\x%s','\\x%s')" % (old.encode('hex'),new.encode('hex'))



def printop(char):
    hexchar = binascii.unhexlify(char)
    # print char
    md = Cs(CS_ARCH_X86, CS_MODE_32)
    for insn in md.disasm(hexchar, 0x00):
        print "%s : \t%s\t%s " %(char, insn.mnemonic, insn.op_str)


for char in chars:
    printop(char)
    # Prints all possible chars from MONA3 Output

BadChars(badchars,converted)
