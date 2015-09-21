import os
import re

file = 'dist/ruby222.7z'

import subprocess


cmd = '7za.exe l {0} | FINDSTR "[0-9].D....\>" | FIND /V "\\"'.format(file)

process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
last_line = ''
folder = set()
for line in iter(process.stdout.readline,''):
   folder.add(line.rstrip())

folder_name = map(lambda x: re.sub('\s+', ' ', x), folder).pop().split(' ')[-1]
print last_line

cmd = '7za.exe x {0} -y -o{1}'.format(file, 'dist')
print cmd
process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
for line in iter(process.stdout.readline,''):
    print line.rstrip()
# process.wait()
print process.returncode

print folder_name
os.rename('dist/{0}'.format(folder_name), file.strip('.7z'))
