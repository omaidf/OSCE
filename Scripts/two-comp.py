from sys import argv, stdout


def twos_comp(bytes):
    to_return = 0xffffffff - int(bytes,16) + 1
    return "%0.8x" % to_return


if len(argv) < 2:
    print "[-] Missing arguments: ./%s <hex value>" % argv[0]
    print "       Example: ./%s 41424344" % argv[0]
    exit()


shellcode = argv[1]

print twos_comp(shellcode)