from multiprocessing import Process, Lock

def f():
#    ... do something using "lock" ...
    pass

if __name__ == '__main__':
    lock = Lock()
    for i in range(10):
        Process(target=f).start()

