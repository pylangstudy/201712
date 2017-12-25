import asyncio

def func():
    lock = asyncio.Lock()
    #...
    with (yield from lock):
        pass

if __name__ == '__main__':
    func()
