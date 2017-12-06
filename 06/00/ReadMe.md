# [17.2.2. リファレンス](https://docs.python.jp/3/library/multiprocessing.html#reference)

< [17. 並行実行](https://docs.python.jp/3/library/concurrency.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

ソースコード: [Lib/multiprocessing/](https://github.com/python/cpython/tree/3.6/Lib/multiprocessing/)

[multiprocessing](https://docs.python.jp/3/library/multiprocessing.html#module-multiprocessing) パッケージは [threading](https://docs.python.jp/3/library/threading.html#module-threading) モジュールの API とほとんど同じです。

## [17.2.2.1. Process クラスと例外](https://docs.python.jp/3/library/multiprocessing.html#process-and-exceptions)

属性|概要
----|----
class multiprocessing.Process(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)|Process オブジェクトは各プロセスの処理を表します。 Process クラスは threading.Thread クラスのすべてのメソッドと同じインタフェースを提供します。
run()|プロセスが実行する処理を表すメソッドです。
start()|プロセスの処理を開始するためのメソッドです。
join([timeout])|オプションの引数 timeout が None (デフォルト) の場合、 join() メソッドが呼ばれたプロセスは処理が終了するまでブロックします。 timeout が正の数である場合、最大 timeout 秒ブロックします。 プロセスが終了あるいはタイムアウトした場合、メソッドは None を返すことに注意してください。 プロセスの exitcode を確認し終了したかどうかを判断してください。
name|プロセスの名前。名前は識別のためだけに使用される文字列です。それ自体には特別な意味はありません。複数のプロセスに同じ名前が与えられても構いません。
is_alive()|プロセスが実行中かを判別します。
daemon|デーモンプロセスであるかのフラグであり、ブール値です。この属性は start() が呼び出される前に設定されている必要があります。
pid|プロセスIDを返します。プロセスの生成前は None が設定されています。
exitcode|子プロセスの終了コードです。子プロセスがまだ終了していない場合は None が返されます。負の値 -N は子プロセスがシグナル N で終了したことを表します。
authkey|プロセスの認証キーです (バイト文字列です)。
sentinel|プロセスが終了するときに "ready" となるシステムオブジェクトの数値ハンドル。
terminate()|プロセスを終了します。Unix 環境では SIGTERM シグナルを、 Windows 環境では TerminateProcess() を使用して終了させます。終了ハンドラーや finally 節などは、実行されないことに注意してください。
exception multiprocessing.ProcessError|すべての multiprocessing 例外の基底クラスです。
exception multiprocessing.BufferTooShort|この例外は Connection.recv_bytes_into() によって発生し、バッファーオブジェクトが小さすぎてメッセージが読み込めないことを示します。
exception multiprocessing.AuthenticationError|認証エラーがあった場合に送出されます。
exception multiprocessing.TimeoutError|タイムアウトをサポートするメソッドでタイムアウトが過ぎたときに送出されます。

## [17.2.2.2. パイプ (Pipe) とキュー (Queue)](https://docs.python.jp/3/library/multiprocessing.html#pipes-and-queues)

> 複数のプロセスを使う場合、一般的にはメッセージパッシングをプロセス間通信に使用し、ロックのような同期プリミティブを使用しないようにします。

> メッセージのやりとりのために Pipe() (2つのプロセス間の通信用)、もしくはキュー (複数のメッセージ生成プロセス (producer)、消費プロセス (consumer) の実現用) を使うことができます。

> Queue, SimpleQueue と JoinableQueue 型は複数プロセスから生成/消費を行う FIFO キューです。これらのキューは標準ライブラリの queue.Queue を模倣しています。 Queue には Python 2.5 の queue.Queue クラスで導入された task_done() と join() メソッドがないことが違う点です。

> もし JoinableQueue を使用するなら、キューから削除される各タスクのために JoinableQueue.task_done() を呼び出さなければ なりません 。さもないと、いつか完了していないタスクを数えるためのセマフォがオーバーフローし、例外を発生させるでしょう。

> 管理オブジェクトを使用することで共有キューを作成できることも覚えておいてください。詳細は マネージャー を参照してください。

### 注釈

> multiprocessing は、タイムアウトを伝えるために、通常の queue.Empty と queue.Full 例外を使用します。それらはmultiprocessing の名前空間では利用できないため、queue からインポートする必要があります。

### 注釈

> オブジェクトがキューに追加される際、そのオブジェクトは pickle 化されています。そのため、バックグラウンドのスレッドが後になって下位層のパイプに pickle 化されたデータをフラッシュすることがあります。これにより、少し驚くような結果になりますが、実際に問題になることはないはずです。これが問題になるような状況では、かわりに manager を使ってキューを作成することができるからです。

* 空のキューの中にオブジェクトを追加した後、キューの empty() メソッドが False を返すまでの間にごくわずかな遅延が起きることがあり、get_nowait() が queue.Empty を発生させることなく制御が呼び出し元に返ってしまうことがあります。
* 複数のプロセスがオブジェクトをキューに詰めている場合、キューの反対側ではオブジェクトが詰められたのとは違う順序で取得される可能性があります。ただし、同一のプロセスから詰め込まれたオブジェクトは、それらのオブジェクト間では、必ず期待どおりの順序になります。

### 警告

> Queue を利用しようとしている最中にプロセスを Process.terminate() や os.kill() で終了させる場合、キューにあるデータは破損し易くなります。終了した後で他のプロセスがキューを利用しようとすると、例外を発生させる可能性があります。

### 警告

> 上述したように、もし子プロセスがキューへ要素を追加するなら (かつ JoinableQueue.cancel_join_thread を使用しないなら) そのプロセスはバッファーされたすべての要素がパイプへフラッシュされるまで終了しません。

> これは、そのプロセスを join しようとする場合、キューに追加されたすべての要素が消費されたことが確実でないかぎり、デッドロックを発生させる可能性があることを意味します。似たような現象で、子プロセスが非デーモンプロセスの場合、親プロセスは終了時に非デーモンのすべての子プロセスを join しようとしてハングアップする可能性があります。

> マネージャーを使用して作成されたキューではこの問題はありません。詳細は プログラミングガイドライン を参照してください。

> プロセス間通信におけるキューの使用例を知りたいなら 使用例 を参照してください。

属性|概要
----|----
multiprocessing.Pipe([duplex])|パイプの両端を表す Connection オブジェクトのペア (conn1, conn2) を返します。
class multiprocessing.Queue([maxsize])|パイプや2～3個のロック/セマフォを使用して実装されたプロセス共有キューを返します。あるプロセスが最初に要素をキューへ追加するとき、バッファーからパイプの中へオブジェクトを転送する供給スレッドが開始されます。
qsize()|おおよそのキューのサイズを返します。マルチスレッディング/マルチプロセスの特性上、この数値は信用できません。
empty()|キューが空っぽなら True を、そうでなければ False を返します。マルチスレッディング/マルチプロセシングの特性上、これは信用できません。
full()|キューがいっぱいなら True を、そうでなければ False を返します。マルチスレッディング/マルチプロセシングの特性上、これは信用できません。
put(obj[, block[, timeout]])|キューの中へ obj を追加します。オプションの引数 block が True (デフォルト) 且つ timeout が None (デフォルト) なら、空きスロットが利用可能になるまで必要であればブロックします。 timeout が正の数なら、最大 timeout 秒ブロックして、その時間内に空きスロットが利用できなかったら queue.Full 例外を発生させます。それ以外 (block が False) で、空きスロットがすぐに利用可能な場合はキューに要素を追加します。そうでなければ queue.Full 例外が発生します(その場合 timeout は無視されます)。
put_nowait(obj)|put(obj, False) と等価です。
get([block[, timeout]])|キューから要素を取り出して削除します。オプションの引数 block が True (デフォルト) 且つ timeout が None (デフォルト) なら、要素が取り出せるまで必要であればブロックします。 timeout が正の数なら、最大 timeout 秒ブロックして、その時間内に要素が取り出せなかったら queue.Empty 例外を発生させます。それ以外 (block が False) で、要素がすぐに取り出せる場合は要素を返します。そうでなければ queue.Empty 例外が発生します(その場合 timeout は無視されます)。
get_nowait()|get(False) と等価です。
close()|カレントプロセスからこのキューへそれ以上データが追加されないことを表します。バックグラウンドスレッドはパイプへバッファーされたすべてのデータをフラッシュするとすぐに終了します。これはキューがガベージコレクトされるときに自動的に呼び出されます。
join_thread()|バックグラウンドスレッドを join します。このメソッドは close() が呼び出された後でのみ使用されます。バッファーされたすべてのデータがパイプへフラッシュされるのを保証するため、バックグラウンドスレッドが終了するまでブロックします。
cancel_join_thread()|join_thread() がブロッキングするのを防ぎます。特にこれはバックグラウンドスレッドがそのプロセスの終了時に自動的に join されるのを防ぎます。詳細は join_thread() を参照してください。
class multiprocessing.SimpleQueue|単純化された Queue 型です。ロックされた Pipe と非常に似ています。
empty()|キューが空ならば True を、そうでなければ False を返します。
get()|キューから要素を削除して返します。
put(item)|item をキューに追加します。
class multiprocessing.JoinableQueue([maxsize])|JoinableQueue は Queue のサブクラスであり、 task_done() や join() メソッドが追加されているキューです。
task_done()|以前にキューへ追加されたタスクが完了したことを表します。キューのコンシューマによって使用されます。 タスクをフェッチするために使用されるそれぞれの get() に対して、 後続の task_done() 呼び出しはタスクの処理が完了したことをキューへ伝えます。
join()|キューにあるすべてのアイテムが取り出されて処理されるまでブロックします。

## [17.2.2.3. その他](https://docs.python.jp/3/library/multiprocessing.html#miscellaneous)

属性|概要
----|----
multiprocessing.active_children()|カレントプロセスのすべてのアクティブな子プロセスのリストを返します。
multiprocessing.cpu_count()|システムの CPU 数を返します。
multiprocessing.current_process()|カレントプロセスに対応する Process オブジェクトを返します。
multiprocessing.freeze_support()|multiprocessing を使用しているプログラムをフリーズして Windows の実行可能形式を生成するためのサポートを追加します。(py2exe , PyInstaller や cx_Freeze でテストされています。)
multiprocessing.get_all_start_methods()|サポートしている開始方式のリストを返します。先頭の要素がデフォルトを意味します。利用可能な開始方式には 'fork'、'spawn' および 'forkserver' があります。Windows では 'spawn' のみが利用可能です。Unix では 'fork' および 'spawn' は常にサポートされており、'fork' がデフォルトになります。
multiprocessing.get_context(method=None)|multiprocessing モジュールと同じ属性を持つコンテキストオブジェクトを返します。
multiprocessing.get_start_method(allow_none=False)|開始するプロセスで使用する開始方式名を返します。
multiprocessing.set_executable()|子プロセスを開始するときに、使用する Python インタープリターのパスを設定します。(デフォルトでは sys.executable が使用されます)。コードに組み込むときは、おそらく次のようにする必要があります
multiprocessing.set_start_method(method)|子プロセスの開始方式を指定します。method には 'fork'、'spawn' あるいは 'forkserver' を指定できます。

### 注釈

> multiprocessing には threading.active_count(), threading.enumerate(), threading.settrace(), threading.setprofile(), threading.Timer や threading.local のような関数はありません。

## [17.2.2.4. Connection オブジェクト](https://docs.python.jp/3/library/multiprocessing.html#connection-objects)

> Connection オブジェクトは pickle でシリアライズ可能なオブジェクトか文字列を送ったり、受け取ったりします。そういったオブジェクトはメッセージ指向の接続ソケットと考えられます。

> Connection オブジェクトは通常は Pipe() を使用して作成されます。詳細は リスナーとクライアント も参照してください。

属性|概要
----|----
class multiprocessing.Connection| 
send(obj)|コネクションの相手側へ recv() を使用して読み込むオブジェクトを送ります。
recv()|Return an object sent from the other end of the connection using send(). Blocks until there is something to receive. Raises EOFError if there is nothing left to receive and the other end was closed.
fileno()|コネクションが使用するハンドラーか、ファイル記述子を返します。
close()|コネクションをクローズします。
poll([timeout])|読み込み可能なデータがあるかどうかを返します。
send_bytes(buffer[, offset[, size]])|bytes-like object から完全なメッセージとしてバイトデータを送ります。
recv_bytes([maxlength])|コネクションの相手側から送られたバイトデータの完全なメッセージを文字列として返します。何か受け取るまでブロックします。受け取るデータが何も残っておらず、相手側がコネクションを閉じていた場合、 EOFError が送出されます。
recv_bytes_into(buffer[, offset])|コネクションの相手側から送られたバイトデータを buffer に読み込み、メッセージのバイト数を返します。 何か受け取るまでブロックします。何も受け取らずにコネクションの相手側でクローズされた場合 EOFError が発生します。

```python
>>> from multiprocessing import Pipe
>>> a, b = Pipe()
>>> a.send([1, 'hello', None])
>>> b.recv()
[1, 'hello', None]
>>> b.send_bytes(b'thank you')
>>> a.recv_bytes()
b'thank you'
>>> import array
>>> arr1 = array.array('i', range(5))
>>> arr2 = array.array('i', [0] * 10)
>>> a.send_bytes(arr1)
>>> count = b.recv_bytes_into(arr2)
>>> assert count == len(arr1) * arr1.itemsize
>>> arr2
array('i', [0, 1, 2, 3, 4, 0, 0, 0, 0, 0])
```

### 警告

> Connection.recv() メソッドは受信したデータを自動的に unpickle 化します。それはメッセージを送ったプロセスが信頼できる場合を除いてセキュリティリスクになります。

> そのため Pipe() を使用してコネクションオブジェクトを生成する場合を除いて、何らかの認証処理を実行した後で recv() や send() メソッドのみを使用すべきです。詳細は 認証キー を参照してください。

### 警告

> もしプロセスがパイプの読み込みまたは書き込み中に kill されると、メッセージの境界がどこなのか分からなくなってしまうので、そのパイプ内のデータは破損してしまいがちです。

## [17.2.2.5. 同期プリミティブ](https://docs.python.jp/3/library/multiprocessing.html#synchronization-primitives)

> 一般的にマルチプロセスプログラムは、マルチスレッドプログラムほどは同期プリミティブを必要としません。詳細は threading モジュールのドキュメントを参照してください。

> マネージャーオブジェクトを使用して同期プリミティブを作成できることも覚えておいてください。詳細は マネージャー を参照してください。

属性|概要
----|----
class multiprocessing.Barrier(parties[, action[, timeout]])|バリアーオブジェクト: threading.Barrier のクローンです。
class multiprocessing.BoundedSemaphore([value])|有限セマフォオブジェクト: threading.BoundedSemaphore の類似物です。
class multiprocessing.Condition([lock])|状態変数: threading.Condition の別名です。
class multiprocessing.Event|threading.Event のクローンです。
class multiprocessing.Lock|再帰しないロックオブジェクトで、 threading.Lock 相当のものです。プロセスやスレッドがロックをいったん獲得 (acquire) すると、それに続くほかのプロセスやスレッドが獲得しようとする際、それが解放 (release) されるまではブロックされます。解放はどのプロセス、スレッドからも行えます。スレッドに対して適用される threading.Lock のコンセプトと振る舞いは、特筆すべきものがない限り、プロセスとスレッドに適用される multiprocessing.Lock に引き継がれています。
acquire(block=True, timeout=None)|ブロックあり、またはブロックなしでロックを獲得します。
release()|ロックを解放します。これはロックを獲得したプロセスやスレッドだけでなく、任意のプロセスやスレッドから呼ぶことができます。
class multiprocessing.RLock|再帰ロックオブジェクトで、 threading.RLock 相当のものです。再帰ロックオブジェクトはそれを獲得 (acquire) したプロセスやスレッドが解放 (release) しなければなりません。プロセスやスレッドがロックをいったん獲得すると、同じプロセスやスレッドはブロックされずに再度獲得出来ます。そのプロセスやスレッドは獲得した回数ぶん解放しなければなりません。
acquire(block=True, timeout=None)|ブロックあり、またはブロックなしでロックを獲得します。
release()|再帰レベルをデクリメントしてロックを解放します。デクリメント後に再帰レベルがゼロになった場合、ロックの状態をアンロック (いかなるプロセス、いかなるスレッドにも所有されていない状態) にリセットし、ロックの状態がアンロックになるのを待ってブロックしているプロセスもしくはスレッドがある場合にはその中のただ一つだけが処理を進行できるようにします。デクリメント後も再帰レベルがゼロでない場合、ロックの状態はロックのままで、呼び出し側のプロセスもしくはスレッドに所有されたままになります。
class multiprocessing.Semaphore([value])|セマフォオブジェクト: threading.Semaphore のクローンです。

### 注釈

> Mac OS X では sem_timedwait がサポートされていないので、acquire() にタイムアウトを与えて呼ぶと、ループ内でスリープすることでこの関数がエミュレートされます。

### 注釈

> メインスレッドが BoundedSemaphore.acquire(), Lock.acquire(), RLock.acquire(), Semaphore.acquire(), Condition.acquire() 又は Condition.wait() を呼び出してブロッキング状態のときに Ctrl-C で生成される SIGINT シグナルを受け取ると、その呼び出しはすぐに中断されて KeyboardInterrupt が発生します。

> これは同等のブロッキング呼び出しが実行中のときに SIGINT が無視される threading の振る舞いとは違っています。

### 注釈

> このパッケージに含まれる機能には、ホストとなるオペレーティングシステム上で動作している共有セマフォを使用しているものがあります。これが使用できない場合には、multiprocessing.synchronize モジュールが無効になり、このモジュールのインポート時に ImportError が発生します。詳細は bpo-3770 を参照してください。 

## [17.2.2.6. 共有 ctypes オブジェクト](https://docs.python.jp/3/library/multiprocessing.html#shared-ctypes-objects)

> 子プロセスにより継承される共有メモリを使用する共有オブジェクトを作成することができます。

属性|概要
----|----
multiprocessing.Value(typecode_or_type, *args, lock=True)|共有メモリから割り当てられた ctypes オブジェクトを返します。 デフォルトでは、返り値は実際のオブジェクトの同期ラッパーです。オブジェクトそれ自身は、 Value の value 属性によってアクセスできます。
multiprocessing.Array(typecode_or_type, size_or_initializer, *, lock=True)|共有メモリから割り当てられた ctypes 配列を返します。デフォルトでは、返り値は実際の配列の同期ラッパーです。

### [17.2.2.6.1. multiprocessing.sharedctypes モジュール](https://docs.python.jp/3/library/multiprocessing.html#module-multiprocessing.sharedctypes)

> multiprocessing.sharedctypes モジュールは子プロセスに継承される共有メモリの ctypes オブジェクトを割り当てる関数を提供します。

### 注釈

> 共有メモリのポインターを格納することは可能ではありますが、特定プロセスのアドレス空間の位置を参照するということを覚えておいてください。しかし、そのポインターは別のプロセスのコンテキストにおいて無効になる確率が高いです。そして、別のプロセスからそのポインターを逆参照しようとするとクラッシュを引き起こす可能性があります。

属性|概要
----|----
multiprocessing.sharedctypes.RawArray(typecode_or_type, size_or_initializer)|共有メモリから割り当てられた ctypes 配列を返します。
multiprocessing.sharedctypes.RawValue(typecode_or_type, *args)|共有メモリから割り当てられた ctypes オブジェクトを返します。
multiprocessing.sharedctypes.Array(typecode_or_type, size_or_initializer, *, lock=True)|RawArray() と同様ですが、 lock の値によっては ctypes 配列をそのまま返す代わりに、プロセスセーフな同期ラッパーが返されます。
multiprocessing.sharedctypes.Value(typecode_or_type, *args, lock=True)|RawValue() と同様ですが、 lock の値によっては ctypes オブジェクトをそのまま返す代わりに、プロセスセーフな同期ラッパーが返されます。
multiprocessing.sharedctypes.copy(obj)|共有メモリから割り当てられた ctypes オブジェクト obj をコピーしたオブジェクトを返します。
multiprocessing.sharedctypes.synchronized(obj[, lock])|同期アクセスに lock を使用する ctypes オブジェクトのためにプロセスセーフなラッパーオブジェクトを返します。 lock が None (デフォルト) なら、 multiprocessing.RLock オブジェクトが自動的に作成されます。

> 次の表は通常の ctypes 構文で共有メモリから共有 ctypes オブジェクトを作成するための構文を比較します。 (MyStruct テーブル内には ctypes.Structure のサブクラスがあります。)

ctypes|type を使用する sharedctypes|typecode を使用する sharedctypes
------|----------------------------|--------------------------------
c_double(2.4)|RawValue(c_double, 2.4)|RawValue('d', 2.4)
MyStruct(4, 6)|RawValue(MyStruct, 4, 6)| 
(c_short * 7)()|RawArray(c_short, 7)|RawArray('h', 7)
(c_int * 3)(9, 2, 8)|RawArray(c_int, (9, 2, 8))|RawArray('i', (9, 2, 8))

> 以下に子プロセスが多くの ctypes オブジェクトを変更する例を紹介します:


```python
from multiprocessing import Process, Lock
from multiprocessing.sharedctypes import Value, Array
from ctypes import Structure, c_double

class Point(Structure):
    _fields_ = [('x', c_double), ('y', c_double)]

def modify(n, x, s, A):
    n.value **= 2
    x.value **= 2
    s.value = s.value.upper()
    for a in A:
        a.x **= 2
        a.y **= 2

if __name__ == '__main__':
    lock = Lock()

    n = Value('i', 7)
    x = Value(c_double, 1.0/3.0, lock=False)
    s = Array('c', b'hello world', lock=lock)
    A = Array(Point, [(1.875,-6.25), (-5.75,2.0), (2.375,9.5)], lock=lock)

    p = Process(target=modify, args=(n, x, s, A))
    p.start()
    p.join()

    print(n.value)
    print(x.value)
    print(s.value)
    print([(a.x, a.y) for a in A])
```

> 結果は以下のように表示されます

```python
49
0.1111111111111111
HELLO WORLD
[(3.515625, 39.0625), (33.0625, 4.0), (5.640625, 90.25)]
```

## [17.2.2.7. マネージャー](https://docs.python.jp/3/library/multiprocessing.html#managers)

> マネージャーは異なるプロセス間で共有されるデータの作成方法を提供します。これには別のマシン上で走るプロセス間のネットワーク越しの共有も含まれます。マネージャーオブジェクトは 共有オブジェクト を管理するサーバープロセスを制御します。他のプロセスはプロキシ経由で共有オブジェクトへアクセスすることができます。

> multiprocessing.Manager()|プロセス間でオブジェクトを共有するために使用される SyncManager オブジェクトを返します。返されたマネージャーオブジェクトは生成される子プロセスに対応付けられ、共有オブジェクトを作成するメソッドや、共有オブジェクトに対応するプロキシを返すメソッドを持ちます。

> マネージャープロセスは親プロセスが終了するか、ガベージコレクトされると停止します。マネージャークラスは multiprocessing.managers モジュールで定義されています:

属性|概要
----|----
class multiprocessing.managers.BaseManager([address[, authkey]])|BaseManager オブジェクトを作成します。
start([initializer[, initargs]])|マネージャーを開始するためにサブプロセスを開始します。initializer が None でなければ、サブプロセスは開始時に initializer(*initargs) を呼び出します。
get_server()|マネージャーの制御下にある実際のサーバーを表す Server オブジェクトを返します。 Server オブジェクトは serve_forever() メソッドをサポートします:
connect()|ローカルからリモートのマネージャーオブジェクトへ接続します:
shutdown()|マネージャーが使用するプロセスを停止します。これはサーバープロセスを開始するために start() が使用された場合のみ有効です。
register(typeid[, callable[, proxytype[, exposed[, method_to_typeid[, create_method]]]]])|マネージャークラスで呼び出し可能オブジェクト(callable)や型を登録するために使用されるクラスメソッドです。
address|マネージャーが使用するアドレスです。
class multiprocessing.managers.SyncManager|プロセス間の同期のために使用される BaseManager のサブクラスです。 multiprocessing.Manager() はこの型のオブジェクトを返します。
Barrier(parties[, action[, timeout]])|共有 threading.Barrier オブジェクトを作成して、そのプロキシを返します。
BoundedSemaphore([value])|共有 threading.BoundedSemaphore オブジェクトを作成して、そのプロキシを返します。
Condition([lock])|共有 threading.Condition オブジェクトを作成して、そのプロキシを返します。
Event()|共有 threading.Event オブジェクトを作成して、そのプロキシを返します。
Lock()|共有 threading.Lock オブジェクトを作成して、そのプロキシを返します。
Namespace()|共有 Namespace オブジェクトを作成して、そのプロキシを返します。
Queue([maxsize])|共有 queue.Queue オブジェクトを作成して、そのプロキシを返します。
RLock()|共有 threading.RLock オブジェクトを作成して、そのプロキシを返します。
Semaphore([value])|共有 threading.Semaphore オブジェクトを作成して、そのプロキシを返します。
Array(typecode, sequence)|配列を作成して、そのプロキシを返します。
Value(typecode, value)|書き込み可能な value 属性を作成して、そのプロキシを返します。
dict(), dict(mapping), dict(sequence)|共有 dict オブジェクトを作成して、そのプロキシを返します。
list(), list(sequence)|共有 list オブジェクトを作成して、そのプロキシを返します。
class multiprocessing.managers.Namespace|SyncManager に登録することのできる型です。

### get_server()

```python
>>> from multiprocessing.managers import BaseManager
>>> manager = BaseManager(address=('', 50000), authkey=b'abc')
>>> server = manager.get_server()
>>> server.serve_forever()
```

### connect()
        
```python
>>> from multiprocessing.managers import BaseManager
>>> m = BaseManager(address=('127.0.0.1', 5000), authkey=b'abc')
>>> m.connect()
```

### class multiprocessing.managers.Namespace

```python
>>> manager = multiprocessing.Manager()
>>> Global = manager.Namespace()
>>> Global.x = 10
>>> Global.y = 'hello'
>>> Global._z = 12.3    # this is an attribute of the proxy
>>> print(Global)
Namespace(x=10, y='hello')
```

### [17.2.2.7.1. カスタマイズされたマネージャー](https://docs.python.jp/3/library/multiprocessing.html#customized-managers)

> 独自のマネージャーを作成するには、BaseManager のサブクラスを作成して、 マネージャークラスで呼び出し可能なオブジェクトか新たな型を登録するために register() クラスメソッドを使用します。例えば:

```python
from multiprocessing.managers import BaseManager

class MathsClass:
    def add(self, x, y):
        return x + y
    def mul(self, x, y):
        return x * y

class MyManager(BaseManager):
    pass

MyManager.register('Maths', MathsClass)

if __name__ == '__main__':
    with MyManager() as manager:
        maths = manager.Maths()
        print(maths.add(4, 3))         # prints 7
        print(maths.mul(7, 8))         # prints 56
```

### [17.2.2.7.2. リモートマネージャーを使用する](https://docs.python.jp/3/library/multiprocessing.html#using-a-remote-manager)

> あるマシン上でマネージャーサーバーを実行して、他のマシンからそのサーバーを使用するクライアントを持つことができます(ファイアウォールを通過できることが前提)。

> 次のコマンドを実行することでリモートクライアントからアクセスを受け付ける1つの共有キューのためにサーバーを作成します:

```python
>>> from multiprocessing.managers import BaseManager
>>> import queue
>>> queue = queue.Queue()
>>> class QueueManager(BaseManager): pass
>>> QueueManager.register('get_queue', callable=lambda:queue)
>>> m = QueueManager(address=('', 50000), authkey=b'abracadabra')
>>> s = m.get_server()
>>> s.serve_forever()
```

> あるクライアントからサーバーへのアクセスは次のようになります:

```python
>>> from multiprocessing.managers import BaseManager
>>> class QueueManager(BaseManager): pass
>>> QueueManager.register('get_queue')
>>> m = QueueManager(address=('foo.bar.org', 50000), authkey=b'abracadabra')
>>> m.connect()
>>> queue = m.get_queue()
>>> queue.put('hello')
```

> 別のクライアントもそれを使用することができます:

```python
>>> from multiprocessing.managers import BaseManager
>>> class QueueManager(BaseManager): pass
>>> QueueManager.register('get_queue')
>>> m = QueueManager(address=('foo.bar.org', 50000), authkey=b'abracadabra')
>>> m.connect()
>>> queue = m.get_queue()
>>> queue.get()
'hello'
```

> ローカルプロセスもそのキューへアクセスすることができます。クライアント上で上述のコードを使用してアクセスします:

```python
>>> from multiprocessing import Process, Queue
>>> from multiprocessing.managers import BaseManager
>>> class Worker(Process):
...     def __init__(self, q):
...         self.q = q
...         super(Worker, self).__init__()
...     def run(self):
...         self.q.put('local hello')
...
>>> queue = Queue()
>>> w = Worker(queue)
>>> w.start()
>>> class QueueManager(BaseManager): pass
...
>>> QueueManager.register('get_queue', callable=lambda: queue)
>>> m = QueueManager(address=('', 50000), authkey=b'abracadabra')
>>> s = m.get_server()
>>> s.serve_forever()
```

## [17.2.2.8. Proxy オブジェクト](https://docs.python.jp/3/library/multiprocessing.html#proxy-objects)

> プロキシは別のプロセスで(おそらく)有効な共有オブジェクトを 参照する オブジェクトです。共有オブジェクトはプロキシの 参照対象 になるということができます。複数のプロキシオブジェクトが同じ参照対象を持つ可能性もあります。

> プロキシオブジェクトはその参照対象の対応するメソッドを呼び出すメソッドを持ちます (そうは言っても、参照対象のすべてのメソッドが必ずしもプロキシ経由で利用可能なわけではありません)。 この方法で、プロキシオブジェクトはまるでその参照先と同じように使えます:

```python
>>> from multiprocessing import Manager
>>> manager = Manager()
>>> l = manager.list([i*i for i in range(10)])
>>> print(l)
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> print(repr(l))
<ListProxy object, typeid 'list' at 0x...>
>>> l[4]
16
>>> l[2:5]
[4, 9, 16]
```

> プロキシに str() を適用すると参照対象のオブジェクト表現を返すのに対して、 repr() を適用するとプロキシのオブジェクト表現を返すことに注意してください。

> プロキシオブジェクトの重要な機能は pickle 化ができることで、これによりプロセス間での受け渡しができます。 そのため、参照対象が Proxy オブジェクト を持てます。 これによって管理されたリスト、辞書、その他 Proxy オブジェクト をネストできます:

```python
>>> a = manager.list()
>>> b = manager.list()
>>> a.append(b)         # referent of a now contains referent of b
>>> print(a, b)
[<ListProxy object, typeid 'list' at ...>] []
>>> b.append('hello')
>>> print(a[0], b)
['hello'] ['hello']
```

> 同様に、辞書とリストのプロキシも他のプロキシの内部に入れてネストできます:

```python
>>> l_outer = manager.list([ manager.dict() for i in range(2) ])
>>> d_first_inner = l_outer[0]
>>> d_first_inner['a'] = 1
>>> d_first_inner['b'] = 2
>>> l_outer[1]['c'] = 3
>>> l_outer[1]['z'] = 26
>>> print(l_outer[0])
{'a': 1, 'b': 2}
>>> print(l_outer[1])
{'c': 3, 'z': 26}
```

> (プロキシでない) 標準の list オブジェクトや dict オブジェクトが参照対象に含まれていた場合、それらの可変な値の変更はマネージャーからは伝搬されません。 というのも、プロキシには参照対象の中に含まれる値がいつ変更されたかを知る術が無いのです。 しかし、コンテナプロキシに値を保存する (これはプロキシオブジェクトの __setitem__ を起動します) 場合はマネージャーを通して変更が伝搬され、その要素を実際に変更するために、コンテナプロキシに変更後の値が再代入されます:

```python
# create a list proxy and append a mutable object (a dictionary)
lproxy = manager.list()
lproxy.append({})
# now mutate the dictionary
d = lproxy[0]
d['a'] = 1
d['b'] = 2
# at this point, the changes to d are not yet synced, but by
# updating the dictionary, the proxy is notified of the change
lproxy[0] = d
```

> This approach is perhaps less convenient than employing nested Proxy オブジェクト for most use cases but also demonstrates a level of control over the synchronization.

注釈

> multiprocessing のプロキシ型は値による比較に対して何もサポートしません。そのため、例えば以下のようになります:

```python
>>> manager.list([1,2,3]) == [1,2,3]
False
```

> 比較を行いたいときは参照対象のコピーを使用してください。

属性|概要
----|----
class multiprocessing.managers.BaseProxy|プロキシオブジェクトは BaseProxy のサブクラスのインスタンスです。
_callmethod(methodname[, args[, kwds]])|プロキシの参照対象のメソッドの実行結果を返します。
_getvalue()|参照対象のコピーを返します。
__repr__()|プロキシオブジェクトのオブジェクト表現を返します。
__str__()|参照対象のオブジェクト表現を返します。

### _callmethod

```python
>>> l = manager.list(range(10))
>>> l._callmethod('__len__')
10
>>> l._callmethod('__getitem__', (slice(2, 7),)) # equivalent to l[2:7]
[2, 3, 4, 5, 6]
>>> l._callmethod('__getitem__', (20,))          # equivalent to l[20]
Traceback (most recent call last):
...
IndexError: list index out of range
```

### [17.2.2.8.1. クリーンアップ](https://docs.python.jp/3/library/multiprocessing.html#cleanup)

> プロキシオブジェクトは弱参照(weakref)コールバックを使用します。プロキシオブジェクトがガベージコレクトされるときにその参照対象が所有するマネージャーからその登録を取り消せるようにするためです。

> 共有オブジェクトはプロキシが参照しなくなったときにマネージャープロセスから削除されます。

## [17.2.2.9. プロセスプール](https://docs.python.jp/3/library/multiprocessing.html#module-multiprocessing.pool)

> Pool クラスでタスクを実行するプロセスのプールを作成することができます。

属性|概要
----|----
class multiprocessing.pool.Pool([processes[, initializer[, initargs[, maxtasksperchild[, context]]]]])|プロセスプールオブジェクトは、ジョブを送り込めるワーカープロセスのプールを制御します。タイムアウトやコールバックのある非同期の実行をサポートし、並列 map 実装を持ちます。
apply(func[, args[, kwds]])|引数 args とキーワード引数 kwds を伴って func を呼びます。結果が準備できるまでブロックします。このブロックがあるため、 apply_async() の方が並行作業により適しています。加えて、 func は、プール内の1つのワーカーだけで実行されます。
apply_async(func[, args[, kwds[, callback[, error_callback]]]])|apply() メソッドの派生版で結果オブジェクトを返します。
map(func, iterable[, chunksize])|map() 組み込み関数の並列版です (iterable な引数を1つだけサポートするという違いはありますが)。結果が出るまでブロックします。
map_async(func, iterable[, chunksize[, callback[, error_callback]]])|map() メソッドの派生版で結果オブジェクトを返します。
imap(func, iterable[, chunksize])|map() の遅延評価版です。
imap_unordered(func, iterable[, chunksize])|イテレーターが返す結果の順番が任意の順番で良いと見なされることを除けば imap() と同じです。 (ワーカープロセスが1つしかない場合のみ "正しい" 順番になることが保証されます。)
starmap(func, iterable[, chunksize])|iterable の要素が、引数として unpack されるイテレート可能オブジェクトであると期待される以外は、 map() と似ています。
starmap_async(func, iterable[, chunksize[, callback[, error_back]]])|starmap() と map_async() の組み合わせです。 イテレート可能オブジェクトの iterable をイテレートして、 unpack したイテレート可能オブジェクトを伴って func を呼び出します。結果オブジェクトを返します。
close()|これ以上プールでタスクが実行されないようにします。すべてのタスクが完了した後でワーカープロセスが終了します。
terminate()|実行中の処理を完了させずにワーカープロセスをすぐに停止します。プールオブジェクトがガベージコレクトされるときに terminate() が呼び出されます。
join()|ワーカープロセスが終了するのを待ちます。 join() を使用する前に close() か terminate() を呼び出さなければなりません。
class multiprocessing.pool.AsyncResult|Pool.apply_async() や Pool.map_async() で返される結果のクラスです。
get([timeout])|結果を受け取ったときに返します。 timeout が None ではなくて、その結果が timeout 秒以内に受け取れない場合 multiprocessing.TimeoutError が発生します。リモートの呼び出しが例外を発生させる場合、その例外は get() が再発生させます。
wait([timeout])|その結果が有効になるか timeout 秒経つまで待ちます。
ready()|その呼び出しが完了しているかどうかを返します。
successful()|その呼び出しが例外を発生させることなく完了したかどうかを返します。その結果が返せる状態でない場合 AssertionError が発生します。

> 次の例はプールの使用例を紹介します:

```python
from multiprocessing import Pool
import time

def f(x):
    return x*x

if __name__ == '__main__':
    with Pool(processes=4) as pool:         # start 4 worker processes
        result = pool.apply_async(f, (10,)) # evaluate "f(10)" asynchronously in a single process
        print(result.get(timeout=1))        # prints "100" unless your computer is *very* slow

        print(pool.map(f, range(10)))       # prints "[0, 1, 4,..., 81]"

        it = pool.imap(f, range(10))
        print(next(it))                     # prints "0"
        print(next(it))                     # prints "1"
        print(it.next(timeout=1))           # prints "4" unless your computer is *very* slow

        result = pool.apply_async(time.sleep, (10,))
        print(result.get(timeout=1))        # raises multiprocessing.TimeoutError
```

## [17.2.2.10. リスナーとクライアント](https://docs.python.jp/3/library/multiprocessing.html#module-multiprocessing.connection)

> 通常、プロセス間でメッセージを渡すにはキューを使用するか Pipe() が返す Connection オブジェクトを使用します。

> しかし multiprocessing.connection モジュールにはさらに柔軟な仕組みがあります。 このモジュールは、基本的にはソケットもしくは Windows の名前付きパイプを扱う高レベルのメッセージ指向 API を提供します。また、 hmac モジュールを使用した ダイジェスト認証 や同時の複数接続のポーリングもサポートします。

属性|概要
----|----
multiprocessing.connection.deliver_challenge(connection, authkey)|ランダム生成したメッセージをコネクションの相手側へ送信して応答を待ちます。
multiprocessing.connection.answer_challenge(connection, authkey)|メッセージを受信して、そのキーとして authkey を使用するメッセージのダイジェストを計算し、ダイジェストを送り返します。
multiprocessing.connection.Client(address[, family[, authenticate[, authkey]]])|address で渡したアドレスを使用するリスナーに対してコネクションを確立しようとして Connection を返します。
accept()|リスナーオブジェクトの名前付きパイプか束縛されたソケット上でコネクションを受け付けて Connection オブジェクトを返します。認証が失敗した場合 AuthenticationError が発生します。
close()|リスナーオブジェクトの名前付きパイプか束縛されたソケットをクローズします。これはリスナーがガベージコレクトされるときに自動的に呼ばれます。そうは言っても、明示的に close() を呼び出す方が望ましいです。
address|リスナーオブジェクトが使用中のアドレスです。
last_accepted|最後にコネクションを受け付けたアドレスです。有効なアドレスがない場合は None になります。
multiprocessing.connection.wait(object_list, timeout=None)|object_list 中のオブジェクトが準備ができるまで待機します。準備ができた object_list 中のオブジェクトのリストを返します。timeout が浮動小数点なら、最大でその秒数だけ呼び出しがブロックします。timeout が None の場合、無制限の期間ブロックします。負のタイムアウトは0と等価です。

### 例

> 次のサーバーコードは認証キーとして 'secret password' を使用するリスナーを作成します。このサーバーはコネクションを待ってクライアントへデータを送信します:

```python
from multiprocessing.connection import Listener
from array import array

address = ('localhost', 6000)     # family is deduced to be 'AF_INET'

with Listener(address, authkey=b'secret password') as listener:
    with listener.accept() as conn:
        print('connection accepted from', listener.last_accepted)

        conn.send([2.25, None, 'junk', float])

        conn.send_bytes(b'hello')

        conn.send_bytes(array('i', [42, 1729]))
```

> 次のコードはサーバーへ接続して、サーバーからデータを受信します:

```python
from multiprocessing.connection import Client
from array import array

address = ('localhost', 6000)

with Client(address, authkey=b'secret password') as conn:
    print(conn.recv())                  # => [2.25, None, 'junk', float]

    print(conn.recv_bytes())            # => 'hello'

    arr = array('i', [0, 0, 0, 0, 0])
    print(conn.recv_bytes_into(arr))    # => 8
    print(arr)                          # => array('i', [42, 1729, 0, 0, 0])
```

> 次のコードは wait() を使って複数のプロセスからのメッセージを同時に待ちます:

```python
import time, random
from multiprocessing import Process, Pipe, current_process
from multiprocessing.connection import wait

def foo(w):
    for i in range(10):
        w.send((i, current_process().name))
    w.close()

if __name__ == '__main__':
    readers = []

    for i in range(4):
        r, w = Pipe(duplex=False)
        readers.append(r)
        p = Process(target=foo, args=(w,))
        p.start()
        # We close the writable end of the pipe now to be sure that
        # p is the only process which owns a handle for it.  This
        # ensures that when p closes its handle for the writable end,
        # wait() will promptly report the readable end as being ready.
        w.close()

    while readers:
        for r in wait(readers):
            try:
                msg = r.recv()
            except EOFError:
                readers.remove(r)
            else:
                print(msg)
```

### [17.2.2.10.1. アドレスフォーマット](https://docs.python.jp/3/library/multiprocessing.html#address-formats)

* 'AF_INET' アドレスは (hostname, port) のタプルになります。 hostname は文字列で port は整数です。
* 'AF_UNIX' アドレスはファイルシステム上のファイル名の文字列です。
* 'AF_PIPE' アドレスは、次の形式を持つ文字列です r'\\.\pipe\PipeName' 。 ServerName という名前のリモートコンピューター上の名前付きパイプに接続するために Client() を使用するには、代わりに r'\\ServerName\pipe\PipeName' 形式のアドレスを使用する必要があります。

> デフォルトでは、2つのバックスラッシュで始まる文字列は 'AF_UNIX' よりも 'AF_PIPE' として推測されることに注意してください。

## [17.2.2.11. 認証キー](https://docs.python.jp/3/library/multiprocessing.html#authentication-keys)

> Connection.recv を使用するとき、データは自動的に unpickle されて受信します。信頼できない接続元からのデータを unpickle することはセキュリティリスクがあります。そのため Listener や Client() はダイジェスト認証を提供するために hmac モジュールを使用します。

> 認証キーはパスワードとして見なされるバイト文字列です。コネクションが確立すると、双方の終点で正しい接続先であることを証明するために 知っているお互いの認証キーを要求します。(双方の終点が同じキーを使用して通信しようとしても、コネクション上でそのキーを送信することは できません。)

> 認証が要求されているにもかかわらず認証キーが指定されていない場合 current_process().authkey の返す値が使用されます。 (詳細は Process を参照してください。) この値はカレントプロセスを作成する Process オブジェクトによって自動的に継承されます。 これは(デフォルトでは)複数プロセスのプログラムの全プロセスが相互にコネクションを 確立するときに使用される1つの認証キーを共有することを意味します。

> 適当な認証キーを os.urandom() を使用して生成することもできます。

## [17.2.2.12. ログ記録](https://docs.python.jp/3/library/multiprocessing.html#logging)

> ロギングのためにいくつかの機能が利用可能です。しかし logging パッケージは、 (ハンドラー種別に依存して)違うプロセスからのメッセージがごちゃ混ぜになるので、プロセスの共有ロックを使用しないことに注意してください。

属性|概要
----|----
multiprocessing.get_logger()|multiprocessing が使用するロガーを返します。必要に応じて新たなロガーを作成します。
multiprocessing.log_to_stderr()|この関数は get_logger() に対する呼び出しを実行しますが、 get_logger によって作成されるロガーを返すことに加えて、 '[%(levelname)s/%(processName)s] %(message)s' のフォーマットを使用して sys.stderr へ出力を送るハンドラーを追加します。

> 以下にロギングを有効にした例を紹介します:

```python
>>> import multiprocessing, logging
>>> logger = multiprocessing.log_to_stderr()
>>> logger.setLevel(logging.INFO)
>>> logger.warning('doomed')
[WARNING/MainProcess] doomed
>>> m = multiprocessing.Manager()
[INFO/SyncManager-...] child process calling self.run()
[INFO/SyncManager-...] created temp directory /.../pymp-...
[INFO/SyncManager-...] manager serving at '/.../listener-...'
>>> del m
[INFO/MainProcess] sending shutdown message to manager
[INFO/SyncManager-...] manager exiting with exitcode 0
```

> 完全なロギングレベルの表については logging モジュールを参照してください。

## [17.2.2.13. multiprocessing.dummy モジュール](https://docs.python.jp/3/library/multiprocessing.html#module-multiprocessing.dummy)

> multiprocessing.dummy は multiprocessing の API を複製しますが threading モジュールのラッパーでしかありません。

