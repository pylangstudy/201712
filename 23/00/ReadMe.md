# [18.5.5. ストリーム (コルーチンベースの API)](https://docs.python.jp/3/library/asyncio-stream.html)

< [18.5. asyncio — 非同期 I/O、イベントループ、コルーチンおよびタスク](https://docs.python.jp/3/library/asyncio.html) < [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

* Source code: [Lib/asyncio/streams.py](https://github.com/python/cpython/tree/3.6/Lib/asyncio/streams.py)

## [18.5.5.1. ストリーム関数](https://docs.python.jp/3/library/asyncio-stream.html#stream-functions)

> 注釈

> このモジュール内のトップレベル関数は、便利なラッパーとしてのみ意図されています。特別なことは何もありませんし、それらが思い通りに動作しない場合は、ご自由にコードをコピーしてください。

属性|概要
----|----
coroutine asyncio.open_connection(host=None, port=None, *, loop=None, limit=None, **kwds)|create_connection() のラッパーで (reader, writer) ペアを返します。
coroutine asyncio.open_unix_connection(path=None, *, loop=None, limit=None, **kwds)|create_unix_connection() のラッパーで (reader, writer) ペアを返します。

## [18.5.5.2. StreamReader](https://docs.python.jp/3/library/asyncio-stream.html#streamreader)

属性|概要
----|----
class asyncio.StreamReader(limit=None, loop=None)|このクラスは スレッド安全ではありません。
exception()|例外を取得します。
feed_eof()|EOF の肯定応答を行います。
feed_data(data)|バイト列 data を内部バッファーに取り込みます。データを待っているあらゆる処理が再開されます。
set_exception(exc)|例外を設定します。
set_transport(transport)|トランスポートを設定します。
coroutine read(n=-1)|n バイト読み込みます。n が指定されないか -1 が指定されていた場合 EOF になるまで読み込み、全データを返します。
coroutine readline()|1 行読み込みます。 "行" とは、\n で終了するバイト列のシーケンスです。
coroutine readexactly(n)|厳密に n バイト読み込みます。n バイト読み込む前にストリームの終端に達したとき、IncompleteReadError を送出します。例外の IncompleteReadError.partial 属性に、読み込んだ分の不完全なバイト列が格納されます。
coroutine readuntil(separator=b'\n')|separator が見つかるまでストリームからデータを読み込みます。
at_eof()|バッファーが空で feed_eof() が呼ばれていた場合 True を返します。

## [18.5.5.3. StreamWriter](https://docs.python.jp/3/library/asyncio-stream.html#streamwriter)

属性|概要
----|----
class asyncio.StreamWriter(transport, protocol, reader, loop)|トランスポートをラップします。
transport|トランスポートです。
can_write_eof()|トランスポートが write_eof() をサポートしている場合は True を、していない場合は False を返します。WriteTransport.can_write_eof() を参照してください。
close()|トランスポートを閉じます: BaseTransport.close() を参照してください。
coroutine drain()|下層のトランスポートの書き込みバッファーがフラッシュされる機会を与えます。
get_extra_info(name, default=None)|オプションのトランスポート情報を返します: BaseTransport.get_extra_info() を参照してください。
write(data)|トランスポートにバイト列 data を書き込みます: WriteTransport.write() を参照してください。
writelines(data)|バイト列のデータのリスト (またはリテラブル) をトランスポートに書き込みます: WriteTransport.writelines() を参照してください。
write_eof()|バッファーされたデータをフラッシュした後送信側のトランスポートをクローズします: WriteTransport.write_eof() を参照してください。

## [18.5.5.4. StreamReaderProtocol](https://docs.python.jp/3/library/asyncio-stream.html#streamreaderprotocol)

属性|概要
----|----
class asyncio.StreamReaderProtocol(stream_reader, client_connected_cb=None, loop=None)|Protocol と StreamReader を適合させる些末なヘルパークラスです。Protocol のサブクラスです。

## [18.5.5.5. IncompleteReadError](https://docs.python.jp/3/library/asyncio-stream.html#incompletereaderror)

属性|概要
----|----
exception asyncio.IncompleteReadError|不完全な読み込みエラーです。EOFError のサブクラスです。
expected|想定されていたバイト数 (int) です。
partial|ストリームの終端に達する前に読み込んだバイト文字列 (bytes) です。

## [18.5.5.6. LimitOverrunError](https://docs.python.jp/3/library/asyncio-stream.html#limitoverrunerror)

属性|概要
----|----
exception asyncio.LimitOverrunError|区切り文字を探している間にバッファリミットに到達しました。
consumed|未消費のバイトの合計数。

## [18.5.5.7. ストリームの例](https://docs.python.jp/3/library/asyncio-stream.html#stream-examples)

### [18.5.5.7.1. ストリームを使った TCP Echo クライアント](https://docs.python.jp/3/library/asyncio-stream.html#tcp-echo-client-using-streams)

> asyncio.open_connection() 関数を使った TCP Echo クライアントです:

```python
import asyncio

@asyncio.coroutine
def tcp_echo_client(message, loop):
    reader, writer = yield from asyncio.open_connection('127.0.0.1', 8888,
                                                        loop=loop)

    print('Send: %r' % message)
    writer.write(message.encode())

    data = yield from reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()

message = 'Hello World!'
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()
```

> 参考

> AbstractEventLoop.create_connection() メソッドを使った TCP Echo クライアントプロトコル の例

### [18.5.5.7.2. ストリームを使った TCP Echo サーバー](https://docs.python.jp/3/library/asyncio-stream.html#tcp-echo-server-using-streams)

> asyncio.start_server() 関数を使った TCP Echo サーバーです:

```python
import asyncio

@asyncio.coroutine
def handle_echo(reader, writer):
    data = yield from reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))

    print("Send: %r" % message)
    writer.write(data)
    yield from writer.drain()

    print("Close the client socket")
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
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

> 参考

> AbstractEventLoop.create_server() メソッドを使った TCP Echo サーバープロトコル の例

### [18.5.5.7.3. HTTP ヘッダーの取得](https://docs.python.jp/3/library/asyncio-stream.html#get-http-headers)

> コマンドラインから渡された URL の HTTP ヘッダーを問い合わせる簡単な例です:

```python
import asyncio
import urllib.parse
import sys

@asyncio.coroutine
def print_http_headers(url):
    url = urllib.parse.urlsplit(url)
    if url.scheme == 'https':
        connect = asyncio.open_connection(url.hostname, 443, ssl=True)
    else:
        connect = asyncio.open_connection(url.hostname, 80)
    reader, writer = yield from connect
    query = ('HEAD {path} HTTP/1.0\r\n'
             'Host: {hostname}\r\n'
             '\r\n').format(path=url.path or '/', hostname=url.hostname)
    writer.write(query.encode('latin-1'))
    while True:
        line = yield from reader.readline()
        if not line:
            break
        line = line.decode('latin1').rstrip()
        if line:
            print('HTTP header> %s' % line)

    # Ignore the body, close the socket
    writer.close()

url = sys.argv[1]
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(print_http_headers(url))
loop.run_until_complete(task)
loop.close()
```

> 使い方:

> python example.py http://example.com/path/page.html

> または HTTPS を使用:

> python example.py https://example.com/path/page.html

### [18.5.5.7.4. ストリームを使ってデータを待つオープンソケットの登録](https://docs.python.jp/3/library/asyncio-stream.html#register-an-open-socket-to-wait-for-data-using-streams)

> open_connection() 関数を使ってソケットがデータを受信するまで待つコルーチンです:

```python
import asyncio
try:
    from socket import socketpair
except ImportError:
    from asyncio.windows_utils import socketpair

@asyncio.coroutine
def wait_for_data(loop):
    # Create a pair of connected sockets
    rsock, wsock = socketpair()

    # Register the open socket to wait for data
    reader, writer = yield from asyncio.open_connection(sock=rsock, loop=loop)

    # Simulate the reception of data from the network
    loop.call_soon(wsock.send, 'abc'.encode())

    # Wait for data
    data = yield from reader.read(100)

    # Got data, we are done: close the socket
    print("Received:", data.decode())
    writer.close()

    # Close the second socket
    wsock.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(wait_for_data(loop))
loop.close()
```

> 参考

> プロトコルを使ってデータを待つオープンソケットの登録 の例では AbstractEventLoop.create_connection() メソッドによって作成された低レベルプロトコルを使用しています。

> 読み込みイベント用のファイル記述子の監視 の例では、ソケットのファイル記述子を登録するのに低水準の AbstractEventLoop.add_reader() メソッドを使用しています。

