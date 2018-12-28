import sys

if len(sys.argv) == 3:
    first = int(sys.argv[1], 16)
    second = int(sys.argv[2], 16)
    if first > second:
        print str(first - second + 1) + " byte(s) of space"
    else:
        print str(second - first + 1) + " byte(s) of space"
else:
    print "Usage: python memory-space-calc.py 1035F090 1035F100"
    
