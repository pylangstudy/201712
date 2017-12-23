# [18.5.6. サブプロセス](https://docs.python.jp/3/library/asyncio-subprocess.html)

< [18.5. asyncio — 非同期 I/O、イベントループ、コルーチンおよびタスク](https://docs.python.jp/3/library/asyncio.html) < [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

* Source code: [Lib/asyncio/subprocess.py](https://github.com/python/cpython/tree/3.6/Lib/asyncio/subprocess.py)

## [18.5.6.1. Windows でのイベントループ](https://docs.python.jp/3/library/asyncio-subprocess.html#windows-event-loop)

> Windows では、デフォルトのイベントループは SelectorEventLoop になりますが、これはサブプロセスをサポートしていません。代わりに ProactorEventLoop を使用します。Windows で使用する例:

```python
import asyncio, sys

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
```

> 参考

> 利用可能なイベントループ および プラットフォームでのサポート。 

## [18.5.6.2. サブプロセスの作成: Process を使用した高水準 API](https://docs.python.jp/3/library/asyncio-subprocess.html#create-a-subprocess-high-level-api-using-process)

属性|概要
----|----
coroutine asyncio.create_subprocess_exec(*args, stdin=None, stdout=None, stderr=None, loop=None, limit=None, **kwds)|サブプロセスを作成します。
coroutine asyncio.create_subprocess_shell(cmd, stdin=None, stdout=None, stderr=None, loop=None, limit=None, **kwds)|シェルコマンド cmd を実行します。

> パイプに接続するには AbstractEventLoop.connect_read_pipe() および AbstractEventLoop.connect_write_pipe() メソッドを使用します。

## [18.5.6.3. サブプロセスの作成: subprocess.Popen を使用した低水準 API](https://docs.python.jp/3/library/asyncio-subprocess.html#create-a-subprocess-low-level-api-using-subprocess-popen)

> subprocess モジュールを使用して非同期にサブプロセスを実行します。

属性|概要
----|----
coroutine AbstractEventLoop.subprocess_exec(protocol_factory, *args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)|1 個以上の文字列引数 (ファイルシステムエンコーディング にエンコードされた文字列またはバイト列) からサブプロセスを作成します。先頭の文字列で実行するプログラムを指定し、残りの文字列でプログラムの引数を指定します (それが Python スクリプトであれば、sys.argv の値に相当します)。これは標準ライブラリの subprocess.Popen クラスが shell=False で呼び出され、文字列のリストが第 1 引数として渡されたときと似ていますが、Popen が引数として文字列のリストを 1 個取るのに対し、subprocess_exec() 引数として複数の文字列を取ります。
coroutine AbstractEventLoop.subprocess_shell(protocol_factory, cmd, *, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, **kwargs)|プラットフォームの "シェル" 構文を使用して cmd (ファイルシステムエンコーディング にエンコードされた文字列またはバイト列) からサブプロセスを作成します。これは標準ライブラリ subprocess.Popen クラスを shell=True で呼び出したときと似ています。

> 参考

> AbstractEventLoop.connect_read_pipe() および AbstractEventLoop.connect_write_pipe() メソッド。

## [18.5.6.4. 定数](https://docs.python.jp/3/library/asyncio-subprocess.html#constants)

属性|概要
----|----
asyncio.subprocess.PIPE|create_subprocess_shell() および create_subprocess_exec() の引数 stdin、stdout あるいは stderr で使用できる特殊な値です。オープンすべき標準ストリームへのパイプを示します。
asyncio.subprocess.STDOUT|create_subprocess_shell() および create_subprocess_exec() の引数 stderr で使用できる特殊な値です。標準エラー出力を標準出力と同様に扱うための標準出力へのパイプを示します。
asyncio.subprocess.DEVNULL|create_subprocess_shell() および create_subprocess_exec() の引数 stdin、stdout あるいは stderr で使用できる特殊な値です。特殊ファイル os.devnull を使用するよう示します。

## [18.5.6.5. Process](https://docs.python.jp/3/library/asyncio-subprocess.html#process)

属性|概要
----|----
class asyncio.subprocess.Process|関数 create_subprocess_exec() あるいは create_subprocess_shell() によって作成されたサブプロセスです。
coroutine wait()|プロセスの終了を待ちます。リターンコードが returncode 属性に設定され、返されます。
coroutine communicate(input=None)|プロセスと交信、すなわち、標準入力へのデータ送信、EOF に達するまで標準出力および標準エラー出力からのデータ受信、およびプロセスの終了の待機を行います。任意の引数 input は子プロセスに送信するデータを設定します。送信するデータがない場合は None を設定します (デフォルト)。input はバイト列でなければなりません。
send_signal(signal)|子プロセスにシグナル signal を送信します。
terminate()|子プロセスを停止します。POSIX システムでは、子プロセスに signal.SIGTERM を送信します。Windows では、Win32 API 関数 TerminateProcess() が呼び出されます。
kill()|子プロセスを kill します。POSIX システムでは SIGKILL を子プロセスに送信します。Windows では kill() は terminate() の別名になります。
stdin|標準入力ストリーム (StreamWriter) になります。プロセスが stdin=None で作成されていた場合 None になります。
stdout|標準出力ストリーム (StreamReader) になります。プロセスが stdout=None で作成されていた場合 None になります。
stderr|標準エラー出力ストリーム (StreamReader) になります。プロセスが stderr=None で作成されていた場合 None になります。
pid|プロセスの識別子です。
returncode|プロセスが終了したときのリターンコードです。None 値はプロセスがまだ終了していないことを示します。

## [18.5.6.6. サブプロセスとスレッド](https://docs.python.jp/3/library/asyncio-subprocess.html#subprocess-and-threads)

> asyncio はサブプロセスを異なるスレッドから実行するのをサポートしていますが、制限があります:

* イベントループはメインスレッド内で実行されなければなりません
* 子ウォッチャーは、他のスレッドからサブプロセスが実行される前に、メインスレッドで作成されなければなりません。 メインスレッドで get_child_watcher() を呼んで子ウォッチャーをインスタンス化してください。

> asyncio.subprocess.Process クラスはスレッド安全ではありません。

> 参考

* [asyncio-multithreading](https://docs.python.jp/3/library/asyncio-dev.html#asyncio-multithreading)

## [18.5.6.7. サブプロセスの例](https://docs.python.jp/3/library/asyncio-subprocess.html#subprocess-examples)

### [18.5.6.7.1. トランスポートおよびプロトコルを使用したサブプロセス](https://docs.python.jp/3/library/asyncio-subprocess.html#subprocess-using-transport-and-protocol)

> サブプロセスの出力を取得しサブプロセスの終了を待機するサブプロセスプロトコルの例です。サブプロセスは AbstractEventLoop.subprocess_exec() メソッドで作成されます:

```python
import asyncio
import sys

class DateProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future):
        self.exit_future = exit_future
        self.output = bytearray()

    def pipe_data_received(self, fd, data):
        self.output.extend(data)

    def process_exited(self):
        self.exit_future.set_result(True)

@asyncio.coroutine
def get_date(loop):
    code = 'import datetime; print(datetime.datetime.now())'
    exit_future = asyncio.Future(loop=loop)

    # Create the subprocess controlled by the protocol DateProtocol,
    # redirect the standard output into a pipe
    create = loop.subprocess_exec(lambda: DateProtocol(exit_future),
                                  sys.executable, '-c', code,
                                  stdin=None, stderr=None)
    transport, protocol = yield from create

    # Wait for the subprocess exit using the process_exited() method
    # of the protocol
    yield from exit_future

    # Close the stdout pipe
    transport.close()

    # Read the output which was collected by the pipe_data_received()
    # method of the protocol
    data = bytes(protocol.output)
    return data.decode('ascii').rstrip()

if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

date = loop.run_until_complete(get_date(loop))
print("Current date: %s" % date)
loop.close()
```

### [18.5.6.7.2. ストリームを使用したサブプロセス](https://docs.python.jp/3/library/asyncio-subprocess.html#subprocess-using-streams)

> サブプロセスを制御する Process クラスと標準出力から読み込む StreamReader クラスを使用した例で得す。サブプロセスは create_subprocess_exec() 関数で作成されます:

```python
import asyncio.subprocess
import sys

@asyncio.coroutine
def get_date():
    code = 'import datetime; print(datetime.datetime.now())'

    # Create the subprocess, redirect the standard output into a pipe
    create = asyncio.create_subprocess_exec(sys.executable, '-c', code,
                                            stdout=asyncio.subprocess.PIPE)
    proc = yield from create

    # Read one line of output
    data = yield from proc.stdout.readline()
    line = data.decode('ascii').rstrip()

    # Wait for the subprocess exit
    yield from proc.wait()
    return line

if sys.platform == "win32":
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
else:
    loop = asyncio.get_event_loop()

date = loop.run_until_complete(get_date())
print("Current date: %s" % date)
loop.close()
```

