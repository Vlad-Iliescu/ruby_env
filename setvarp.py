import sys

key = sys.argv[1]
value = sys.argv[2]
command = 'setx %s %s\n' % (key, value)
open('settmp.bat', 'w').write(command)
