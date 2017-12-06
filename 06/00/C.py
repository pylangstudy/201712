from multiprocessing import Manager
manager = Manager()
l = manager.list([i*i for i in range(10)])
print(l)
print(repr(l))
print(l[4])
print(l[2:5])

