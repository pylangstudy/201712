from ctypes.util import find_library
#print(find_library("c"))
#print(find_library("m"))
#print(find_library("bz2"))
#print(find_library("AGL"))
libc = find_library("c")
print(libc)
print(libc.time == libc.time)
print(libc['time'] == libc['time'])
