import subprocess
print(subprocess.getstatusoutput('ls /bin/ls'))
print(subprocess.getstatusoutput('cat /bin/junk'))
print(subprocess.getstatusoutput('/bin/junk'))
print(subprocess.getstatusoutput('/bin/kill $$'))

