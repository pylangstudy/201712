from multiprocessing.managers import BaseManager
m = BaseManager(address=('127.0.0.1', 5000), authkey=b'abc')
m.connect()
