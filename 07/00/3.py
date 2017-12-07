from multiprocessing import Process, Lock

def f(l):
#    ... do something using "l" ...
    pass

if __name__ == '__main__':
    lock = Lock()
    for i in range(10):
        Process(target=f, args=(lock,)).start()

