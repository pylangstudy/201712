from subprocess import Popen, PIPE, check_output
# 方法1
p1 = Popen(["dmesg"], stdout=PIPE)
p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
print(output.decode('UTF-8'))
# 方法2
output=check_output("dmesg | grep hda", shell=True)
print(output.decode('UTF-8'))

