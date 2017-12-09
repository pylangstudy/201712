import os
import subprocess
sts = os.system("mycmd" + " myarg")
# becomes
sts = subprocess.call("mycmd" + " myarg", shell=True)

import sys
try:
    retcode = subprocess.call("mycmd" + " myarg", shell=True)
    if retcode < 0:
        print("Child was terminated by signal", -retcode, file=sys.stderr)
    else:
        print("Child returned", retcode, file=sys.stderr)
except OSError as e:
    print("Execution failed:", e, file=sys.stderr)
