import os
from subprocess import Popen, PIPE, STDOUT

cmd = 'ls'
bufsize = 1024

#(child_stdout, child_stdin) = popen2.popen2("somestring", bufsize, mode)
#print(child_stdout, child_stdin)

p = Popen("somestring", shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdout, child_stdin) = (p.stdout, p.stdin)
print(child_stdout, child_stdin)




#(child_stdout, child_stdin) = popen2.popen2(["mycmd", "myarg"], bufsize, mode)
#print(child_stdout, child_stdin)

p = Popen(["mycmd", "myarg"], bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdout, child_stdin) = (p.stdout, p.stdin)
print(child_stdout, child_stdin)
