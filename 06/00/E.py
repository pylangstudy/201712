from multiprocessing import Manager
manager = Manager()
l_outer = manager.list([ manager.dict() for i in range(2) ])
d_first_inner = l_outer[0]
d_first_inner['a'] = 1
d_first_inner['b'] = 2
l_outer[1]['c'] = 3
l_outer[1]['z'] = 26
print(l_outer[0])
print(l_outer[1])
