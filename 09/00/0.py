import subprocess

subprocess.run(["ls", "-l"])
#subprocess.run("exit 1", shell=True, check=True)#subprocess.CalledProcessError: Command 'exit 1' returned non-zero exit status 1.
subprocess.run(["ls", "-l", "/dev/null"], stdout=subprocess.PIPE)
