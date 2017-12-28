# [## [18.7. asynchat — 非同期ソケットコマンド/レスポンスハンドラ](https://docs.python.jp/3/library/asynchat.html)

< [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

ソースコード: [Lib/asynchat.py](https://github.com/python/cpython/tree/3.6/Lib/asynchat.py)

> バージョン 3.6 で撤廃: 代わりに asyncio を使ってください。

> 注釈

> このモジュールは後方互換性のためだけに存在します。新しいコードでは asyncio を利用することを推奨します。 

> asynchat を使うと、 asyncore を基盤とした非同期なサーバ・クライアントをより簡単に開発する事ができます。 asynchat では、プロトコルの要素が任意の文字列で終了するか、または可変長の文字列であるようなプロトコルを容易に制御できるようになっています。 asynchat は、抽象クラス async_chat を定義しており、 async_chat を継承して collect_incoming_data() メソッドと found_terminator() メソッドを実装すれば使うことができます。 async_chat と asyncore は同じ非同期ループを使用しており、 asyncore.dispatcher も asynchat.async_chat も同じチャネルマップに登録する事ができます。通常、 asyncore.dispatcher はサーバチャネルとして使用し、リクエストの受け付け時に asynchat.async_chat オブジェクトを生成します。

属性|概要
----|----
class asynchat.async_chat|このクラスは、 asyncore.dispatcher から継承した抽象クラスです。使用する際には async_chat のサブクラスを作成し、 collect_incoming_data() と found_terminator() を定義しなければなりません。 asyncore.dispatcher のメソッドを使用する事もできますが、メッセージ/レスポンス処理を中心に行う場合には使えないメソッドもあります。
ac_in_buffer_size|非同期入力バッファサイズ (デフォルト値: 4096)。
ac_out_buffer_size|非同期出力バッファサイズ (デフォルト値: 4096)。
async_chat.close_when_done()|Pushes a None on to the producer queue. When this producer is popped off the queue it causes the channel to be closed.
async_chat.collect_incoming_data(data)|チャネルが受信した不定長のデータを data に指定して呼び出されます。このメソッドは必ずオーバライドする必要があり、デフォルトの実装では、 NotImplementedError 例外を送出します。
async_chat.discard_buffers()|In emergencies this method will discard any data held in the input and/or output buffers and the producer queue.
async_chat.found_terminator()|入力データストリームが、 set_terminator() で指定した終了条件と一致した場合に呼び出されます。このメソッドは必ずオーバライドする必要があり、デフォルトの実装では、 NotImplementedError 例外を送出します。入力データを参照する必要がある場合でも引数としては与えられないため、入力バッファをインスタンス属性として参照しなければなりません。
async_chat.get_terminator()|現在のチャネルの終了条件を返します。
async_chat.push(data)|Pushes data on to the channel’s queue to ensure its transmission. This is all you need to do to have the channel write the data out to the network, although it is possible to use your own producers in more complex schemes to implement encryption and chunking, for example.
async_chat.push_with_producer(producer)|Takes a producer object and adds it to the producer queue associated with the channel. When all currently-pushed producers have been exhausted the channel will consume this producer’s data by calling its more() method and send the data to the remote endpoint.
async_chat.set_terminator(term)|チャネルで検出する終了条件を設定します。term は入力プロトコルデータの処理方式によって以下の3つの型の何れかを指定します。

## [18.7.1. asynchat 使用例]()

> 以下のサンプルは、 async_chat でHTTPリクエストを読み込む処理の一部です。Webサーバは、クライアントからの接続毎に http_request_handler オブジェクトを作成します。最初はチャネルの終了条件に空行を指定してHTTPヘッダの末尾までを検出し、その後ヘッダ読み込み済みを示すフラグを立てています。

> ヘッダ読み込んだ後、リクエストの種類がPOSTであればデータが入力ストリームに流れるため、Content-Length: ヘッダの値を数値として終了条件に指定し、適切な長さのデータをチャネルから読み込みます。

> 必要な入力データを全て入手したら、チャネルの終了条件に None を指定して残りのデータを無視するようにしています。この後、 handle_request() が呼び出されます。

```python
import asynchat

class http_request_handler(asynchat.async_chat):

    def __init__(self, sock, addr, sessions, log):
        asynchat.async_chat.__init__(self, sock=sock)
        self.addr = addr
        self.sessions = sessions
        self.ibuffer = []
        self.obuffer = b""
        self.set_terminator(b"\r\n\r\n")
        self.reading_headers = True
        self.handling = False
        self.cgi_data = None
        self.log = log

    def collect_incoming_data(self, data):
        """Buffer the data"""
        self.ibuffer.append(data)

    def found_terminator(self):
        if self.reading_headers:
            self.reading_headers = False
            self.parse_headers(b"".join(self.ibuffer))
            self.ibuffer = []
            if self.op.upper() == b"POST":
                clen = self.headers.getheader("content-length")
                self.set_terminator(int(clen))
            else:
                self.handling = True
                self.set_terminator(None)
                self.handle_request()
        elif not self.handling:
            self.set_terminator(None)  # browsers sometimes over-send
            self.cgi_data = parse(self.headers, b"".join(self.ibuffer))
            self.handling = True
            self.ibuffer = []
            self.handle_request()
```

