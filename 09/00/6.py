import os
import subprocess

cmd = 'ls'
bufsize = 1024

"""
(child_stdin,
 child_stdout,
 child_stderr) = os.popen3(cmd, mode, bufsize)
print(child_stdin, child_stdout, child_stderr)
"""
p = subprocess.Popen(cmd, shell=True, bufsize=bufsize,
          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
(child_stdin,
 child_stdout,
 child_stderr) = (p.stdin, p.stdout, p.stderr)
print(child_stdin, child_stdout, child_stderr)






#(child_stdin, child_stdout_and_stderr) = os.popen4(cmd, mode, bufsize)
#print(child_stdin, child_stdout_and_stderr)

p = subprocess.Popen(cmd, shell=True, bufsize=bufsize,
          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
(child_stdin, child_stdout_and_stderr) = (p.stdin, p.stdout)
print(child_stdin, child_stdout_and_stderr)






pipe = os.popen(cmd, 'w')
#...
rc = pipe.close()
if rc is not None and rc >> 8:
    print("There were some errors")

process = subprocess.Popen(cmd, stdin=subprocess.PIPE)
#...
process.stdin.close()
if process.wait() != 0:
    print("There were some errors")

