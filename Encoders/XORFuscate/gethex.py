bindshell = ""
with open("shellcode", "rb") as f:
    byte = f.read(1)
    while byte != "":
        if len(byte) > 0:
            bindshell += '%02.X' % ord(byte)
        byte = f.read(1)
print bindshell.decode('hex')