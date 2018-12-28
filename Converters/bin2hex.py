bindshell = 'bindshell = "'
length = 0
with open("w32-bind-ngs-shellcode.bin", "rb") as f:
    byte = f.read(1)
    while byte != "":
        if len(byte) > 0:
            bindshell += '\\x' + '%02.X' % ord(byte)
            length += 1
        byte = f.read(1)
bindshell += '"'
print "Length: " + str(length)
print bindshell
        
