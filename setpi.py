import os
import subprocess

cmd = ['setenv.bat', 'PI', '3.14']
cmd = 'setenv.bat PI 3.15'

process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
process.wait()
print process.returncode

try:
    os.remove('settmp.bat')
except WindowsError:
    pass