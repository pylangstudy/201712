import ctypes
#http://www22.atpages.jp/~cncc/download/SofTalk/.NET/stn019329.zip
#Linux上でWindows用の.dllファイルは読み込めない
ctypes.CDLL('./softalk/dll/aqt10/AquesTalk.dll')#OSError: ./softalk/dll/aqt10/AquesTalk.dll: invalid ELF header
ctypes.WinDLL('./softalk/dll/aqt10/AquesTalk.dll')#AttributeError: module 'ctypes' has no attribute 'WinDLL'

