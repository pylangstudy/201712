# [17.4. concurrent.futures – 並列タスク実行](https://docs.python.jp/3/library/concurrent.futures.html)

< [17. 並行実行](https://docs.python.jp/3/library/concurrency.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

* [17_3.md](https://github.com/pylangstudy/201712/tree/master/08/00/17_3.md)

> バージョン 3.2 で追加.

> ソースコード: [Lib/concurrent/futures/thread.py](https://github.com/python/cpython/tree/3.6/Lib/concurrent/futures/thread.py) および [Lib/concurrent/futures/process.py](https://github.com/python/cpython/tree/3.6/Lib/concurrent/futures/process.py)

> concurrent.futures モジュールは、非同期に実行できる呼び出し可能オブジェクトの高水準のインタフェースを提供します。

> 非同期実行は ThreadPoolExecutor を用いてスレッドで実行することも、 ProcessPoolExecutor を用いて別々のプロセスで実行することもできます. どちらも Executor 抽象クラスで定義された同じインターフェースを実装します。

## [17.4.1. Executor オブジェクト](https://docs.python.jp/3/library/concurrent.futures.html#executor-objects)

属性|説明
----|----
class concurrent.futures.Executor|非同期呼び出しを実行するためのメソッドを提供する抽象クラスです。このクラスを直接使ってはならず、具象サブクラスを介して使います。
submit(fn, *args, **kwargs)|呼び出し可能オブジェクト fn を、 fn(*args **kwargs) として実行するようにスケジュールし、呼び出し可能オブジェクトの実行を表現する Future オブジェクトを返します。
map(func, *iterables, timeout=None, chunksize=1)|func が非同期で実行され、複数の func が同時に呼び出されうることを除き、 map(func, *iterables) と同等です。__next__() が呼ばれその結果が Executor.map() の元々の呼び出しから timeout 秒経った後も利用できない場合、返されるイタレータは concurrent.futures.TimeoutError を送出します。timeout は整数または浮動小数点数です。timeout が指定されないか None の場合、待ち時間に制限はありません。もし呼び出しが例外を送出した場合、その例外はイタレータから値を受け取る時に送出されます。ProcessPoolExecutor の使用中にこのメソッドを使用すると、 iterables をいくつかのチャンクに分割し、それぞれのチャンクを別々のタスクとしてプールに送信します。これらのチャンクの (大まかな) サイズは、 chunksize を正の整数値に設定することで指定できます。 iterable が非常に長い場合、chunksize*に大きな値を設定すると、デフォルトサイズの 1 を使用する場合に比べて性能が大幅に向上します。 :class:`ThreadPoolExecutor` に対しては *chunksize を指定しても意味がありません。
shutdown(wait=True)|executor に対して、現在保留中のフューチャーが実行された後で、使用中のすべての資源を解放するように伝えます。シャットダウンにより後に Executor.submit() と Executor.map() を呼び出すと RuntimeError が送出されます。

## [17.4.2. ThreadPoolExecutor](https://docs.python.jp/3/library/concurrent.futures.html#threadpoolexecutor)

> ThreadPoolExecutor はスレッドのプールを使用して非同期に呼び出しを行う、 Executor のサブクラスです。

> Future に関連づけられた呼び出し可能オブジェクトが、別の Future の結果を待つ時にデッドロックすることがあります。例:

```python
import time
def wait_on_b():
    time.sleep(5)
    print(b.result())  # b will never complete because it is waiting on a.
    return 5

def wait_on_a():
    time.sleep(5)
    print(a.result())  # a will never complete because it is waiting on b.
    return 6


executor = ThreadPoolExecutor(max_workers=2)
a = executor.submit(wait_on_b)
b = executor.submit(wait_on_a)
```

以下でも同様です:

```python
def wait_on_future():
    f = executor.submit(pow, 5, 2)
    # This will never complete because there is only one worker thread and
    # it is executing this function.
    print(f.result())

executor = ThreadPoolExecutor(max_workers=1)
executor.submit(wait_on_future)
```

属性|説明
----|----
class concurrent.futures.ThreadPoolExecutor(max_workers=None, thread_name_prefix='')|最大で max_workers 個のスレッドを非同期実行に使う Executor のサブクラスです。

### [17.4.2.1. ThreadPoolExecutor の例](https://docs.python.jp/3/library/concurrent.futures.html#threadpoolexecutor-example)

```python
import concurrent.futures
import urllib.request

URLS = ['http://www.foxnews.com/',
        'http://www.cnn.com/',
        'http://europe.wsj.com/',
        'http://www.bbc.co.uk/',
        'http://some-made-up-domain.com/']

# Retrieve a single page and report the URL and contents
def load_url(url, timeout):
    with urllib.request.urlopen(url, timeout=timeout) as conn:
        return conn.read()

# We can use a with statement to ensure threads are cleaned up promptly
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    # Start the load operations and mark each future with its URL
    future_to_url = {executor.submit(load_url, url, 60): url for url in URLS}
    for future in concurrent.futures.as_completed(future_to_url):
        url = future_to_url[future]
        try:
            data = future.result()
        except Exception as exc:
            print('%r generated an exception: %s' % (url, exc))
        else:
            print('%r page is %d bytes' % (url, len(data)))
```

## [17.4.3. ProcessPoolExecutor](https://docs.python.jp/3/library/concurrent.futures.html#processpoolexecutor)

> ProcessPoolExecutor はプロセスプールを使って非同期呼び出しを実施する Executor のサブクラスです。ProcessPoolExecutor は multiprocessing モジュールを利用します。このため Global Interpreter Lock を回避することができますが、pickle 化できるオブジェクトしか実行したり返したりすることができません。

> __main__ モジュールはワーカサブプロセスでインポート可能でなければなりません。 すなわち、 ProcessPoolExecutor は対話的インタープリタでは動きません。

> ProcessPoolExecutor に渡された呼び出し可能オブジェクトから Executor や Future メソッドを呼ぶとデッドロックに陥ります。

属性|説明
----|----
class concurrent.futures.ProcessPoolExecutor(max_workers=None)|Executor のサブクラスで、最大 max_workers のプールを使用して非同期な呼び出しを行います。 max_workers が None や与えられなかった場合、デフォルトでマシンのプロセッサの数になります。 max_workers が 0 以下の場合 ValueError が送出されます。

### [17.4.3.1. ProcessPoolExecutor の例](https://docs.python.jp/3/library/concurrent.futures.html#processpoolexecutor-example)

```python
import concurrent.futures
import math

PRIMES = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419]

def is_prime(n):
    if n % 2 == 0:
        return False

    sqrt_n = int(math.floor(math.sqrt(n)))
    for i in range(3, sqrt_n + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number, prime in zip(PRIMES, executor.map(is_prime, PRIMES)):
            print('%d is prime: %s' % (number, prime))

if __name__ == '__main__':
    main()
```

## [17.4.4. Future オブジェクト](https://docs.python.jp/3/library/concurrent.futures.html#future-objects)

> Future クラスは呼び出し可能オブジェクトの非同期実行をカプセル化します。 Future のインスタンスは Executor.submit() によって生成されます。

属性|説明
----|----
class concurrent.futures.Future|呼び出し可能オブジェクトの非同期実行をカプセル化します。 Future インスタンスは Executor.submit() で生成され、テストを除いて直接生成すべきではありません。
cancel()|呼び出しのキャンセルを試みます。もし呼び出しが現在実行中でキャンセルすることができない場合、メソッドは False を返します。そうでない場合呼び出しはキャンセルされ、True を返します。
cancelled()|呼び出しが正常にキャンセルされた場合 True を返します。
running()|現在呼び出しが実行中でキャンセルできない場合 True を返します。
done()|呼び出しが正常にキャンセルされたか終了した場合 True を返します。
result(timeout=None)|呼び出しによって返された値を返します。呼び出しがまだ完了していない場合、このメソッドは timeout 秒の間待機します。呼び出しが timeout 秒間の間に完了しない場合、 concurrent.futures.TimeoutError が送出されます。 timeout にはintかfloatを指定できます。timeout が指定されていないか、 None である場合、待機時間に制限はありません。
exception(timeout=None)|呼び出しによって送出された例外を返します。呼び出しがまだ完了していない場合、このメソッドは timeout 秒だけ待機します。呼び出しが timeout 秒の間に完了しない場合、 concurrent.futures.TimeoutError が送出されます。 timeout にはintかfloatを指定できます。 timeout が指定されていないか、 None である場合、待機時間に制限はありません。
add_done_callback(fn)|呼び出し可能な fn オブジェクトを future にアタッチします。futureがキャンセルされたか、実行を終了した際に、future をそのただ一つの引数として fn が呼び出されます。
set_running_or_notify_cancel()|このメソッドは、Future に関連付けられたワークやユニットテストによるワークの実行前に、 Executor の実装によってのみ呼び出してください。
set_result(result)|Future に関連付けられたワークの結果を result に設定します。
set_exception(exception)|Future に関連付けられたワークの結果を Exception exception に設定します。

## [17.4.5. モジュール関数](https://docs.python.jp/3/library/concurrent.futures.html#module-functions)

属性|説明
----|----
concurrent.futures.wait(fs, timeout=None, return_when=ALL_COMPLETED)|fs によって与えられた (別の Executor インスタンスによって作成された可能性のある) 複数の Future インスタンスの完了を待機します。集合型を 2 要素含む名前付きのタプルを返します。1 つめの集合 done には、待機の完了前に完了したフューチャ (完了またはキャンセル済み) が含まれます。2 つめの集合 not_done には、未完了のフューチャが含まれます。
concurrent.futures.as_completed(fs, timeout=None)|フューチャの完了時 (完了またはキャンセル) に yield する fs によって与えられた (別の Executor インスタンスによって作成された可能性のある) 複数の Future インスタンスのイテレータを返します。 as_completed() が呼び出される前に完了したすべてのフューチャは最初に yield されます。__next__() が呼び出され、その結果が as_completed() の元々の呼び出しから timeout 秒経った後も利用できない場合、返されるイタレータは concurrent.futures.TimeoutError を送出します。timeout は整数または浮動小数点数です。timeout が指定されないか None である場合、待ち時間に制限はありません。

### concurrent.futures.wait

> timeout で結果を返すまで待機する最大秒数を指定できます。timeout は整数か浮動小数点数をとります。timeout が指定されないか None の場合、無期限に待機します。

> return_when でこの関数がいつ結果を返すか指定します。指定できる値は以下の 定数のどれか一つです:

定数|説明
----|----
FIRST_COMPLETED|いずれかのフューチャが終了したかキャンセルされたときに返します。
FIRST_EXCEPTION|いずれかのフューチャが例外の送出で終了した場合に返します。例外を送出したフューチャがない場合は、ALL_COMPLETED と等価になります。
ALL_COMPLETED|すべてのフューチャが終了したかキャンセルされたときに返します。

### 参考

URL|説明
---|----
[PEP 3148](https://www.python.org/dev/peps/pep-3148) – futures - execute computations asynchronously|この機能を Python 標準ライブラリに含めることを述べた提案です。

## [17.4.6. 例外クラス](https://docs.python.jp/3/library/concurrent.futures.html#exception-classes)

属性|説明
----|----
exception concurrent.futures.CancelledError|future がキャンセルされたときに送出されます。
exception concurrent.futures.TimeoutError|future の操作が与えられたタイムアウトを超過したときに送出されます。
exception concurrent.futures.process.BrokenProcessPool|RuntimeError から派生しています。 この例外クラスは ProcessPoolExecutor のワーカの1つが正常に終了されなかったとき (例えば外部から kill されたとき) に送出されます。

