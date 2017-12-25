import asyncio

def func():
    lock = asyncio.Lock()
    #...
    yield from lock
    try:
        ...
    finally:
        lock.release()

if __name__ == '__main__':
    func()
