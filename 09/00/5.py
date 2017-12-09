import os
import subprocess

cmd = 'ls'
bufsize = 1024

#(child_stdin, child_stdout) = os.popen2(cmd, mode, bufsize)
#print(child_stdin, child_stdout)

p = subprocess.Popen(cmd, shell=True, bufsize=bufsize,
          stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
(child_stdin, child_stdout) = (p.stdin, p.stdout)
print(child_stdin, child_stdout)

