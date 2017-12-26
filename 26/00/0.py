import asyncio
import requests
async def queue_execution(arg_urls, callback, parallel=2):
    loop = asyncio.get_event_loop()
    queue = asyncio.Queue()

    for u in arg_urls:
        queue.put_nowait(u)

    async def fetch(q):
        while not q.empty():
            u = await q.get()
            future = loop.run_in_executor(None, requests.get, u)
            future.add_done_callback(callback)
            await future

    tasks = [fetch(queue) for i in range(parallel)]
    return await asyncio.wait(tasks)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    results = []
    def store_result(f):
        results.append(f.result())
    loop.run_until_complete(queue_execution([
        "http://www.google.com",
        "http://www.yahoo.com",
        "https://github.com/"
    ], store_result))
    for r in results:
        print("queue execution: {0}".format(r.url))

