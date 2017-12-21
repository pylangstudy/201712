# [18.5.4. Transports and protocols (callback based API)](https://docs.python.jp/3/library/asyncio-protocol.html)

< [18.5. asyncio — 非同期 I/O、イベントループ、コルーチンおよびタスク](https://docs.python.jp/3/library/asyncio.html) < [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

* Source code: [Lib/asyncio/transports.py](https://github.com/python/cpython/tree/3.6/Lib/asyncio/transports.py)
* Source code: [Lib/asyncio/protocols.py](https://github.com/python/cpython/tree/3.6/Lib/asyncio/protocols.py)

## [18.5.4.1. トランスポート](https://docs.python.jp/3/library/asyncio-protocol.html#transports)

> トランスポートは、asyncio が提供する、さまざまな種類の通信チャンネルを抽象化するクラス群です。通常あなた自身が直接トランスポートのインスタンスを作成することはなく、AbstractEventLoop のメソッドを呼び出すことでトランスポートとその下層の通信チャンネルのインスタンスが作成され、成功時にコールバックが返ります。

> いったん通信チャンネルが確立されると、トランスポートは常に プロトコル インスタンスとのペアを成します。プロトコルはその後さまざまな用途のためトランスポートのメソッドを呼び出します。

> asyncio は現在 TCP、UDP、SSL およびサブプロセスパイプのトランスポートを実装しています。利用可能なトランスポートのメソッドはトランスポートの種類に依存します。

> トランスポートクラスは スレッド安全ではありません。

> バージョン 3.6 で変更: デフォルトでソケットオプションの TCP_NODELAY が設定されるようになりました。

### [18.5.4.1.1. BaseTransport](https://docs.python.jp/3/library/asyncio-protocol.html#basetransport)

属性|概要
----|----
class asyncio.BaseTransport|トランスポートの基底クラスです。
close()|トランスポートをクローズします。トランスポートが発信データのバッファーを持っていた場合、バッファーされたデータは非同期にフラッシュされます。それ以降データは受信されません。バッファーされていたデータがすべてフラッシュされた後、そのプロトコルの connection_lost() メソッドが引数 None で呼び出されます。
is_closing()|トランスポートを閉じている最中か閉じていた場合 True を返します。
get_extra_info(name, default=None)|オプションのトランスポート情報を返します。name は取得したトランスポート固有の情報を表す文字列で、default は情報が存在しなかったときに返す値になります。
set_protocol(protocol)|新しいプロトコルを設定します。プロトコルの切り替えは、両方のプロトコルのドキュメントで切り替えがサポートされている場合にのみ行うべきです。
get_protocol()|現在のプロトコルを返します。

### [18.5.4.1.2. ReadTransport](https://docs.python.jp/3/library/asyncio-protocol.html#readtransport)

属性|概要
----|----
class asyncio.ReadTransport|読み出し専用トランスポートのインターフェースです。
pause_reading()|トランスポートの受信側を一時停止します。resume_reading() が呼び出されるまでそのプロトコルの data_received() メソッドにデータは渡されません。
resume_reading()|受信を再開します。読み込み可能データが存在した場合そのプロトコルの data_received() メソッドが一度呼び出されます。

### [18.5.4.1.3. WriteTransport](https://docs.python.jp/3/library/asyncio-protocol.html#writetransport)

属性|概要
----|----
class asyncio.WriteTransport|書き込み専用トランスポートのインターフェースです。
abort()|トランスポートを即座にクローズします。未完了の処理があってもそれを待ちません。バッファーされているデータは失われます。それ以降データは受信されません。最終的にそのプロトコルの connection_lost() メソッドが引数 None で呼び出されます。
can_write_eof()|トランスポートが write_eof() をサポートしている場合 True を、サポートしていない場合は False を返します。
get_write_buffer_size()|トランスポートで使用されている出力バッファーの現在のサイズを返します。
get_write_buffer_limits()|書き込みフロー制御の 最高 および 最低 水位点 (high- and low-water limits) を取得します。(low, high) のタプルを返します。low および high は整数のバイト列になります。
set_write_buffer_limits(high=None, low=None)|書き込みフロー制御の 最高 および 最低 水位点 (high- and low-water limits) を設定します。
write(data)|トランスポートにバイト列 data を書き込みます。
writelines(list_of_data)|バイト列のデータのリスト (またはイテラブル) をトランスポートに書き込みます。この振る舞いはイテラブルを yield して各要素で write() を呼び出すことと等価ですが、より効率的な実装となる場合があります。
write_eof()|バッファーされたデータをフラッシュした後トランスポートの送信側をクローズします。データは受信されます。

### [18.5.4.1.4. DatagramTransport](https://docs.python.jp/3/library/asyncio-protocol.html#datagramtransport)

属性|概要
----|----
DatagramTransport.sendto(data, addr=None)|リモートピア addr (トランスポート依存の対象アドレス) にバイト列 data を送信します。addr が None の場合、データはトランスポートの作成時に指定された送信先に送られます。
DatagramTransport.abort()|トランスポートを即座にクローズします。未完了の処理があってもそれを待ちません。バッファーされているデータは失われます。それ以降データは受信されません。最終的にそのプロトコルの connection_lost() メソッドが引数 None で呼び出されます。

### [18.5.4.1.5. BaseSubprocessTransport](https://docs.python.jp/3/library/asyncio-protocol.html#basesubprocesstransport)

属性|概要
----|----
class asyncio.BaseSubprocessTransport|get_pid()|サブプロセスのプロセス ID (整数) を返します。
get_pipe_transport(fd)|整数のファイル記述子 fd に該当する通信パイプのトランスポートを返します:
get_returncode()|サブプロセスのリターンコード (整数) を返します。リターンコードを持たない場合 None を返します。subprocess.Popen.returncode 属性と同じです。
kill()|subprocess.Popen.kill() と同様に、サブプロセスを kill します。
send_signal(signal)|サブプロセスにシグナル signal を送信します。subprocess.Popen.send_signal() と同じです。
terminate()|サブプロセスに停止を要求します。subprocess.Popen.terminate() と同じです。このメソッドは close() メソッドの別名です。
close()|サブプロセスがまだ返していない場合、terminate() メソッドの呼び出しによってサブプロセスに停止を要求し、全パイプ (stdin、stdout および stderr) のトランスポートをクローズします。

## [18.5.4.2. プロトコル](https://docs.python.jp/3/library/asyncio-protocol.html#protocols)

> asyncio はネットワークプロトコルの実装をサブクラス化する基底クラスを提供します。これらクラスは トランスポート と連動して使用されます: プロトコルは入力データの解析および出力データの書き込みのための問い合わせを行い、トランスポートは実際の I/O とバッファリングに責任を持ちます。

> プロトコルクラスをサブクラス化するとき、いくつかのメソッドをオーバーライドすることを推奨します。これらメソッドはコールバックです: いくつかのイベントが発生したとき (例えばデータの受信など) に呼び出されます; あなたがトランスポートを実装する場合を除き、これらを直接呼び出すべきではありません。

> 注釈

> すべてのコールバックはデフォルトで空の実装を持ちます。したがって、あなたが興味を持ったイベント用のコールバックのみ実装が必要になります。

### [18.5.4.2.1. プロトコルクラス群](https://docs.python.jp/3/library/asyncio-protocol.html#protocol-classes)

属性|概要
----|----
class asyncio.Protocol|(例えば TCP や SSL トランスポートとともに使用する) ストリーミングプロトコルを実装する基底クラスです。
class asyncio.DatagramProtocol|(例えば UDP トランスポートともに使用する) データグラムプロトコルを実装する基底クラスです。
class asyncio.SubprocessProtocol|子プロセスと (一方向パイプを使用して) 通信するプロトコルを実装する基底クラスです。

### [18.5.4.2.2. コネクションコールバック](https://docs.python.jp/3/library/asyncio-protocol.html#connection-callbacks)

> これらコールバックは Protocol、DatagramProtocol および SubprocessProtocol インスタンスから呼び出される場合があります:

属性|概要
----|----
BaseProtocol.connection_made(transport)|コネクションが作成されたときに呼び出されます。
BaseProtocol.connection_lost(exc)|コネクションが失われた、あるいはクローズされたときに呼び出されます。
SubprocessProtocol.pipe_data_received(fd, data)|子プロセスが自身の標準出力や標準エラー出力のパイプにデータを書き込んだときに呼び出されます。fd はパイプのファイル記述子 (整数) になります。data はデータを含む空ではないバイト列になります。
SubprocessProtocol.pipe_connection_lost(fd, exc)|子プロセスと通信するパイプの一つがクローズされると呼び出されます。fd はクローズされたファイル記述子 (整数) になります。
SubprocessProtocol.process_exited()|子プロセスが終了したときに呼び出されます。

### [18.5.4.2.3. ストリーミングプロトコル](https://docs.python.jp/3/library/asyncio-protocol.html#streaming-protocols)

> 以下のコールバックは Protocol インスタンス上で呼び出されます:

属性|概要
----|----
Protocol.data_received(data)|データを受信したときに呼び出されます。data は受信したデータを含む空ではないバイト列オブジェクトになります。
Protocol.eof_received()|相手方が送信するデータがないことを伝えてきたとき (例えば相手方が asyncio を使用しており write_eof() を呼び出した場合) に呼び出されます。

### [18.5.4.2.4. データグラムプロトコル](https://docs.python.jp/3/library/asyncio-protocol.html#datagram-protocols)

> 以下のコールバックは DatagramProtocol インスタンス上で呼び出されます。

属性|概要
----|----
DatagramProtocol.datagram_received(data, addr)|データグラムを受信したときに呼び出されます。data は受信データを含むバイトオブジェクトです。addr はデータを送信するピアのアドレスです; 正確な形式はトランスポートに依存します。
DatagramProtocol.error_received(exc)|直前の送信あるいは受信が OSError を送出したときに呼び出されます。exc は OSError のインスタンスになります。

### [18.5.4.2.5. フロー制御コールバック](https://docs.python.jp/3/library/asyncio-protocol.html#flow-control-callbacks)

> これらコールバックは Protocol、DatagramProtocol および SubprocessProtocol インスタンスから呼び出される場合があります:

属性|概要
----|----
BaseProtocol.pause_writing()|トランスポートのバッファーサイズが最高水位点 (High-Water Mark) を超えたときに呼び出されます。
BaseProtocol.resume_writing()|トランスポートのバッファーサイズが最低水位点 (Low-Water Mark) に達したきに呼び出されます。

### [18.5.4.2.6. コルーチンとプロトコル](https://docs.python.jp/3/library/asyncio-protocol.html#coroutines-and-protocols)

> コルーチンはプロトコルメソッドで ensure_future() を使用してスケジュールされることがありますが、それは実行順を保証するものではありません。プロトコルはプロトコルメソッド内で作成されたコルーチンを検知しないため、それらを待機しません。

> 信頼できる実行順を持つには、コルーチンの yield from で ストリームオブジェクト を使用します。例えば、StreamWriter.drain() コルーチンは書き込みバッファーがフラッシュされるまで待機することができます。

## [18.5.4.3. プロトコルの例](https://docs.python.jp/3/library/asyncio-protocol.html#protocol-examples)

### [18.5.4.3.1. TCP Echo クライアントプロトコル](https://docs.python.jp/3/library/asyncio-protocol.html#tcp-echo-client-protocol)

> AbstractEventLoop.create_connection() メソッドを使用した TCP Echo クライアントで、データを送信しコネクションがクローズされるまで待機します。


```python
import asyncio

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop

    def connection_made(self, transport):
        transport.write(self.message.encode())
        print('Data sent: {!r}'.format(self.message))

    def data_received(self, data):
        print('Data received: {!r}'.format(data.decode()))

    def connection_lost(self, exc):
        print('The server closed the connection')
        print('Stop the event loop')
        self.loop.stop()

loop = asyncio.get_event_loop()
message = 'Hello World!'
coro = loop.create_connection(lambda: EchoClientProtocol(message, loop),
                              '127.0.0.1', 8888)
loop.run_until_complete(coro)
loop.run_forever()
loop.close()
```

> この例ではイベントループを 2 個実行しています。run_until_complete() メソッドはサーバが待ち受け状態にないときに例外を送出するためのもので、通常作成しなければならない例外の送出やループの停止などを行うための短いコルーチンの代用になります。run_until_complete() の終了時、ループの実行は終了しているので、エラー発生時にループを停止する必要はありません。

> 参考

> ストリームを使った TCP Echo クライアント の例では asyncio.open_connection() 関数を使用しています。

### [18.5.4.3.2. TCP Echo サーバープロトコル](https://docs.python.jp/3/library/asyncio-protocol.html#tcp-echo-server-protocol)

> AbstractEventLoop.create_server() メソッドを使用した TCP Echo サーバーで、受信したデータを返信しコネクションをクローズします。

```python
import asyncio

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()

loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
```

> Transport.close() は、データがまだソケットに送信されていなくても、WriteTransport.write() の直後に呼び出されます: それぞれのメソッドは非同期です。これらトランスポートメソッドはコルーチンではないため、yield from は必要ありません。

> 参考

> ストリームを使った TCP Echo サーバー の例では asyncio.start_server() 関数を使用しています。 

### [18.5.4.3.3. UDP Echo クライアントプロトコル](https://docs.python.jp/3/library/asyncio-protocol.html#udp-echo-client-protocol)

> AbstractEventLoop.create_datagram_endpoint() メソッドを使用する UDP Echo クライアントで、データを送信し応答を受信するとトランスポートをクローズします。

```python
import asyncio

class EchoClientProtocol:
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.transport = None

    def connection_made(self, transport):
        self.transport = transport
        print('Send:', self.message)
        self.transport.sendto(self.message.encode())

    def datagram_received(self, data, addr):
        print("Received:", data.decode())

        print("Close the socket")
        self.transport.close()

    def error_received(self, exc):
        print('Error received:', exc)

    def connection_lost(self, exc):
        print("Socket closed, stop the event loop")
        loop = asyncio.get_event_loop()
        loop.stop()

loop = asyncio.get_event_loop()
message = "Hello World!"
connect = loop.create_datagram_endpoint(
    lambda: EchoClientProtocol(message, loop),
    remote_addr=('127.0.0.1', 9999))
transport, protocol = loop.run_until_complete(connect)
loop.run_forever()
transport.close()
loop.close()
```

### [18.5.4.3.4. UDP Echo サーバープロトコル](https://docs.python.jp/3/library/asyncio-protocol.html#udp-echo-server-protocol)

> AbstractEventLoop.create_datagram_endpoint() メソッドを使用しする UDP Echo サーバーで、受信したデータを返送します。

```python
import asyncio

class EchoServerProtocol:
    def connection_made(self, transport):
        self.transport = transport

    def datagram_received(self, data, addr):
        message = data.decode()
        print('Received %r from %s' % (message, addr))
        print('Send %r to %s' % (message, addr))
        self.transport.sendto(data, addr)

loop = asyncio.get_event_loop()
print("Starting UDP server")
# One protocol instance will be created to serve all client requests
listen = loop.create_datagram_endpoint(
    EchoServerProtocol, local_addr=('127.0.0.1', 9999))
transport, protocol = loop.run_until_complete(listen)

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

transport.close()
loop.close()
```

### [18.5.4.3.5. プロトコルを使ってデータを待つオープンソケットの登録](https://docs.python.jp/3/library/asyncio-protocol.html#register-an-open-socket-to-wait-for-data-using-a-protocol)

> プロトコルと AbstractEventLoop.create_connection() メソッドを使用してソケットがデータを受信するまで待機し、受信後イベントループをクローズします。

```python
import asyncio
try:
    from socket import socketpair
except ImportError:
    from asyncio.windows_utils import socketpair

# Create a pair of connected sockets
rsock, wsock = socketpair()
loop = asyncio.get_event_loop()

class MyProtocol(asyncio.Protocol):
    transport = None

    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        print("Received:", data.decode())

        # We are done: close the transport (it will call connection_lost())
        self.transport.close()

    def connection_lost(self, exc):
        # The socket has been closed, stop the event loop
        loop.stop()

# Register the socket to wait for data
connect_coro = loop.create_connection(MyProtocol, sock=rsock)
transport, protocol = loop.run_until_complete(connect_coro)

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

> 読み込みイベント用のファイル記述子の監視 の例では、ソケットのファイル記述子を登録するのに低水準の AbstractEventLoop.add_reader() メソッドを使用しています。

> ストリームを使ってデータを待つオープンソケットの登録 の例ではコルーチンの open_connection() 関数によって作成された高水準ストリームを使用しています。

