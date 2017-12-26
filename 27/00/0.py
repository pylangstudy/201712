import asyncio

@asyncio.coroutine
def test():
    print("never scheduled")

test()
