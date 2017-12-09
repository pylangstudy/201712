import os
import subprocess

pid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")
print(pid)
pid = subprocess.Popen(["/bin/mycmd", "myarg"]).pid
print(pid)

retcode = os.spawnlp(os.P_WAIT, "/bin/mycmd", "mycmd", "myarg")
print(retcode)
retcode = subprocess.call(["/bin/mycmd", "myarg"])
print(retcode)

print(os.spawnvp(os.P_NOWAIT, path, args))
print(subprocess.Popen([path] + args[1:]))

print(os.spawnlpe(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg", env))
print(subprocess.Popen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"}))


