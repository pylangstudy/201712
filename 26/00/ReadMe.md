# [18.5.8. キュー](https://docs.python.jp/3/library/asyncio-queue.html)

< [18.5. asyncio — 非同期 I/O、イベントループ、コルーチンおよびタスク](https://docs.python.jp/3/library/asyncio.html) < [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

* Source code: [Lib/asyncio/queues.py](https://github.com/python/cpython/tree/3.6/Lib/asyncio/queues.py)

> asyncio queue API は queue モジュールのクラス (Queue, PriorityQueue, LifoQueue) に近くなるよう設計されましたが、 timeout 引数はありません。 asyncio.wait_for() 関数を用いてタイムアオウト後にタスクをキャンセルすることが出来ます。

## [18.5.8.1. Queue](https://docs.python.jp/3/library/asyncio-queue.html#queue)

属性|概要
----|----
class asyncio.Queue(maxsize=0, *, loop=None)|プロデューサーおよびコンシューマーコルーチンの連係に役立つキューです。
empty()|キューが空ならば True を、そうでなければ False を返します。
full()|キューに要素が maxsize 個あれば True を返します。
coroutine get()|キューから要素を削除して返します。キューが空の場合項目が利用可能になるまで待機します。
get_nowait()|キューから要素を削除して返します。
coroutine join()|キューにあるすべてのアイテムが取り出されて処理されるまでブロックします。
coroutine put(item)|要素をキューに入れます。キューがいっぱいの場合、要素を追加する前にスロットが利用できるまで待機します。
put_nowait(item)|ブロックせずにアイテムをキューに追加します。
qsize()|キュー内のアイテム数です。
task_done()|キューに入っていたタスクが完了したことを示します。
maxsize|キューに追加できるアイテム数です。

## [18.5.8.2. PriorityQueue](https://docs.python.jp/3/library/asyncio-queue.html#priorityqueue)

属性|概要
----|----
class asyncio.PriorityQueue|Queue のサブクラスです; 優先順位に従ってエントリを回収します (最低が最初)。

## [18.5.8.3. LifoQueue](https://docs.python.jp/3/library/asyncio-queue.html#lifoqueue)

属性|概要
----|----
class asyncio.LifoQueue|Queue のサブクラスです。エントリは最後に追加されたものから回収されます。

### [18.5.8.3.1. 例外](https://docs.python.jp/3/library/asyncio-queue.html#exceptions)

属性|概要
----|----
exception asyncio.QueueEmpty|get_nowait() メソッドが空の Queue オブジェクトに対して呼ばれたときに送出されます。
exception asyncio.QueueFull|put_nowait() メソッドが full の Queue オブジェクトに対して呼ばれたときに送出されます。

