# [18.5.7. 同期プリミティブ](https://docs.python.jp/3/library/asyncio-sync.html)

< [18.5. asyncio — 非同期 I/O、イベントループ、コルーチンおよびタスク](https://docs.python.jp/3/library/asyncio.html) < [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

* Source code: [Lib/asyncio/locks.py](https://github.com/python/cpython/tree/3.6/Lib/asyncio/locks.py)

> asyncio lock API は threading モジュールのクラス (Lock, Event, Condition, Semaphore, BoundedSemaphore) に近くなるよう設計されましたが、 timeout 引数はありません。 asyncio.wait_for() 関数を用いてタイムアオウト後にタスクをキャンセルすることが出来ます。

## [18.5.7.1. ロック](https://docs.python.jp/3/library/asyncio-sync.html#locks)

### [18.5.7.1.1. Lock](https://docs.python.jp/3/library/asyncio-sync.html#lock)

属性|概要
----|----
class asyncio.Lock(*, loop=None)|プリミティブなロックオブジェクトです。
locked()|ロック状態のとき True を返します。
coroutine acquire()|ロックを獲得します。
release()|ロックを解放します。

### [18.5.7.1.2. Event](https://docs.python.jp/3/library/asyncio-sync.html#event)

属性|概要
----|----
class asyncio.Event(*, loop=None)|threading.Event と等価で非同期な Event 実装です。
clear()|内部フラグを偽にリセットします。その後 wait() を呼んでいるコルーチンは set() が呼び出されて内部フラグが真に設定されるまでブロックします。
is_set()|内部フラグが真のとき True を返します。
set()|内部フラグを真に設定します。それを待っていたすべてのコルーチンが再開します。wait() を呼び出していたコルーチンへのブロックが解除されます。
coroutine wait()|内部フラグが真になるまでブロックします。

### [18.5.7.1.3. Condition](https://docs.python.jp/3/library/asyncio-sync.html#condition)

属性|概要
----|----
class asyncio.Condition(lock=None, *, loop=None)|threading.Condition と等価で非同期な Condition 実装です。
    coroutine acquire()|下層でのロックを獲得します。
    notify(n=1)|デフォルトでは、この条件を待機しているコルーチンがあればそれが再開されます。呼び出したコルーチンがこのロックを獲得していない状態でこのメソッドが呼び出されると RuntimeError が送出されます。
    locked()|下層のロックを獲得していれば True を返します。
    notify_all()|この条件を待機しているすべてのコルーチンを再開します。このメソッドは notify() のように振る舞いますが、1 個ではなくすべてのコルーチンが再開されます。呼び出したコルーチンがロックを獲得していない状態でこのメソッドが呼び出されると RuntimeError が送出されます。
    release()|下層のロックを解除します。
    coroutine wait()|通知を受けるまで待機します。
    coroutine wait_for(predicate)|predicate が真になるまで待機します。

## [18.5.7.2. セマフォ](https://docs.python.jp/3/library/asyncio-sync.html#semaphores)

### [18.5.7.2.1. Semaphore](https://docs.python.jp/3/library/asyncio-sync.html#semaphore)

属性|概要
----|----
class asyncio.Semaphore(value=1, *, loop=None)|Semaphore 実装です。
coroutine acquire()|セマフォを獲得します。
locked()|セマフォを直ちに獲得できる場合 True を返します。
release()|セマフォを解放し、内部カウンターを 1 加算します。カウンター値がゼロで他のコルーチンが待機状態にあった場合、加算後そのコルーチンが再開されます。

### [18.5.7.2.2. BoundedSemaphore](https://docs.python.jp/3/library/asyncio-sync.html#boundedsemaphore)

属性|概要
----|----
class asyncio.BoundedSemaphore(value=1, *, loop=None)|Semaphore を継承した有限セマフォの実装です。

