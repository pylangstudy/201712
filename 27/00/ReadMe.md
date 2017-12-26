# [18.5.9. asyncio での開発](https://docs.python.jp/3/library/asyncio-dev.html)

< [18.5. asyncio — 非同期 I/O、イベントループ、コルーチンおよびタスク](https://docs.python.jp/3/library/asyncio.html) < [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

> 非同期プログラミングは古典的な "逐次" プログラミングとは異なります。このページでは非同期プログラミングで陥りやすい落とし穴の一覧とその回避方法について説明しています。

## [18.5.9.1. asyncio のデバッグモード](https://docs.python.jp/3/library/asyncio-dev.html#debug-mode-of-asyncio)

> asyncio の実装では、パフォーマンスが重視されています。非同期コードの開発を行いやすくするには、 デバッグモード を有効にするとよいかもしれません。

> アプリケーションで全てのデバッグチェックを有効にするには:

* 環境変数 PYTHONASYNCIODEBUG を 1 に設定するか、 AbstractEventLoop.set_debug() を呼び出すと、asyncio  デバッグモードがグローバルに有効になります。
* asyncio logger のトップレベルを logging.DEBUG に設定します。例えば、起動時に logging.basicConfig(level=logging.DEBUG) を呼び出します。
* warnings モジュールを構成して、 ResourceWarning 警告が表示されるようにします。例えば、Python の -Wdefault コマンドラインオプションを使用して、それらを表示します。

> デバッグチェックの例:

* 定義されているが "yielded from" されなかったコルーチン のログを取ります
* 誤ったスレッドから呼ばれた場合、 call_soon() や call_at() メソッドが例外を送出します
* セレクターの実行時間のログを取ります
* 実行時間が 100 ms を超えるコールバックのログ。AbstractEventLoop.slow_callback_duration 属性には "遅い" コールバックとみなす最小時間を秒で指定できます。
* トランスポートとイベントループが 明示的に閉じられなかった 場合、 ResourceWarning 警告が出ます。

> 参考

> AbstractEventLoop.set_debug() メソッドならびに asyncio logger。

## [18.5.9.2. 取り消し](https://docs.python.jp/3/library/asyncio-dev.html#cancellation)

> Cancellation of tasks is not common in classic programming. In asynchronous programming, not only is it something common, but you have to prepare your code to handle it.

> Future おびタスクは、それらの Future.cancel() メソッドを呼び出すことで、明示的にキャンセルすることができます。wait_for() 関数は、タイムアウト発生時に、待機中のタスクをキャンセルします。タスクを間接的にキャンセルすることができる使用例は、他にも数多くあります。

> Future がキャンセルされた場合、Future の set_result() または set_exception() メソッドは呼び出さないでください。例外を送出して、失敗してしまいます。例えば、以下のように書いてください。

```python
if not fut.cancelled():
    fut.set_result('done')
```

> AbstractEventLoop.call_soon() で、Future の set_result() メソッドまたは set_exception() メソッドの呼び出しを直接スケジュールしないでください。Future は、そのメソッドが呼び出される前にキャンセルされる場合があります。

> Future を待機する場合、Future がキャンセルされているかどうかを早い段階で確認し、無駄な操作を防いでください。以下に例を示します。

```python
@coroutine
def slow_operation(fut):
    if fut.cancelled():
        return
    # ... slow computation ...
    yield from fut
    # ...
```

> shield() 関数も、キャンセルを無視するために使用できます。

## [18.5.9.3. 並行処理とマルチスレッド処理](https://docs.python.jp/3/library/asyncio-dev.html#concurrency-and-multithreading)

イベントループは 1 個のスレッド内で実行し、同じスレッド内ですべてのコールバックとタスクを実行します。1 個のタスクがイベントループ内で実行される間、他のタスクは同じスレッド内で実行されることはありません。ただし、タスクが yield from を使用するとそのタスクはサスペンドされ、イベントループは次のタスクを実行します。

異なるスレッドからコールバックをスケジュールする場合、 AbstractEventLoop.call_soon_threadsafe() メソッドを使用してください。例:

```python
loop.call_soon_threadsafe(callback, *args)
```

> ほとんどの asyncio オブジェクトはスレッドセーフではありません。イベントループの外からオブジェクトにアクセスしていないかどうかだけに注意してください。例えばフューチャーをキャンセルする場合にその Future.cancel() メソッドを直接呼び出すのではなく以下のようにします:

```python
loop.call_soon_threadsafe(fut.cancel)
```

> シグナルの処理やサブプロセスの実行を行うには、イベントループはメインスレッド内で実行しなければなりません。

> 別のスレッドからコルーチンオブジェクトをスケジュールする場合は、 run_coroutine_threadsafe() メソッドを使用してください。 run_coroutine_threadsafe() は結果にアクセスするための concurrent.futures.Future を返します:

```python
future = asyncio.run_coroutine_threadsafe(coro_func(), loop)
result = future.result(timeout)  # Wait for the result with a timeout
```

> AbstractEventLoop.run_in_executor() メソッドをスレッドプール実行者とともに使用することで、イベントループのスレッドをブロックすることなく、別のスレッド内でコールバックを実行できます。

> 参考

> 同期プリミティブ 節にはタスクの同期法が書かれています。

> サブプロセスとスレッド 節では別スレッドからサブプロセスを実行する際の asyncio の限界を列挙しています。

## [18.5.9.4. ブロック関数を正しく扱う](https://docs.python.jp/3/library/asyncio-dev.html#handle-blocking-functions-correctly)

> ブロック関数を直接呼び出してはなりません。例えば、関数が 1 秒間ブロックした場合、他のタスクには 1 秒間の遅延が発生します。これは反応性において重大な影響が発生します。

> ネットワークとサブプロセスには、asyncio モジュールは プロトコル のような高水準 API を提供しています。

> 実行者を使用することで、イベントループのスレッドをブロックすることなく、別のスレッドや別のサブプロセスでタスクを実行できます。AbstractEventLoop.run_in_executor() メソッドを参照してください。

> 参考

> 遅延呼び出し 節でイベントループで時間を扱う手順の詳細を説明しています。

## [18.5.9.5. ログ記録](https://docs.python.jp/3/library/asyncio-dev.html#logging)

> asyncio モジュールは logging モジュールとともにロガー 'asyncio' の情報のログを記録します。

> asyncio モジュールのデフォルトのログレベルは、 logging.INFO です。asyncio にそれほどの冗長性を求めないユーザは、ログレベルを変更できます。例えば、レベルを logging.WARNING に変更するには、以下のようにします。

```python
```
logging.getLogger('asyncio').setLevel(logging.WARNING)

## [18.5.9.6. スケジュールされなかったコルーチンオブジェクトの検出](https://docs.python.jp/3/library/asyncio-dev.html#detect-coroutine-objects-never-scheduled)

> コルーチン関数が呼び出されてもその結果が ensure_future() や AbstractEventLoop.create_task() メソッドに渡されない場合、そのコルーチンオブジェクトの実行がスケジュールされることはなく、これはおそらくバグです。 asyncio のデバッグモードの有効化 により 警告のログ記録 を行うことでそれを検出できます。

> バグの例:

```python
import asyncio

@asyncio.coroutine
def test():
    print("never scheduled")

test()
```

> デバッグモードの出力:

```sh
Coroutine test() at test.py:3 was never yielded from
Coroutine object created at (most recent call last):
  File "test.py", line 7, in <module>
    test()
```

> これを修正するには、そのコルーチンオブジェクトで ensure_future() 関数か AbstractEventLoop.create_task() メソッドを呼び出します。

> 参考

> 未完のタスクの破棄。

## [18.5.9.7. 未処理の例外の検出](https://docs.python.jp/3/library/asyncio-dev.html#detect-exceptions-never-consumed)

> Python は通常未処理の例外には sys.displayhook() を呼び出します。 Future.set_exception() が呼び出されたものの処理されなかった場合、 sys.displayhook() が呼び出されません。 代わりに、フューチャーがガベージコレクションで削除されたとき、例外発生場所のトレースバックとともに ログが記録され ます。

> 未処理の例外の例:

```python
import asyncio

@asyncio.coroutine
def bug():
    raise Exception("not consumed")

loop = asyncio.get_event_loop()
asyncio.ensure_future(bug())
loop.run_forever()
loop.close()
```

> 出力:

```sh
Task exception was never retrieved
future: <Task finished coro=<coro() done, defined at asyncio/coroutines.py:139> exception=Exception('not consumed',)>
Traceback (most recent call last):
  File "asyncio/tasks.py", line 237, in _step
    result = next(coro)
  File "asyncio/coroutines.py", line 141, in coro
    res = func(*args, **kw)
  File "test.py", line 5, in bug
    raise Exception("not consumed")
Exception: not consumed
```

> asyncio のデバッグモードの有効化 によりタスクが生成したトレースバックを取得できます。デバッグモードの出力は以下のようになります:

```sh
Task exception was never retrieved
future: <Task finished coro=<bug() done, defined at test.py:3> exception=Exception('not consumed',) created at test.py:8>
source_traceback: Object created at (most recent call last):
  File "test.py", line 8, in <module>
    asyncio.ensure_future(bug())
Traceback (most recent call last):
  File "asyncio/tasks.py", line 237, in _step
    result = next(coro)
  File "asyncio/coroutines.py", line 79, in __next__
    return next(self.gen)
  File "asyncio/coroutines.py", line 141, in coro
    res = func(*args, **kw)
  File "test.py", line 5, in bug
    raise Exception("not consumed")
Exception: not consumed
```

> この問題を解決するには異なるオプションがあります。最初のオプションでは、別のコルーチン内でコルーチンをチェーンし、古典的な try/except を使用します:

```python
@asyncio.coroutine
def handle_exception():
    try:
        yield from bug()
    except Exception:
        print("exception consumed")

loop = asyncio.get_event_loop()
asyncio.ensure_future(handle_exception())
loop.run_forever()
loop.close()
```

> AbstractEventLoop.run_until_complete() 関数を使う別のオプション:

```python
task = asyncio.ensure_future(bug())
try:
    loop.run_until_complete(task)
except Exception:
    print("exception consumed")
```

> 参考

> Future.exception() メソッド。

## [18.5.9.8. コルーチンを正しくチェーンする](https://docs.python.jp/3/library/asyncio-dev.html#chain-coroutines-correctly)

> コルーチン関数が別のコルーチン関数かタスクを呼び出すとき、それらは yield from で明示的にチェーンされなければなりません。そうされなかった場合、逐次的に実行されることは保証されません。

> asyncio.sleep() を使って処理速度の低下をシミュレートする異なるバグの例:

```python
import asyncio

@asyncio.coroutine
def create():
    yield from asyncio.sleep(3.0)
    print("(1) create file")

@asyncio.coroutine
def write():
    yield from asyncio.sleep(1.0)
    print("(2) write into file")

@asyncio.coroutine
def close():
    print("(3) close file")

@asyncio.coroutine
def test():
    asyncio.ensure_future(create())
    asyncio.ensure_future(write())
    asyncio.ensure_future(close())
    yield from asyncio.sleep(2.0)
    loop.stop()

loop = asyncio.get_event_loop()
asyncio.ensure_future(test())
loop.run_forever()
print("Pending tasks at exit: %s" % asyncio.Task.all_tasks(loop))
loop.close()
```

> 予想される出力:

```sh
(1) create file
(2) write into file
(3) close file
Pending tasks at exit: set()
```

> 実際の出力:

```sh
(3) close file
(2) write into file
Pending tasks at exit: {<Task pending create() at test.py:7 wait_for=<Future pending cb=[Task._wakeup()]>>}
Task was destroyed but it is pending!
task: <Task pending create() done at test.py:5 wait_for=<Future pending cb=[Task._wakeup()]>>
```

> create() が完了する前か、write() を呼び出す前に close() が呼び出されたか、その一方でコルーチン関数が create()、write()。close() の順で呼び出された場合、ループは停止します。

> この問題を解決するには、タスクは yield from でマークされなければなりません:

```python
@asyncio.coroutine
def test():
    yield from asyncio.ensure_future(create())
    yield from asyncio.ensure_future(write())
    yield from asyncio.ensure_future(close())
    yield from asyncio.sleep(2.0)
    loop.stop()
```

> あるいは、asyncio.ensure_future() を使いません:

```python
@asyncio.coroutine
def test():
    yield from create()
    yield from write()
    yield from close()
    yield from asyncio.sleep(2.0)
    loop.stop()
```

## [18.5.9.9. 未完のタスクの破棄](https://docs.python.jp/3/library/asyncio-dev.html#pending-task-destroyed)

> 未完のタスクが破棄された場合、それがラップした コルーチン は完了しません。これがおそらくバグであり、そのため警告がログに記録されます。

ログの例:

```sh
Task was destroyed but it is pending!
task: <Task pending coro=<kill_me() done, defined at test.py:5> wait_for=<Future pending cb=[Task._wakeup()]>>
```

> asyncio のデバッグモードの有効化 をすることで、タスクが生成された場所でトレースバックを取得できます。以下はデバッグモードでログを記録する例です。

```sh
Task was destroyed but it is pending!
source_traceback: Object created at (most recent call last):
  File "test.py", line 15, in <module>
    task = asyncio.ensure_future(coro, loop=loop)
task: <Task pending coro=<kill_me() done, defined at test.py:5> wait_for=<Future pending cb=[Task._wakeup()] created at test.py:7> created at test.py:15>
```

> 参考

> スケジュールされなかったコルーチンオブジェクトの検出。

## [18.5.9.10. トランスポートとイベントループを閉じる](https://docs.python.jp/3/library/asyncio-dev.html#close-transports-and-event-loops)

> もはやトランスポートの必要がない場合、その close() メソッドを呼び出して、リソースを解放します。イベントループも、明示的に閉じなければなりません。

> トランスポートまたはイベントループが明示的に閉じられない場合、デストラクタ内で ResourceWarning 警告が送出されます。デフォルトでは、 ResourceWarning 警告は無視されます。asyncio のデバッグモード セクションで、それらを表示する方法を説明します。

