import multiprocessing

manager = multiprocessing.Manager()
Global = manager.Namespace()
Global.x = 10
Global.y = 'hello'
Global._z = 12.3    # this is an attribute of the proxy
print(Global)
