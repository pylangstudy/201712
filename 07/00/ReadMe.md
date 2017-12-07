# [17.2.3. プログラミングガイドライン](https://docs.python.jp/3/library/multiprocessing.html#programming-guidelines)

< [17. 並行実行](https://docs.python.jp/3/library/concurrency.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

ソースコード: [Lib/multiprocessing/](https://github.com/python/cpython/tree/3.6/Lib/multiprocessing/)

[multiprocessing](https://docs.python.jp/3/library/multiprocessing.html#module-multiprocessing) を使用するときに守るべき一定のガイドラインとイディオムを挙げます。

## [17.2.3.1. すべての開始方式について](https://docs.python.jp/3/library/multiprocessing.html#all-start-methods)

> 以下はすべての開始方式に当てはまります。

### 共有状態を避ける

> できるだけプロセス間で巨大なデータを移動することは避けるようにすべきです。

> プロセス間の通信には、threading モジュールの低レベルな同期プリミティブを使うのではなく、キューやパイプを使うのが良いでしょう。

### pickle 化の可能性

> プロキシのメソッドへの引数は、 pickle 化できるものにしてください。

### プロキシのスレッドセーフ性

> 1 つのプロキシオブジェクトは、ロックで保護しないかぎり、2 つ以上のスレッドから使用してはいけません。

> (異なるプロセスで 同じ プロキシを使用することは問題ではありません。)

### ゾンビプロセスを join する

> Unix 上ではプロセスが終了したときに join しないと、そのプロセスはゾンビになります。新たなプロセスが開始する (または active_children() が呼ばれる) ときに、join されていないすべての完了プロセスが join されるので、あまり多くにはならないでしょう。また、終了したプロセスの Process.is_alive はそのプロセスを join します。そうは言っても、自分で開始したすべてのプロセスを明示的に join することはおそらく良いプラクティスです。

### pickle/unpickle より継承する方が良い

> 開始方式に spawn あるいは forkserver を使用している場合、multiprocessing から多くの型を pickle 化する必要があるため子プロセスはそれらを使うことができます。しかし、一般にパイプやキューを使用して共有オブジェクトを他のプロセスに送信することは避けるべきです。代わりに、共有リソースにアクセスする必要のあるプロセスは上位プロセスからそれらを継承するようにすべきです。

### プロセスの強制終了を避ける

> あるプロセスを停止するために Process.terminate メソッドを使用すると、そのプロセスが現在使用されている (ロック、セマフォ、パイプやキューのような) 共有リソースを破壊したり他のプロセスから利用できない状態を引き起こし易いです。

> そのため、共有リソースを使用しないプロセスでのみ Process.terminate を使用することを考慮することがおそらく最善の方法です。

### キューを使用するプロセスを join する

> キューに要素を追加するプロセスは、すべてのバッファーされた要素が "feeder" スレッドによって下位層のパイプに対してフィードされるまで終了を待つということを覚えておいてください。 (子プロセスはこの動作を避けるためにキューの Queue.cancel_join_thread メソッドを呼ぶことができます。)

> これはキューを使用するときに、キューに追加されたすべての要素が最終的にそのプロセスが join される前に削除されていることを確認する必要があることを意味します。そうしないと、そのキューに要素が追加したプロセスの終了を保証できません。デーモンではないプロセスは自動的に join されることも覚えておいてください。

> 次の例はデッドロックを引き起こします:

```python
from multiprocessing import Process, Queue

def f(q):
    q.put('X' * 1000000)

if __name__ == '__main__':
    queue = Queue()
    p = Process(target=f, args=(queue,))
    p.start()
    p.join()                    # this deadlocks
    obj = queue.get()
```

> 修正するには最後の2行を入れ替えます(または単純に p.join() の行を削除します)。

### 明示的に子プロセスへリソースを渡す

> Unix で開始方式に fork を使用している場合、子プロセスはグローバルリソースを使用した親プロセス内で作成された共有リソースを使用できます。しかし、オブジェクトを子プロセスのコンストラクターに引数として渡すべきです。

> Windows や他の開始方式と (将来的にでも) 互換性のあるコードを書く場合は別として、これは子プロセスが実行中である限りは親プロセス内でオブジェクトがガベージコレクトされないことも保証します。これは親プロセス内でオブジェクトがガベージコレクトされたときに一部のリソースが開放されてしまう場合に重要かもしれません。

> そのため、例えば

```python
from multiprocessing import Process, Lock

def f():
    ... do something using "lock" ...

if __name__ == '__main__':
    lock = Lock()
    for i in range(10):
        Process(target=f).start()
```

> は、次のように書き直すべきです

```python
from multiprocessing import Process, Lock

def f(l):
    ... do something using "l" ...

if __name__ == '__main__':
    lock = Lock()
    for i in range(10):
        Process(target=f, args=(lock,)).start()
```

> sys.stdin を file-like オブジェクトに置き換えることに注意する

> multiprocessing は元々無条件に:

```python
os.close(sys.stdin.fileno())
```

> を multiprocessing.Process._bootstrap() メソッドの中で呼び出していました — これはプロセス内プロセス (processes-in-processes) で問題が起こしてしまいます。そこで、これは以下のように変更されました:

```python
sys.stdin.close()
sys.stdin = open(os.open(os.devnull, os.O_RDONLY), closefd=False)
```

> これによってプロセス同士が衝突して bad file descripter エラーを起こすという根本的な問題は解決しましたが、アプリケーションの出力バッファーを sys.stdin() から "file-like オブジェクト" に置き換えるという潜在的危険を持ち込んでしまいました。危険というのは、複数のプロセスが file-like オブジェクトの close() を呼び出すと、オブジェクトに同じデータが何度もフラッシュされ、破損してしまう可能性がある、というものです。

> もし file-like オブジェクトを書いて独自のキャッシュを実装するなら、キャッシュするときに常に pid を記録しておき、pid が変わったらキュッシュを捨てることで、フォークセーフにできます。例:

```python
@property
def cache(self):
    pid = os.getpid()
    if pid != self._pid:
        self._pid = pid
        self._cache = []
    return self._cache
```

> より詳しい情報は bpo-5155 、 bpo-5313 、 bpo-5331 を見てください

## [17.2.3.2. 開始方式が spawn および forkserver の場合](https://docs.python.jp/3/library/multiprocessing.html#the-spawn-and-forkserver-start-methods)

> 開始方式に fork を適用しない場合にいくつかの追加の制限事項があります。

### さらなる pickle 化の可能性

> Process.__init__() へのすべての引数は pickle 化できることを確認してください。また Process をサブクラス化する場合、そのインスタンスが Process.start メソッドが呼ばれたときに pickle 化できるようにしてください。

### グローバル変数

> 子プロセスで実行されるコードがグローバル変数にアクセスしようとする場合、子プロセスが見るその値は Process.start が呼ばれたときの親プロセスの値と同じではない可能性があります。

> しかし、単にモジュールレベルの定数であるグローバル変数なら問題にはなりません。

### メインモジュールの安全なインポート

> 新たな Python インタプリタによるメインモジュールのインポートが、意図しない副作用 (新たなプロセスを開始する等) を起こさずできるようにしてください。

> 例えば、開始方式に spawn あるいは forkserver を使用した場合に以下のモジュールを実行すると RuntimeError で失敗します:

```python
from multiprocessing import Process

def foo():
    print('hello')

p = Process(target=foo)
p.start()
```

> 代わりに、次のように if __name__ == '__main__': を使用してプログラムの "エントリポイント" を保護すべきです:

```python
from multiprocessing import Process, freeze_support, set_start_method

def foo():
    print('hello')

if __name__ == '__main__':
    freeze_support()
    set_start_method('spawn')
    p = Process(target=foo)
    p.start()
```

> (プログラムをフリーズせずに通常通り実行するなら freeze_support() 行は取り除けます。)

> これは新たに生成された Python インタープリターがそのモジュールを安全にインポートして、モジュールの foo() 関数を実行します。

> プールまたはマネージャーがメインモジュールで作成される場合に似たような制限が適用されます。

## [17.2.4. 使用例](https://docs.python.jp/3/library/multiprocessing.html#examples)

> カスタマイズされたマネージャーやプロキシの作成方法と使用方法を紹介します:

```python
from multiprocessing import freeze_support
from multiprocessing.managers import BaseManager, BaseProxy
import operator
class Foo:
    def f(self):
        print('you called Foo.f()')
    def g(self):
        print('you called Foo.g()')
    def _h(self):
        print('you called Foo._h()')

# A simple generator function
def baz():
    for i in range(10):
        yield i*i

# Proxy type for generator objects
class GeneratorProxy(BaseProxy):
    _exposed_ = ['__next__']
    def __iter__(self):
        return self
    def __next__(self):
        return self._callmethod('__next__')

# Function to return the operator module
def get_operator_module():
    return operator

##

class MyManager(BaseManager):
    pass

# register the Foo class; make `f()` and `g()` accessible via proxy
MyManager.register('Foo1', Foo)

# register the Foo class; make `g()` and `_h()` accessible via proxy
MyManager.register('Foo2', Foo, exposed=('g', '_h'))

# register the generator function baz; use `GeneratorProxy` to make proxies
MyManager.register('baz', baz, proxytype=GeneratorProxy)

# register get_operator_module(); make public functions accessible via proxy
MyManager.register('operator', get_operator_module)

##

def test():
    manager = MyManager()
    manager.start()

    print('-' * 20)

    f1 = manager.Foo1()
    f1.f()
    f1.g()
    assert not hasattr(f1, '_h')
    assert sorted(f1._exposed_) == sorted(['f', 'g'])

    print('-' * 20)

    f2 = manager.Foo2()
    f2.g()
    f2._h()
    assert not hasattr(f2, 'f')
    assert sorted(f2._exposed_) == sorted(['g', '_h'])

    print('-' * 20)

    it = manager.baz()
    for i in it:
        print('<%d>' % i, end=' ')
    print()

    print('-' * 20)

    op = manager.operator()
    print('op.add(23, 45) =', op.add(23, 45))
    print('op.pow(2, 94) =', op.pow(2, 94))
    print('op._exposed_ =', op._exposed_)

##

if __name__ == '__main__':
    freeze_support()
    test()
```

> Pool を使用する例です:

```python
import multiprocessing
import time
import random
import sys

#
# Functions used by test code
#

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % (
        multiprocessing.current_process().name,
        func.__name__, args, result
        )

def calculatestar(args):
    return calculate(*args)

def mul(a, b):
    time.sleep(0.5 * random.random())
    return a * b

def plus(a, b):
    time.sleep(0.5 * random.random())
    return a + b

def f(x):
    return 1.0 / (x - 5.0)

def pow3(x):
    return x ** 3

def noop(x):
    pass

#
# Test code
#

def test():
    PROCESSES = 4
    print('Creating pool with %d processes\n' % PROCESSES)

    with multiprocessing.Pool(PROCESSES) as pool:
        #
        # Tests
        #

        TASKS = [(mul, (i, 7)) for i in range(10)] + \
                [(plus, (i, 8)) for i in range(10)]

        results = [pool.apply_async(calculate, t) for t in TASKS]
        imap_it = pool.imap(calculatestar, TASKS)
        imap_unordered_it = pool.imap_unordered(calculatestar, TASKS)

        print('Ordered results using pool.apply_async():')
        for r in results:
            print('\t', r.get())
        print()

        print('Ordered results using pool.imap():')
        for x in imap_it:
            print('\t', x)
        print()

        print('Unordered results using pool.imap_unordered():')
        for x in imap_unordered_it:
            print('\t', x)
        print()

        print('Ordered results using pool.map() --- will block till complete:')
        for x in pool.map(calculatestar, TASKS):
            print('\t', x)
        print()

        #
        # Test error handling
        #

        print('Testing error handling:')

        try:
            print(pool.apply(f, (5,)))
        except ZeroDivisionError:
            print('\tGot ZeroDivisionError as expected from pool.apply()')
        else:
            raise AssertionError('expected ZeroDivisionError')

        try:
            print(pool.map(f, list(range(10))))
        except ZeroDivisionError:
            print('\tGot ZeroDivisionError as expected from pool.map()')
        else:
            raise AssertionError('expected ZeroDivisionError')

        try:
            print(list(pool.imap(f, list(range(10)))))
        except ZeroDivisionError:
            print('\tGot ZeroDivisionError as expected from list(pool.imap())')
        else:
            raise AssertionError('expected ZeroDivisionError')

        it = pool.imap(f, list(range(10)))
        for i in range(10):
            try:
                x = next(it)
            except ZeroDivisionError:
                if i == 5:
                    pass
            except StopIteration:
                break
            else:
                if i == 5:
                    raise AssertionError('expected ZeroDivisionError')

        assert i == 9
        print('\tGot ZeroDivisionError as expected from IMapIterator.next()')
        print()

        #
        # Testing timeouts
        #

        print('Testing ApplyResult.get() with timeout:', end=' ')
        res = pool.apply_async(calculate, TASKS[0])
        while 1:
            sys.stdout.flush()
            try:
                sys.stdout.write('\n\t%s' % res.get(0.02))
                break
            except multiprocessing.TimeoutError:
                sys.stdout.write('.')
        print()
        print()

        print('Testing IMapIterator.next() with timeout:', end=' ')
        it = pool.imap(calculatestar, TASKS)
        while 1:
            sys.stdout.flush()
            try:
                sys.stdout.write('\n\t%s' % it.next(0.02))
            except StopIteration:
                break
            except multiprocessing.TimeoutError:
                sys.stdout.write('.')
        print()
        print()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    test()
```

> ワーカープロセスのコレクションに対してタスクをフィードしてその結果をまとめるキューの使い方の例を紹介します:

```python
import time
import random

from multiprocessing import Process, Queue, current_process, freeze_support

#
# Function run by worker processes
#

def worker(input, output):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        output.put(result)

#
# Function used to calculate result
#

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % \
        (current_process().name, func.__name__, args, result)

#
# Functions referenced by tasks
#

def mul(a, b):
    time.sleep(0.5*random.random())
    return a * b

def plus(a, b):
    time.sleep(0.5*random.random())
    return a + b

#
#
#

def test():
    NUMBER_OF_PROCESSES = 4
    TASKS1 = [(mul, (i, 7)) for i in range(20)]
    TASKS2 = [(plus, (i, 8)) for i in range(10)]

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for task in TASKS1:
        task_queue.put(task)

    # Start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue)).start()

    # Get and print results
    print('Unordered results:')
    for i in range(len(TASKS1)):
        print('\t', done_queue.get())

    # Add more tasks using `put()`
    for task in TASKS2:
        task_queue.put(task)

    # Get and print some more results
    for i in range(len(TASKS2)):
        print('\t', done_queue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')


if __name__ == '__main__':
    freeze_support()
    test()
```

