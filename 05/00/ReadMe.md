# [17.2. multiprocessing — プロセスベースの並列処理](https://docs.python.jp/3/library/threading.html)

< [17. 並行実行](https://docs.python.jp/3/library/concurrency.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)


ソースコード: [Lib/multiprocessing/](https://github.com/python/cpython/tree/3.6/Lib/multiprocessing/)

## [17.2.1. はじめに](https://docs.python.jp/3/library/multiprocessing.html#introduction)

> multiprocessing は、 threading と似た API で複数のプロセスの生成をサポートするパッケージです。 multiprocessing パッケージは、ローカルとリモート両方の並行処理を提供します。また、このパッケージはスレッドの代わりにサブプロセスを使用することにより、グローバルインタープリタロック の問題を避ける工夫が行われています。このような特徴があるため multiprocessing モジュールを使うことで、マルチプロセッサーマシンの性能を最大限に活用することができるでしょう。なお、このモジュールは Unix と Windows の両方で動作します。

> multiprocessing モジュールでは、threading モジュールには似たものが存在しない API も導入されています。その最たるものが Pool オブジェクトです。これは複数の入力データに対して、サブプロセス群に入力データを分配 (データ並列) して関数を並列実行するのに便利な手段を提供します。以下の例では、モジュール内で関数を定義して、子プロセスがそのモジュールを正常にインポートできるようにする一般的な方法を示します。 Pool を用いたデータ並列の基礎的な例は次の通りです:

```python
from multiprocessing import Pool

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        print(p.map(f, [1, 2, 3]))
```

標準出力に以下が出力されます:

```python
[1, 4, 9]
```

### [17.2.1.1. Process クラス](https://docs.python.jp/3/library/multiprocessing.html#the-process-class)

> multiprocessing モジュールでは、プロセスは以下の手順によって生成されます。はじめに Process のオブジェクトを作成し、続いて start() メソッドを呼び出します。この Process クラスは threading.Thread クラスと同様の API を持っています。まずは、簡単な例をもとにマルチプロセスを使用したプログラムについてみていきましょう

```python
from multiprocessing import Process

def f(name):
    print('hello', name)

if __name__ == '__main__':
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
```

> 実行された個々のプロセス ID を表示するために拡張したサンプルコードを以下に示します:

```python
from multiprocessing import Process
import os

def info(title):
    print(title)
    print('module name:', __name__)
    print('parent process:', os.getppid())
    print('process id:', os.getpid())

def f(name):
    info('function f')
    print('hello', name)

if __name__ == '__main__':
    info('main line')
    p = Process(target=f, args=('bob',))
    p.start()
    p.join()
```

> なぜ if __name__ == '__main__' という記述が必要かは プログラミングガイドライン を参照してください。

### [17.2.1.2. コンテキストと開始方式](https://docs.python.jp/3/library/multiprocessing.html#contexts-and-start-methods)

> プラットフォームにもよりますが、multiprocessing はプロセスを開始するために 3 つの方法をサポートしています。それら 開始方式 は以下のとおりです

方法|説明
----|----
spawn|親プロセスは新たに python インタープリタープロセスを開始します。子プロセスはプロセスオブジェクトの run() メソッドの実行に必要なリソースのみ継承します。特に、親プロセスからの不要なファイル記述子とハンドルは継承されません。この方式を使用したプロセスの開始は fork や forkserver に比べ遅くなります。 Unix と Windows で利用可能。Windows でのデフォルト。
fork|親プロセスは os.fork() を使用して Python インタープリターをフォークします。子プロセスはそれが開始されるとき、事実上親プロセスと同一になります。親プロセスのリソースはすべて子プロセスに継承されます。マルチスレッドプロセスのフォークは安全性に問題があることに注意してください。 Unix でのみ利用可能。Unix でのデフォルト。
forkserver|プログラムを開始するとき forkserver 方式を選択した場合、サーバープロセスが開始されます。それ以降、新しいプロセスが必要になったときはいつでも、親プロセスはサーバーに接続し、新しいプロセスのフォークを要求します。フォークサーバープロセスはシングルスレッドなので os.fork() の使用に関しても安全です。不要なリソースは継承されません。 Unix パイプを経由したファイル記述子の受け渡しをサポートする Unix で利用可能。

> バージョン 3.4 で変更: すべての Unix プラットフォームで spawn が、一部のプラットフォームで forkserver が追加されました。Windows では親プロセスの継承可能な全ハンドルが子プロセスに継承されることがなくなりました。

> Unix で開始方式に spawn あるいは forkserver を使用した場合は、プログラムのプロセスによって作成されたリンクされていない名前付きセマフォを追跡する セマフォトラッカー プロセスも開始されます。全プロセスが終了したときにセマフォトラッカーは残っているあらゆるセマフォのリンクを解除します。通常そういったことはないのですが、プロセスがシグナルによって kill されたときに "漏れた" セマフォが発生する場合があります。(名前付きセマフォのリンク解除は、システムが個数の上限のみ許可している場合に深刻な問題になるため、それらは再起動されるまで自動的にリンク解除されることはありません。)

> 開始方式はメインモジュールの if __name__ == '__main__' 節内で、関数 set_start_method() によって指定します。以下に例を示します:

```python
import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    p = mp.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()
```

> 関数 set_start_method() はプログラム内で複数回使用してはいけません。

> もうひとつの方法として、get_context() を使用してコンテキストオブジェクトを取得することができます。コンテキストオブジェクトは multiprocessing モジュールと同じ API を持ち、同じプログラム内で複数の開始方式を使用できます。

```python
import multiprocessing as mp

def foo(q):
    q.put('hello')

if __name__ == '__main__':
    ctx = mp.get_context('spawn')
    q = ctx.Queue()
    p = ctx.Process(target=foo, args=(q,))
    p.start()
    print(q.get())
    p.join()
```

> あるコンテキストに関連したオブジェクトは異なるコンテキストのプロセスとは互換性がない場合があることに注意してください。特に、fork コンテキストを使用して作成されたロックは、spawn あるいは forkserver を使用して開始されたプロセスに渡すことはできません。

> 特定の開始方式の使用を要求するライブラリは get_context() を使用してライブラリ利用者の選択を阻害しないようにするべきです。

## [17.2.1.3. プロセス間でのオブジェクト交換](https://docs.python.jp/3/library/multiprocessing.html#exchanging-objects-between-processes)

> multiprocessing モジュールでは、プロセス間通信の手段が2つ用意されています。それぞれ以下に詳細を示します:

### キュー (Queue)

> Queue クラスは queue.Queue クラスとほとんど同じように使うことができます。以下に例を示します:

```python
from multiprocessing import Process, Queue

def f(q):
    q.put([42, None, 'hello'])

if __name__ == '__main__':
    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    print(q.get())    # prints "[42, None, 'hello']"
    p.join()
```

> キューはスレッドセーフであり、プロセスセーフです。

### パイプ (Pipe)

> Pipe() 関数はパイプで繋がれたコネクションオブジェクトのペアを返します。デフォルトでは双方向性パイプを返します。以下に例を示します:

```python
from multiprocessing import Process, Pipe

def f(conn):
    conn.send([42, None, 'hello'])
    conn.close()

if __name__ == '__main__':
    parent_conn, child_conn = Pipe()
    p = Process(target=f, args=(child_conn,))
    p.start()
    print(parent_conn.recv())   # prints "[42, None, 'hello']"
    p.join()
```

> パイプのそれぞれの端を表す2つのコネクションオブジェクトが Pipe() 関数から返されます。各コネクションオブジェクトには、 send()、 recv()、その他のメソッドがあります。2つのプロセス (またはスレッド) がパイプの 同じ 端で同時に読み込みや書き込みを行うと、パイプ内のデータが破損してしまうかもしれないことに注意してください。もちろん、各プロセスがパイプの別々の端を同時に使用するならば、データが破壊される危険性はありません。

## [17.2.1.4. プロセス間の同期](https://docs.python.jp/3/library/multiprocessing.html#synchronization-between-processes)

> multiprocessing は threading モジュールと等価な同期プリミティブを備えています。以下の例では、ロックを使用して、一度に1つのプロセスしか標準出力に書き込まないようにしています:

```python
from multiprocessing import Process, Lock

def f(l, i):
    l.acquire()
    try:
        print('hello world', i)
    finally:
        l.release()

if __name__ == '__main__':
    lock = Lock()

    for num in range(10):
        Process(target=f, args=(lock, num)).start()
```

> ロックを使用しないで標準出力に書き込んだ場合は、各プロセスからの出力がごちゃまぜになってしまいます。

## [17.2.1.5. プロセス間での状態の共有](https://docs.python.jp/3/library/multiprocessing.html#sharing-state-between-processes)

> これまでの話の流れで触れたとおり、並行プログラミングを行うときには、できるかぎり状態を共有しないのが定石です。複数のプロセスを使用するときは特にそうでしょう。

> しかし、どうしてもプロセス間のデータ共有が必要な場合のために multiprocessing モジュールには2つの方法が用意されています。

### 共有メモリ (Shared memory)

> データを共有メモリ上に保持するために Value クラス、もしくは Array クラスを使用することができます。以下のサンプルコードを使って、この機能についてみていきましょう

```python
from multiprocessing import Process, Value, Array

def f(n, a):
    n.value = 3.1415927
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d', 0.0)
    arr = Array('i', range(10))

    p = Process(target=f, args=(num, arr))
    p.start()
    p.join()

    print(num.value)
    print(arr[:])
```

> このサンプルコードを実行すると以下のように表示されます

```python
3.1415927
[0, -1, -2, -3, -4, -5, -6, -7, -8, -9]
```


> num と arr を生成するときに使用されている、引数 'd' と 'i' は array モジュールにより使用される種別の型コードです。ここで使用されている 'd' は倍精度浮動小数、 'i' は符号付整数を表します。これらの共有オブジェクトは、プロセスセーフでありスレッドセーフです。

> 共有メモリを使用して、さらに柔軟なプログラミングを行うには multiprocessing.sharedctypes モジュールを使用します。このモジュールは共有メモリから割り当てられた任意の ctypes オブジェクトの生成をサポートします。

### サーバープロセス (Server process)

> Manager() 関数により生成されたマネージャーオブジェクトはサーバープロセスを管理します。マネージャーオブジェクトは Python のオブジェクトを保持して、他のプロセスがプロキシ経由でその Python オブジェクトを操作することができます。

> Manager() 関数が返すマネージャは list, dict, Namespace, Lock, RLock, Semaphore, BoundedSemaphore, Condition, Event, Barrier, Queue, Value, Array をサポートします。 以下にサンプルコードを示します。

```python
from multiprocessing import Process, Manager

def f(d, l):
    d[1] = '1'
    d['2'] = 2
    d[0.25] = None
    l.reverse()

if __name__ == '__main__':
    with Manager() as manager:
        d = manager.dict()
        l = manager.list(range(10))

        p = Process(target=f, args=(d, l))
        p.start()
        p.join()

        print(d)
        print(l)
```

> このサンプルコードを実行すると以下のように表示されます

```python
{0.25: None, 1: '1', '2': 2}
[9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
```

> サーバープロセスのマネージャーオブジェクトは共有メモリのオブジェクトよりも柔軟であるといえます。それは、どのような型のオブジェクトでも使えるからです。また、1つのマネージャーオブジェクトはネットワーク経由で他のコンピューター上のプロセスによって共有することもできます。しかし、共有メモリより動作が遅いという欠点があります。

## [17.2.1.6. ワーカープロセスのプールを使用](https://docs.python.jp/3/library/multiprocessing.html#using-a-pool-of-workers)

> Pool クラスは、ワーカープロセスをプールする機能を備えています。このクラスには、異なる方法でワーカープロセスへタスクを割り当てるいくつかのメソッドがあります。

> 例えば:

```python
from multiprocessing import Pool, TimeoutError
import time
import os

def f(x):
    return x*x

if __name__ == '__main__':
    # start 4 worker processes
    with Pool(processes=4) as pool:

        # print "[0, 1, 4,..., 81]"
        print(pool.map(f, range(10)))

        # print same numbers in arbitrary order
        for i in pool.imap_unordered(f, range(10)):
            print(i)

        # evaluate "f(20)" asynchronously
        res = pool.apply_async(f, (20,))      # runs in *only* one process
        print(res.get(timeout=1))             # prints "400"

        # evaluate "os.getpid()" asynchronously
        res = pool.apply_async(os.getpid, ()) # runs in *only* one process
        print(res.get(timeout=1))             # prints the PID of that process

        # launching multiple evaluations asynchronously *may* use more processes
        multiple_results = [pool.apply_async(os.getpid, ()) for i in range(4)]
        print([res.get(timeout=1) for res in multiple_results])

        # make a single worker sleep for 10 secs
        res = pool.apply_async(time.sleep, (10,))
        try:
            print(res.get(timeout=1))
        except TimeoutError:
            print("We lacked patience and got a multiprocessing.TimeoutError")

        print("For the moment, the pool remains available for more work")

    # exiting the 'with'-block has stopped the pool
    print("Now the pool is closed and no longer available")
```

> プールオブジェクトのメソッドは、そのプールを作成したプロセスのみが呼び出すべきです。

> 注釈

> このパッケージに含まれる機能を使用するためには、子プロセスから __main__ モジュールをインポートできる必要があります。このことについては プログラミングガイドライン で触れていますが、ここであらためて強調しておきます。なぜかというと、いくつかのサンプルコード、例えば multiprocessing.pool.Pool のサンプルはインタラクティブシェル上では動作しないからです。以下に例を示します:

```python
>>> from multiprocessing import Pool
>>> p = Pool(5)
>>> def f(x):
...     return x*x
...
>>> p.map(f, [1,2,3])
Process PoolWorker-1:
Process PoolWorker-2:
Process PoolWorker-3:
Traceback (most recent call last):
AttributeError: 'module' object has no attribute 'f'
AttributeError: 'module' object has no attribute 'f'
AttributeError: 'module' object has no attribute 'f'
```

> (このサンプルを試すと、3つのトレースバックすべてがほぼランダムに交互に重なって表示されます。そうなったら、なんとかしてマスタープロセスを止めましょう。)

