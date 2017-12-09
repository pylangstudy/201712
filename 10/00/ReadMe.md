# [17.6. sched — イベントスケジューラ](https://docs.python.jp/3/library/sched.html)

< [17. 並行実行](https://docs.python.jp/3/library/concurrency.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

ソースコード: [Lib/sched.py](https://github.com/python/cpython/tree/3.6/Lib/sched.py)

> sched モジュールは一般的な目的のためのイベントスケジューラを実装するクラスを定義します:

属性|説明
----|----
class sched.scheduler(timefunc=time.monotonic, delayfunc=time.sleep)|scheduler クラスはイベントをスケジュールするための一般的なインタフェースを定義します。それは "外の世界" を実際に扱うための2つの関数を必要とします — timefunc は引数なしで呼ばれて 1 つの数値を返す callable オブジェクトでなければなりません (戻り値は任意の単位で「時間」を表します)。 time.monotonic が利用出来ない場合、 timefunc のデフォルトには time.time が代わりに使われます。 delayfunc は 1 つの引数を持つ callable オブジェクトでなければならず、その時間だけ遅延する必要があります (引数は timefunc の出力と互換)。 delayfunc は、各々のイベントが実行された後に引数 0 で呼ばれることがあります。これは、マルチスレッドアプリケーションの中で他のスレッドが実行する機会を与えるためです。

> 以下はプログラム例です:

```python
>>> import sched, time
>>> s = sched.scheduler(time.time, time.sleep)
>>> def print_time(a='default'):
...     print("From print_time", time.time(), a)
...
>>> def print_some_times():
...     print(time.time())
...     s.enter(10, 1, print_time)
...     s.enter(5, 2, print_time, argument=('positional',))
...     s.enter(5, 1, print_time, kwargs={'a': 'keyword'})
...     s.run()
...     print(time.time())
...
>>> print_some_times()
930343690.257
From print_time 930343695.274 positional
From print_time 930343695.275 keyword
From print_time 930343700.273 default
930343700.276
```

### [17.6.1. スケジューラオブジェクト](https://docs.python.jp/3/library/sched.html#scheduler-objects)

> scheduler インスタンスは以下のメソッドと属性を持っています:

属性|説明
----|----
scheduler.enterabs(time, priority, action, argument=(), kwargs={})|新しいイベントをスケジュールします。引数 time は、コンストラクタへ渡された timefunc の戻り値と互換な数値型でなければいけません。同じ time によってスケジュールされたイベントは、それらの priority によって実行されるでしょう。
scheduler.enter(delay, priority, action, argument=(), kwargs={})|時間単位以上の delay でイベントをスケジュールします。相対的時間以外の、引数、効果、戻り値は、 enterabs() に対するものと同じです。
scheduler.cancel(event)|キューからイベントを消去します。もし event がキューにある現在のイベントでないならば、このメソッドは ValueError を送出します。
scheduler.empty()|もしイベントキューが空ならば、Trueを返します。
scheduler.run(blocking=True)|すべてのスケジュールされたイベントを実行します。このメソッドは次のイベントを待ち、それを実行し、スケジュールされたイベントがなくなるまで同じことを繰り返します。(イベントの待機は、 コンストラクタへ渡された関数 delayfunc() を使うことで行います。)
scheduler.queue|読み出し専用の属性で、これから起こるイベントが実行される順序で格納されたリストを返します。各イベントは、次の属性 time, priority, action, argument, kwargs を持った named tuple の形式になります。

