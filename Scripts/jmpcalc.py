#!/usr/bin/python
# filename: jmpcalc.py
# Author: JollyFrogs
# This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.
# Description: jmpcalc.py is a tool to calculate the opcode of short relative JMPs
#
import sys

def is_decimal(s):
    try: int(s); return True
    except ValueError: return False

def is_hex(s):
    if not (s.startswith("0x") or s.startswith("-0x")): return False
    try: int(s, 16); return True
    except ValueError: return False

def print_usage():
  print("Usage:");print("python jmpcalc.py [relative offset to jmp; use negative number (dec or hex) to indicate a backward jump]")
  print(""); print("Examples:"); print("python jmpcalc.py -16"); print("python jmpcalc.py -0x10"); exit()

if len(sys.argv) != 2: print_usage()
if (not is_decimal(sys.argv[1])) and (not is_hex(sys.argv[1])): print_usage()
if is_decimal(sys.argv[1]): jmpoffset = int(sys.argv[1],10)
if is_hex(sys.argv[1]): jmpoffset = int(sys.argv[1],16)

# Short (two byte) jump value can range from -128 to +127
# Effective jump range is -126 to +129 due to JMP itself being 2 bytes
short_jmp_instruction_size = 2
if jmpoffset == 0: print("Warning: EBFE will result in an endless loop of your JMP instruction")
if jmpoffset == 1: print("Warning: EBFF will try to execute byte 0x01 which is an invalid instruction")

if 2 <= jmpoffset <= 129:
  print("Forward jump by %s (%s) relative from current (JMP) instruction" % (str(jmpoffset),hex(jmpoffset)))
  if jmpoffset == 2: print("EB00 = a simple JMP to the next instruction, similar to two NOP instructions");exit()
  jmprelative = hex(jmpoffset - short_jmp_instruction_size)
  print("JMP OPCODE: EB%02X" % int(jmprelative,16))
  print("JMP OPCODE: \\xEB\\x%02X" % int(jmprelative,16))
  print("JMP OPCODE: 0xEB,0x%02X" % int(jmprelative,16))
  
if -126 <= jmpoffset <= -1:
  print("Backward jump by %s (%s) relative from current (JMP) instruction" % (str(jmpoffset),hex(jmpoffset)))
  jmprelative = hex(256 - short_jmp_instruction_size + jmpoffset)
  print("JMP OPCODE: EB%02X" % int(jmprelative,16))
  print("JMP OPCODE: \\xEB\\x%02X" % int(jmprelative,16))
  print("JMP OPCODE: 0xEB,0x%02X" % int(jmprelative,16))

if 130 <= jmpoffset: print("JMP NEAR and JMP FAR instructions not yet implemented")
if jmpoffset <= -127: print("JMP NEAR and JMP FAR instructions not yet implemented")
