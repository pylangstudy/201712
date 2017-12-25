import asyncio

def func():
    lock = asyncio.Lock()

    if not lock.locked():
        yield from lock
    else:
        # lock is acquired
        ...

if __name__ == '__main__':
    func()
