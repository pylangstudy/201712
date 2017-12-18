# [18.5.1. 基底イベントループ]()

< [18.5. asyncio — 非同期 I/O、イベントループ、コルーチンおよびタスク](https://docs.python.jp/3/library/asyncio.html) < [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

> バージョン 3.4 で追加.

* ソースコード: [Lib/asyncio/](https://github.com/python/cpython/tree/3.6/Lib/asyncio/)
* ソースコード: [Lib/asyncio/events.py](https://github.com/python/cpython/tree/3.6/Lib/asyncio/events.py)

イベントループは asyncio が提供する中心実行デバイスです。以下の多くの機能を提供しています:

* 遅延呼び出しの登録、実行およびキャンセル (タイムアウト)。
* さまざまな種類の通信のためのクライアントおよびサーバー トランスポート の作成。
* 外部プログラムとの通信のためのサブプロセスおよび関連する トランスポート の起動。
* スレッドのプールへ呼び出す、コストの大きい関数の委譲。

属性|概要
----|----
class asyncio.BaseEventLoop|このクラスは実装詳細です。 AbstractEventLoop のサブクラスであり、 asyncio にあるイベントループを実装した具象クラスの基底クラスになっていることがあります。このクラスは直接使うべきではありません。 AbstractEventLoop を代わりに使用してください。サードパーティのコードで BaseEventLoop をサブクラス化すべきではありません。このクラスの内部のインタフェースは安定していません。
class asyncio.AbstractEventLoop|イベントループの抽象基底クラスです。 このクラスは スレッド安全ではありません。

## [18.5.1.1. イベントループの実行]()

属性|概要
----|----
AbstractEventLoop.run_forever()|stop() が呼ばれるまで実行します。もし run_forever() が呼ばれる前に stop() が呼ばれた場合、このメソッドは I/O セレクターをタイムアウト時間ゼロで一度ポーリングして、そこで検出された I/O イベントに応じて実行がスケジュールされたコールバックすべて (に加えて元々スケジュールされていたもの) を実行した後、終了します。もし run_forever() の実行中に stop() が呼ばれた場合、現在バッチ処理中のコールバックを実行した後に終了します。なお、この場合はコールバック内でスケジュールされたコールバックは実行されません。それらは次に run_forever() が呼ばれたときに実行されます。
AbstractEventLoop.run_until_complete(future)|Future が完了するまで実行します。
AbstractEventLoop.is_running()|イベントループの実行状態を返します。
AbstractEventLoop.stop()|実行中のイベントループを停止します。
AbstractEventLoop.is_closed()|イベントループが閉じられていた場合 True を返します。
AbstractEventLoop.close()|イベントループを閉じます。ループは実行中ではいけません。保留中のコールバックは失われます。
coroutine AbstractEventLoop.shutdown_asyncgens()|現在オープンの全ての asynchronous generator オブジェクトをスケジュールし、aclose() 呼び出しによりクローズするようにします。このメソッドの呼び出し後、イベントループは新しい非同期ジェネレータがイテレートされると毎回警告を発します。全てのスケジュールされた非同期ジェネレータの終了処理を確実に行うために使用すべきです。以下に例を示します。

## [18.5.1.2. 呼び出し (call)]()

> asyncio 関数の大半はキーワードを受け付けません。 コールバックに引数を渡したい場合は functools.partial() を使用してください。 例えば loop.call_soon(functools.partial(print, "Hello", flush=True)) は print("Hello", flush=True) を呼び出します。

> 注釈

> lambda 関数よりも functools.partial() を使用しましょう。 asyncio はデバッグモードで引数を表示するよう functools.partial() オブジェクトを精査することが出来ますが、lambda 関数の表現は貧弱です。

属性|概要
----|----
AbstractEventLoop.call_soon(callback, *args)|コールバックをすぐに呼び出せるように準備します。 コールバックは call_soon() が返ると呼び出され、制御はイベントループに返されます。
AbstractEventLoop.call_soon_threadsafe(callback, *args)|call_soon() に似ていますが、スレッドセーフです。

## [18.5.1.3. 遅延呼び出し]()

> イベントループはタイムアウトを計測するために自身に内部時計を持っています。内部時計は (プラットフォーム固有の) イベントループの実装に依存したものが使用されます。理想的には、これは単調時計 (訳注: 巻き戻ることのない時計) です。これは通常 time.time() とは異なる時計です。

> 注釈

> タイムアウト (相対値 delay または絶対値 when) は 1 日を超えてはいけません。

属性|概要
----|----
AbstractEventLoop.call_later(delay, callback, *args)|引数 delay 秒後に callback を呼び出す準備をします。delay は int または float です。
AbstractEventLoop.call_at(when, callback, *args)|絶対タイムスタンプ when (int または float) になったときに呼び出される callback を準備します。 時刻は AbstractEventLoop.time() を参照します。
AbstractEventLoop.time()|現在の時刻を float 値で返します。時刻はイベントループの内部時計に従います。

> 参考

> 関数 asyncio.sleep()。

## [18.5.1.4. Future]()

属性|概要
----|----
AbstractEventLoop.create_future()|ループに付属した asyncio.Future オブジェクトを作成します。

## [18.5.1.5. タスク]()

属性|概要
----|----
AbstractEventLoop.create_task(coro)|コルーチンオブジェクト の実行をスケジュールします: このときフューチャにラップします。Task オブジェクトを返します。
AbstractEventLoop.set_task_factory(factory)|AbstractEventLoop.create_task() が使用するタスクファクトリーを設定します。
AbstractEventLoop.get_task_factory()|タスクファクトリーを返します。デフォルトのものが使用された場合は None を返します。

## [18.5.1.6. コネクションの作成]()

属性|概要
----|----
coroutine AbstractEventLoop.create_connection(protocol_factory, host=None, port=None, *, ssl=None, family=0, proto=0, flags=0, sock=None, local_addr=None, server_hostname=None)|インターネット host および port へのストリーミング転送コネクションを作成します: ソケットファミリ AF_INET または AF_INET6 は host (または指定されていれば family) に依存し、ソケットタイプは SOCK_STREAM になります。protocol_factory は プロトコル のインスタンスを返す呼び出し可能オブジェクトでなければなりません。
coroutine AbstractEventLoop.create_datagram_endpoint(protocol_factory, local_addr=None, remote_addr=None, *, family=0, proto=0, flags=0, reuse_address=None, reuse_port=None, allow_broadcast=None, sock=None)|データグラム接続を作成します: ソケットファミリー AF_INET または AF_INET6 は host (または指定されていれば family) に依存し、ソケットタイプは SOCK_DGRAM です。 protocol_factory は プロトコル のインスタンスを返す呼び出し可能オブジェクトでなければなりません。
coroutine AbstractEventLoop.create_unix_connection(protocol_factory, path, *, ssl=None, sock=None, server_hostname=None)|UNIX コネクションを作成します: ソケットファミリは AF_UNIX、ソケットタイプは SOCK_STREAM になります。AF_UNIX ソケットファミリは同一マシン上のプロセス間で効率的に通信するために使用されます。

## [18.5.1.7. 待ち受けコネクションの作成]()

属性|概要
----|----
coroutine AbstractEventLoop.create_server(protocol_factory, host=None, port=None, *, family=socket.AF_UNSPEC, flags=socket.AI_PASSIVE, sock=None, backlog=100, ssl=None, reuse_address=None, reuse_port=None)|host および port に束縛された TCP サーバー (ソケットタイプ SOCK_STREAM) を作成します。
coroutine AbstractEventLoop.create_unix_server(protocol_factory, path=None, *, sock=None, backlog=100, ssl=None)|AbstractEventLoop.create_server() と似ていますが、ソケットファミリー AF_UNIX 固有です。
coroutine BaseEventLoop.connect_accepted_socket(protocol_factory, sock, *, ssl=None)|受け付けられた接続を扱います。
AbstractEventLoop.add_reader(fd, callback, *args)|読み込み可能なファイル記述子の監視を開始し、指定された引数で callback を呼び出します。
AbstractEventLoop.remove_reader(fd)|読み込み可能なファイル記述子の監視を停止します。
AbstractEventLoop.add_writer(fd, callback, *args)|書き込み可能なファイル記述子の監視を開始し、指定された引数で callback を呼び出します。
AbstractEventLoop.remove_writer(fd)|書き込み可能なファイル記述子の監視を停止します。

## [18.5.1.9. 低水準のソケット操作]()

属性|概要
----|----
coroutine AbstractEventLoop.sock_recv(sock, nbytes)|ソケットからデータを受け取ります。 socket.socket.recv() メソッドのブロックをモデルにしています。
coroutine AbstractEventLoop.sock_sendall(sock, data)|ソケットにデータを送ります。 socket.socket.sendall() メソッドのブロックをモデルにいています。
coroutine AbstractEventLoop.sock_connect(sock, address)|address のソケットに接続します。 socket.socket.connect() メソッドのブロックをモデルにしています。
coroutine AbstractEventLoop.sock_accept(sock)|接続を受け付けます。 socket.socket.accept() のブロック をモデルにしています。

## [18.5.1.10. ホスト名の解決]()

属性|概要
----|----
coroutine AbstractEventLoop.getaddrinfo(host, port, *, family=0, type=0, proto=0, flags=0)|このメソッドは コルーチン で、socket.getaddrinfo() 関数に似ていますが、ブロックされません。
coroutine AbstractEventLoop.getnameinfo(sockaddr, flags=0)|このメソッドは コルーチン で、socket.getnameinfo() 関数に似ていますが、ブロックされません。

## [18.5.1.11. パイプの接続]()

> Windows の SelectorEventLoop では、これらメソッドはサポートされていません。Windows でパイプをサポートするには、ProactorEventLoop を使用してください。

属性|概要
----|----
coroutine AbstractEventLoop.connect_read_pipe(protocol_factory, pipe)|イベントループ内で読み込みパイプを登録します。
coroutine AbstractEventLoop.connect_write_pipe(protocol_factory, pipe)|イベントループ内の書き込みパイプを登録します。

## [18.5.1.12. UNIX シグナル]()

> 利用できる環境: UNIX のみ。

属性|概要
----|----
AbstractEventLoop.add_signal_handler(signum, callback, *args)|シグナル用のハンドラーを追加します。
AbstractEventLoop.remove_signal_handler(sig)|シグナル用のハンドラーを削除します。

> 参考

> signal モジュール。

## [18.5.1.13. 実行者]()

> Executor (スレッドプールまたはプロセスプール) 内の関数を呼び出します。デフォルトでは、一つのイベントループは一つのスレッドプール実行者 (ThreadPoolExecutor) を使用します。

属性|概要
----|----
coroutine AbstractEventLoop.run_in_executor(executor, func, *args)|特定の実行者で func を呼び出す準備をします。
AbstractEventLoop.set_default_executor(executor)|run_in_executor() で使用される実行者を設定します。

## [18.5.1.14. エラーハンドリング API]()

> イベントループ内での例外の扱い方をカスタマイズできます。

属性|概要
----|----
AbstractEventLoop.set_exception_handler(handler)|handler を新しいイベントループ例外ハンドラーとして設定します。
AbstractEventLoop.get_exception_handler()|例外ハンドラを返します。デフォルトのものが使用されている場合は None を返します。
AbstractEventLoop.default_exception_handler(context)|デフォルトの例外ハンドラーです。
AbstractEventLoop.call_exception_handler(context)|現在のイベントループ例外ハンドラーを呼び出します。

## [18.5.1.15. デバッグモード]()

属性|概要
----|----
AbstractEventLoop.get_debug()|イベントループのデバッグモード (bool) を取得します。
AbstractEventLoop.set_debug(enabled: bool)|イベントループのデバッグモードを設定します。

> 参考

> asyncio のデバッグモード。

## [18.5.1.16. サーバー]()

属性|概要
----|----
class asyncio.Server|ソケット上で待機しているサーバーです。
close()|サーバーを停止します: 待機しているソケットをクローズし sockets 属性に None を設定します。
coroutine wait_closed()|close() メソッドが完了するまで待ちます。
sockets|サーバーが待機している socket.socket オブジェクトのリストです。サーバーが停止しているときは None になります。

## [18.5.1.17. ハンドル]()

属性|概要
----|----
class asyncio.Handle|AbstractEventLoop.call_soon(), AbstractEventLoop.call_soon_threadsafe(), AbstractEventLoop.call_later(), および AbstractEventLoop.call_at() が返すコールバックラッパです。
cancel()|呼び出しをキャンセルします。コールバックが既にキャンセルされていたり実行されていた場合、このメソッドの影響はありません。

## [18.5.1.18. イベントループの例]()

### [18.5.1.18.1. call_soon() を使った Hello World]()

> AbstractEventLoop.call_soon() メソッドを使用してコールバックをスケジュールする例です。 コールバックは "Hello World" を表示してイベントループを停止します:

```python
import asyncio

def hello_world(loop):
    print('Hello World')
    loop.stop()

loop = asyncio.get_event_loop()

# Schedule a call to hello_world()
loop.call_soon(hello_world, loop)

# Blocking call interrupted by loop.stop()
loop.run_forever()
loop.close()
```

> 参考

> コルーチンを使った Hello World の例では コルーチン を使用しています。

### [18.5.1.18.2. call_later() で現在の日時を表示する]()

> 現在の日時を毎秒表示するコールバックの例です。コールバックは AbstractEventLoop.call_later() を使用して 5 秒間自身を再スケジュールし、イベントループを停止します。

```python
import asyncio
import datetime

def display_date(end_time, loop):
    print(datetime.datetime.now())
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, display_date, end_time, loop)
    else:
        loop.stop()

loop = asyncio.get_event_loop()

# Schedule the first call to display_date()
end_time = loop.time() + 5.0
loop.call_soon(display_date, end_time, loop)

# Blocking call interrupted by loop.stop()
loop.run_forever()
loop.close()
```

> 参考

> 現在の日時を表示するコルーチン の例は コルーチン を使用しています。

### [18.5.1.18.3. 読み込みイベント用ファイル記述子の監視]()

> ファイル記述子が AbstractEventLoop.add_reader() を使用してデータを受信するまで待機し、その後イベントループを閉じます。

```python
import asyncio
try:
    from socket import socketpair
except ImportError:
    from asyncio.windows_utils import socketpair

# Create a pair of connected file descriptors
rsock, wsock = socketpair()
loop = asyncio.get_event_loop()

def reader():
    data = rsock.recv(100)
    print("Received:", data.decode())
    # We are done: unregister the file descriptor
    loop.remove_reader(rsock)
    # Stop the event loop
    loop.stop()

# Register the file descriptor for read event
loop.add_reader(rsock, reader)

# Simulate the reception of data from the network
loop.call_soon(wsock.send, 'abc'.encode())

# Run the event loop
loop.run_forever()

# We are done, close sockets and the event loop
rsock.close()
wsock.close()
loop.close()
```


> 参考

> プロトコルを使ってデータを待つオープンソケットの登録 の例では AbstractEventLoop.create_connection() メソッドによって作成された低レベルプロトコルを使用しています。

> ストリームを使ってデータを待つオープンソケットの登録 の例ではコルーチンの open_connection() 関数によって作成された高水準ストリームを使用しています。

### [18.5.1.18.4. SIGINT および SIGTERM 用のシグナルハンドラーの設定]()

> AbstractEventLoop.add_signal_handler() メソッドを使用した、シグナル SIGINT および SIGTERM 用のハンドラを登録します。

```python
import asyncio
import functools
import os
import signal

def ask_exit(signame):
    print("got signal %s: exit" % signame)
    loop.stop()

loop = asyncio.get_event_loop()
for signame in ('SIGINT', 'SIGTERM'):
    loop.add_signal_handler(getattr(signal, signame),
                            functools.partial(ask_exit, signame))

print("Event loop running forever, press Ctrl+C to interrupt.")
print("pid %s: send SIGINT or SIGTERM to exit." % os.getpid())
try:
    loop.run_forever()
finally:
    loop.close()
```

> この例は UNIX でのみ動きます。

