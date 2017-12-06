from multiprocessing.managers import BaseManager
manager = BaseManager(address=('', 50000), authkey=b'abc')
server = manager.get_server()
server.serve_forever()
