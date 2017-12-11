# [17.7. queue — 同期キュークラス](https://docs.python.jp/3/library/queue.html)

< [17. 並行実行](https://docs.python.jp/3/library/concurrency.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

ソースコード: [Lib/queue.py](https://github.com/python/cpython/tree/3.6/Lib/queue.py)

> queue モジュールは、複数プロデューサ-複数コンシューマ(multi-producer, multi-consumer)キューを実装します。これは、複数のスレッドの間で情報を安全に交換しなければならないときのマルチスレッドプログラミングで特に有益です。このモジュールの Queue クラスは、必要なすべてのロックセマンティクスを実装しています。これはPythonのスレッドサポートの状況に依存します。 threading モジュールを参照してください。

> The module implements three types of queue, which differ only in the order in which the entries are retrieved. In a FIFO queue, the first tasks added are the first retrieved. In a LIFO queue, the most recently added entry is the first retrieved (operating like a stack). With a priority queue, the entries are kept sorted (using the heapq module) and the lowest valued entry is retrieved first.

翻訳。

> このモジュールでは、エントリが取得される順序だけが異なる3種類のキューが実装されています。 FIFOキューでは、追加される最初のタスクが最初に取得されます。 LIFOキューでは、最後に追加されたエントリが最初に取得されます（スタックのように動作します）。 優先度キューでは、エントリは（heapqモジュールを使用して）ソートされたままにされ、最も低い値のエントリが最初に取得されます。

> 内部的には、このモジュールは競争スレッドを一時的にブロックするためにロックを使っています; しかし、スレッド内での再入を扱うようには設計されていません。

> queue モジュールは以下のクラスと例外を定義します:

属性|説明
----|----
class queue.Queue(maxsize=0)|Constructor for a FIFO queue. maxsize is an integer that sets the upperbound limit on the number of items that can be placed in the queue. Insertion will block once this size has been reached, until queue items are consumed. If maxsize is less than or equal to zero, the queue size is infinite.
class queue.LifoQueue(maxsize=0)|Constructor for a LIFO queue. maxsize is an integer that sets the upperbound limit on the number of items that can be placed in the queue. Insertion will block once this size has been reached, until queue items are consumed. If maxsize is less than or equal to zero, the queue size is infinite.
class queue.PriorityQueue(maxsize=0)|優先順位付きキューのコンストラクタです。maxsize はキューに置くことのできる要素数の上限を設定する整数です。いったんこの大きさに達したら、挿入はキューの要素が消費されるまでブロックされます。もし maxsize が0以下であるならば、キューの大きさは無限です。
exception queue.Empty|空の Queue オブジェクトで、非ブロックメソッド get() (または get_nowait()) が呼ばれたとき、送出される例外です。
exception queue.Full|満杯の Queue オブジェクトで、非ブロックメソッド put() (または put_nowait()) が呼ばれたとき、送出される例外です。

## [17.7.1. キューオブジェクト]()

キューオブジェクト(Queue, LifoQueue, PriorityQueue)は、以下のpublicメソッドを提供しています。

属性|説明
----|----
Queue.qsize()|キューの近似サイズを返します。ここで、qsize() > 0 は後続の get() がブロックしないことを保証しないこと、また qsize() < maxsize が put() がブロックしないことを保証しないことに注意してください。
Queue.empty()|キューが空の場合は True を返し、そうでなければ False を返します。empty() が True を返しても、後続の put() の呼び出しがブロックしないことは保証されません。同様に、empty() が False を返しても、後続の get() の呼び出しがブロックしないことは保証されません。
Queue.full()|キューが一杯の場合は True を返し、そうでなければ False を返します。full() が True を返しても、後続の get() の呼び出しがブロックしないことは保証されません。同様に、full() が False を返しても、後続の put() の呼び出しがブロックしないことは保証されません。
Queue.put(item, block=True, timeout=None)|item をキューに入れます。 もしオプション引数 block が真で timeout が None (デフォルト) の場合は、必要であればフリースロットが利用可能になるまでブロックします。 timeout が正の数の場合は、最大で timeout 秒間ブロックし、その時間内に空きスロットが利用可能にならなければ、例外 Full を送出します。 そうでない場合 (block が偽) は、空きスロットが直ちに利用できるならば、キューにアイテムを置きます。 できないならば、例外 Full を送出します (この場合 timeout は無視されます)。
Queue.put_nowait(item)|put(item, False) と等価です。
Queue.get(block=True, timeout=None)|キューからアイテムを取り除き、それを返します。 オプション引数 block が真で timeout が None (デフォルト) の場合は、必要であればアイテムが取り出せるようになるまでブロックします。 もし timeout が正の数の場合は、最大で timeout 秒間ブロックし、その時間内でアイテムが取り出せるようにならなければ、例外 Empty を送出します。 そうでない場合 (block が偽) は、直ちにアイテムが取り出せるならば、それを返します。 できないならば、例外 Empty を送出します (この場合 timeout は無視されます)。
Queue.get_nowait()|get(False) と等価です。 キューに入れられたタスクが全てコンシューマスレッドに処理されたかどうかを追跡するために 2つのメソッドが提供されます。
Queue.task_done()|過去にキューに入れられたタスクが完了した事を示します。キューのコンシューマスレッドに利用されます。タスクの取り出しに使われた各 get() の後に task_done() を呼び出すと、取り出したタスクに対する処理が完了した事をキューに教えます。
Queue.join()|キューにあるすべてのアイテムが取り出されて処理されるまでブロックします。


> キューに入れたタスクが完了するのを待つ例:

```python
def worker():
    while True:
        item = q.get()
        if item is None:
            break
        do_work(item)
        q.task_done()

q = queue.Queue()
threads = []
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in source():
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()
```

### 参考

クラス|概要
------|----
multiprocessing.Queue|(マルチスレッドではなく) マルチプロセスの文脈で使用されるキュークラス。

> collections.deque は、ロックなしで append() や popleft() といったアトミック操作が可能なキューの実装です。

