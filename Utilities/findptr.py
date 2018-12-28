__VERSION__ = '1.0'
__AUTHOR__ = 'salcho - salchoman[]gmail'
import immlib
import getopt
import immutils
from immutils import *

imm = immlib.Debugger()

def main(args):
	found = False
       	try:
                offset = int(args.pop())
        except:
                imm.log("%s -> %d" % (arg,offset))
                return "[-] Invalid or absent offset"

        arg = ' '.join(args)
        arg = arg.replace('/', '\n')
	if not len(args):
		imm.log("[-] findptr <instrucciones> <offset>")
		imm.log("[-] separadas por /")
		return ""

	imm.log("[*] Buscando %s..." % arg)
	res = imm.search(imm.assemble(arg))
	imm.log("[*] %d resultados" % len(res))

	table = imm.createTable('Pointers table', ['Instruction','Address w/offset','Original addr'])
	for r in res:
		#imm.log("Encontro %s en 0x%08X " % (arg, r) , address = r)
		addr = "%08X" % r
		hexStr = ''
		for i in range(len(addr), -1, -2):
			hexStr += addr[i:i+2]

		hexBytes = []
		for i in range(0, len(hexStr), 2):
                        hexBytes.append(chr(int(hexStr[i:i+2],16)))
                        
                search = ''.join(hexBytes)
		#imm.log("Buscando opcodes %s..." % hexStr, address = int(hexStr, 16))
		pointers = imm.search(search)
		#imm.log("%d resultados" % len(res))
		if len(pointers):
                        found = True

        		for r in pointers:
                		opc = imm.disasm(r)
                        	opc = opc.getDisasm()
                        	table.add(0,["%s"%opc,"0x%08X"%(r+offset),"0x%08X"%r])
                                #imm.log("[***] %s at 0x%08X" % (opc, r), address = r)
        			imm.updateLog()

        if not found:
                imm.log("[-] No se encontro ningun puntero :(");
                
	return ""
