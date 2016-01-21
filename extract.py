import os
import re

file = "D:\\dev\\python\\ruby_env\\dist\\2.0.0\\ruby_2_0_0_p247_x64.7z"
# file = 'dist/2.0.0/ruby_2_0_0_p247_x64.7z'

import subprocess

cmd = '7za.exe l {0} | FINDSTR "[0-9].D....\>" | FIND /V "\\"'.format(file)
# cmd = ['7za.exe l {0}'.format(file)]

stdoutdata = subprocess.getoutput(cmd)
print(stdoutdata)
exit(0)

folder = set()
print(cmd)
with subprocess.Popen(cmd, stdout=subprocess.PIPE) as process:
    l = process.stdout.read()

print(l)
exit(0)

process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
last_line = ''
folder = set()
for line in iter(process.stdout.readline, ''):
    folder.add(line.rstrip())

folder
exit(0)
folder_name = map(lambda x: re.sub('\s+', ' ', x), folder).pop().split(' ')[-1]
print(last_line)
exit(0)

cmd = '7za.exe x {0} -y -o{1}'.format(file, 'dist')
print(cmd)
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
for line in iter(process.stdout.readline, ''):
    print(line.rstrip())
# process.wait()
print(process.returncode)

print(folder_name)
os.rename('dist/{0}'.format(folder_name), file.strip('.7z'))
