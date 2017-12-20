# [18.5.3. タスクとコルーチン](https://docs.python.jp/3/library/asyncio-task.html)

< [18.5. asyncio — 非同期 I/O、イベントループ、コルーチンおよびタスク](https://docs.python.jp/3/library/asyncio.html) < [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

* Source code: [Lib/asyncio/tasks.py](https://github.com/python/cpython/tree/3.6/Lib/asyncio/tasks.py)
* Source code: [Lib/asyncio/coroutines.py](https://github.com/python/cpython/tree/3.6/Lib/asyncio/coroutines.py)

## [18.5.3.1. コルーチン](https://docs.python.jp/3/library/asyncio-task.html#coroutines)

> Coroutines used with asyncio may be implemented using the async def statement, or by using generators. The async def type of coroutine was added in Python 3.5, and is recommended if there is no need to support older Python versions.

> Generator-based coroutines should be decorated with @asyncio.coroutine, although this is not strictly enforced. The decorator enables compatibility with async def coroutines, and also serves as documentation. Generator-based coroutines use the yield from syntax introduced in PEP 380, instead of the original yield syntax.

> 単語 "コルーチン" は単語 "ジェネレーター" のように、(関連はしていますが) 異なる 2 つの概念で使用されます:

* コルーチンを定義した関数 (async def を使用するか @asyncio.coroutine でデコレートされた関数定義)。 曖昧さを避ける際は コルーチン関数 と呼びます (iscoroutinefunction() は True を返します)。
* コルーチン関数の呼び出しによって取得されたオブジェクト。このオブジェクトは、いつかは完了する計算または I/O 操作 (通常はその組み合わせ) を表します。曖昧さの解消が必要な場合はこれを コルーチンオブジェクト (iscoroutine() が True を返す) と呼びます。

> コルーチンができること:

* result = await future or result = yield from future – suspends the coroutine until the future is done, then returns the future’s result, or raises an exception, which will be propagated. (If the future is cancelled, it will raise a CancelledError exception.) Note that tasks are futures, and everything said about futures also applies to tasks.
* result = await coroutine or result = yield from coroutine – wait for another coroutine to produce a result (or raise an exception, which will be propagated). The coroutine expression must be a call to another coroutine.
* return expression – produce a result to the coroutine that is waiting for this one using await or yield from.
* raise exception – raise an exception in the coroutine that is waiting for this one using await or yield from.

> Calling a coroutine does not start its code running – the coroutine object returned by the call doesn’t do anything until you schedule its execution. There are two basic ways to start it running: call await coroutine or yield from coroutine from another coroutine (assuming the other coroutine is already running!), or schedule its execution using the ensure_future() function or the AbstractEventLoop.create_task() method.

> コルーチン (およびタスク) はイベントループが実行中の場合にのみ起動できます。

@asyncio.coroutine|Decorator to mark generator-based coroutines. This enables the generator use yield from to call async def coroutines, and also enables the generator to be called by async def coroutines, for instance using an await expression.

## [18.5.3.1.1. 例: Hello World コルーチン](https://docs.python.jp/3/library/asyncio-task.html#example-hello-world-coroutine)

> "Hello World" と表示するコルーチンの例:

```python
import asyncio

async def hello_world():
    print("Hello World!")

loop = asyncio.get_event_loop()
# Blocking call which returns when the hello_world() coroutine is done
loop.run_until_complete(hello_world())
loop.close()
```

> 参考

> The Hello World with call_soon() example uses the AbstractEventLoop.call_soon() method to schedule a callback.

## [18.5.3.1.2. 例: 現在の日時を表示するコルーチン](https://docs.python.jp/3/library/asyncio-task.html#example-coroutine-displaying-the-current-date)

> sleep() 関数を用いて現在の時刻を5秒間、毎秒表示するコルーチンの例:

```python
import asyncio
import datetime

async def display_date(loop):
    end_time = loop.time() + 5.0
    while True:
        print(datetime.datetime.now())
        if (loop.time() + 1.0) >= end_time:
            break
        await asyncio.sleep(1)

loop = asyncio.get_event_loop()
# Blocking call which returns when the display_date() coroutine is done
loop.run_until_complete(display_date(loop))
loop.close()
```

> 参考

> The display the current date with call_later() example uses a callback with the AbstractEventLoop.call_later() method.

## [18.5.3.1.3. 例: コルーチンのチェーン](https://docs.python.jp/3/library/asyncio-task.html#example-chain-coroutines)

> コルーチンをチェーンする例です:

```python
import asyncio

async def compute(x, y):
    print("Compute %s + %s ..." % (x, y))
    await asyncio.sleep(1.0)
    return x + y

async def print_sum(x, y):
    result = await compute(x, y)
    print("%s + %s = %s" % (x, y, result))

loop = asyncio.get_event_loop()
loop.run_until_complete(print_sum(1, 2))
loop.close()
```

> compute() は print_sum() にチェーンされます: print_sum() コルーチンは compute() が完了するまで待ちます。

この例のシーケンス図です:

> ../_images/tulip_coro.png

> The "Task" is created by the AbstractEventLoop.run_until_complete() method when it gets a coroutine object instead of a task.

> The diagram shows the control flow, it does not describe exactly how things work internally. For example, the sleep coroutine creates an internal future which uses AbstractEventLoop.call_later() to wake up the task in 1 second.

## [18.5.3.2. InvalidStateError](https://docs.python.jp/3/library/asyncio-task.html#invalidstateerror)

属性|概要
----|----
exception asyncio.InvalidStateError|操作はこの状態では許可されません。

## [18.5.3.3. TimeoutError](https://docs.python.jp/3/library/asyncio-task.html#timeouterror)

属性|概要
----|----
exception asyncio.TimeoutError|操作は与えられた期限を超えました。

## [18.5.3.4. フューチャー](https://docs.python.jp/3/library/asyncio-task.html#future)

属性|概要
----|----
class asyncio.Future(*, loop=None)|このクラスは concurrent.futures.Future と ほぼ 互換です。
cancel()|フューチャとスケジュールされたコールバックをキャンセルします。
cancelled()|フューチャがキャンセルされていた場合 True を返します。
done()|Return True if the future is done.
result()|このフューチャが表す結果を返します。
exception()|このフューチャで設定された例外を返します。
add_done_callback(fn)|フューチャが終了したときに実行するコールバックを追加します。
remove_done_callback(fn)|"終了時に呼び出す" リストからコールバックのすべてのインスタンスを除去します。
set_result(result)|フューチャの終了をマークしその結果を設定します。
set_exception(exception)|フューチャの終了をマークし例外を設定します。

### [18.5.3.4.1. 例: run_until_complete() を使ったフューチャ](https://docs.python.jp/3/library/asyncio-task.html#example-future-with-run-until-complete)

> Future と コルーチン関数 を組み合わせた例:

```python
import asyncio

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

loop = asyncio.get_event_loop()
future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))
loop.run_until_complete(future)
print(future.result())
loop.close()
```

> The coroutine function is responsible for the computation (which takes 1 second) and it stores the result into the future. The run_until_complete() method waits for the completion of the future.

> 注釈

> The run_until_complete() method uses internally the add_done_callback() method to be notified when the future is done.

### [18.5.3.4.2. 例: run_forever() を使ったフューチャ](https://docs.python.jp/3/library/asyncio-task.html#example-future-with-run-forever)

> 上の例を Future.add_done_callback() メソッド使って制御フローを明示して書くこともできます:

```python
import asyncio

async def slow_operation(future):
    await asyncio.sleep(1)
    future.set_result('Future is done!')

def got_result(future):
    print(future.result())
    loop.stop()

loop = asyncio.get_event_loop()
future = asyncio.Future()
asyncio.ensure_future(slow_operation(future))
future.add_done_callback(got_result)
try:
    loop.run_forever()
finally:
    loop.close()
```

> この例では slow_operation() を got_result() にリンクするために future を用いています。slow_operation() が終了したとき got_result() が結果と供に呼ばれます。

## [18.5.3.5. タスク](https://docs.python.jp/3/library/asyncio-task.html#task)

属性|概要
----|----
class asyncio.Task(coro, *, loop=None)|コルーチン の実行をスケジュールします: それをフューチャ内にラップします。タスクは Future のサブクラスです。
classmethod all_tasks(loop=None)|イベントループ loop のすべてのタスクの集合を返します。
classmethod current_task(loop=None)|イベントループ内で現在実行中のタスクまたは None を返します。
cancel()|このタスクのキャンセルを自身で要求します。
get_stack(*, limit=None)|このタスクのコルーチンのスタックフレームのリストを返します。
print_stack(*, limit=None, file=None)|このタスクのコルーチンのスタックあるいはトレースバックを出力します。

### [18.5.3.5.1. 例: タスクの並列実行](https://docs.python.jp/3/library/asyncio-task.html#example-parallel-execution-of-tasks)

> 3 個のタスク (A, B, C) を並列に実行する例です:

```python
import asyncio

async def factorial(name, number):
    f = 1
    for i in range(2, number+1):
        print("Task %s: Compute factorial(%s)..." % (name, i))
        await asyncio.sleep(1)
        f *= i
    print("Task %s: factorial(%s) = %s" % (name, number, f))

loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    factorial("A", 2),
    factorial("B", 3),
    factorial("C", 4),
))
loop.close()
```

> 出力:

```
Task A: Compute factorial(2)...
Task B: Compute factorial(2)...
Task C: Compute factorial(2)...
Task A: factorial(2) = 2
Task B: Compute factorial(3)...
Task C: Compute factorial(3)...
Task B: factorial(3) = 6
Task C: Compute factorial(4)...
Task C: factorial(4) = 24
```

> タスクは作成されたときに実行を自動的にスケジュールされます。イベントループはすべてのタスクが終了したときに停止します。

## [18.5.3.6. タスク関数](https://docs.python.jp/3/library/asyncio-task.html#task-functions)

> 注釈

> In the functions below, the optional loop argument allows explicitly setting the event loop object used by the underlying task or coroutine. If it’s not provided, the default event loop is used.

属性|概要
----|----
asyncio.as_completed(fs, *, loop=None, timeout=None)|その値のイテレーターか、待機中のときは Future インスタンスを返します。
asyncio.ensure_future(coro_or_future, *, loop=None)|コルーチンオブジェクト の実行をスケジュールします: このときフューチャにラップします。Task オブジェクトを返します。
asyncio.async(coro_or_future, *, loop=None)|ensure_future() への非推奨なエイリアスです。
asyncio.wrap_future(future, *, loop=None)|Wrap a concurrent.futures.Future object in a Future object.
asyncio.gather(*coros_or_futures, loop=None, return_exceptions=False)|与えられたコルーチンオブジェクトあるいはフューチャからの結果を一つにまとめたフューチャを返します。
asyncio.iscoroutine(obj)|Return True if obj is a coroutine object, which may be based on a generator or an async def coroutine.
asyncio.iscoroutinefunction(func)|Return True if func is determined to be a coroutine function, which may be a decorated generator function or an async def function.
asyncio.run_coroutine_threadsafe(coro, loop)|Submit a coroutine object to a given event loop.
coroutine asyncio.sleep(delay, result=None, *, loop=None)|与えられた時間 (秒) 後に完了する コルーチン を作成します。result が与えられた場合、コルーチン完了時にそれが呼び出し元に返されます。
asyncio.shield(arg, *, loop=None)|フューチャを待機しキャンセル処理から保護します。
coroutine asyncio.wait_for(fut, timeout, *, loop=None)|単一の Future または コルーチンオブジェクト を期限付きで待機します。timeout が None の場合、フューチャが完了するまでブロックします。

