# [18.6. asyncore — 非同期ソケットハンドラ](https://docs.python.jp/3/library/asyncore.html)

< [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)


* ソースコード: [Lib/asyncore.py](https://github.com/python/cpython/tree/3.6/Lib/asyncore.py)

> バージョン 3.6 で撤廃: 代わりに asyncio を使ってください。

> 注釈

> このモジュールは後方互換性のためだけに存在します。新しいコードでは asyncio を利用することを推奨します。

> このモジュールは、非同期ソケットサービスのクライアント・サーバを開発するための基盤として使われます。

> CPUが一つしかない場合、プログラムが"二つのことを同時に"実行する方法は二つしかありません。もっとも簡単で一般的なのはマルチスレッドを利用する方法ですが、これとはまったく異なるテクニックで、一つのスレッドだけでマルチスレッドと同じような効果を得られるテクニックがあります。このテクニックはI/O処理が中心である場合にのみ有効で、CPU負荷の高いプログラムでは効果が無く、この場合にはプリエンプティブなスケジューリングが可能なスレッドが有効でしょう。しかし、多くの場合、ネットワークサーバではCPU負荷よりはIO負荷が問題となります。

> もしOSのI/Oライブラリがシステムコール select() をサポートしている場合（ほとんどの場合はサポートされている）、I/O処理は"バックグラウンド"で実行し、その間に他の処理を実行すれば、複数の通信チャネルを同時にこなすことができます。一見、この戦略は奇妙で複雑に思えるかもしれませんが、いろいろな面でマルチスレッドよりも理解しやすく、制御も容易です。 asyncore は多くの複雑な問題を解決済みなので、洗練され、パフォーマンスにも優れたネットワークサーバとクライアントを簡単に開発することができます。とくに、 asynchat のような、対話型のアプリケーションやプロトコルには非常に有効でしょう。

> 基本的には、この二つのモジュールを使う場合は一つ以上のネットワーク チャネル を asyncore.dispatcher クラス、または asynchat.async_chat のインスタンスとして作成します。作成されたチャネルはグローバルマップに登録され、 loop() 関数で参照されます。 loop() には、専用の マップ を渡す事も可能です。

> チャネルを生成後、 loop() を呼び出すとチャネル処理が開始し、最後のチャネル（非同期処理中にマップに追加されたチャネルを含む）が閉じるまで継続します。

属性|概要
----|----
asyncore.loop([timeout[, use_poll[, map[, count]]]])|ポーリングループを開始し、count 回が過ぎるか、全てのオープン済みチャネルがクローズされた場合のみ終了します。全ての引数はオプションです。引数 count のデフォルト値は None で、ループは全てのチャネルがクローズされた場合のみ終了します。引数 timeout は select() または poll() の引数 timeout として渡され、秒単位で指定します。デフォルト値は 30 秒です。引数 use_poll が真の場合、 select() ではなく poll() が使われます (デフォルト値は False です)。
class asyncore.dispatcher|dispatcher クラスは、低レベルソケットオブジェクトの薄いラッパーです。便宜上、非同期ループから呼び出されるイベント処理メソッドを追加していますが、これ以外の点では、non-blockingなソケットと同様です。
handle_read()|非同期ループで、チャネルのソケットの read() メソッドの呼び出しが成功した時に呼び出されます。
handle_write()|非同期ループで、書き込み可能ソケットが実際に書き込み可能になった時に呼び出されます。このメソッドでは、しばしばパフォーマンスの向上のために必要なバッファリングを実装します。例:
handle_expt()|out of band (OOB)データが検出された時に呼び出されます。OOBはあまりサポートされておらず、また滅多に使われないので、handle_expt() が呼び出されることはほとんどありません。
handle_connect()|ソケットの接続が確立した時に呼び出されます。"welcome"バナーの送信、プロトコルネゴシエーションの初期化などを行います。
handle_close()|ソケットが閉じた時に呼び出されます。
handle_error()|捕捉されない例外が発生した時に呼び出されます。デフォルトでは、短縮したトレースバック情報が出力されます。
handle_accept()|listen 中のチャネル (受動的にオープンしたもの) がリモートホストからの connect() で接続され、接続が確立した時に呼び出されます。 バージョン 3.2 で非推奨になりました; 代わりに handle_accepted() を使ってください。
handle_accepted(sock, addr)|listen 中のチャネル (受動的にオープンしたもの) がリモートホストからの connect() で接続され、接続が確立した時に呼び出されます。 sock はその接続でデータを送受信するのに使える 新しい ソケットオブジェクトで、 addr は接続の対向のソケットに bind されているアドレスです。
readable()|非同期ループ中に呼び出され、readイベントの監視リストに加えるか否かを決定します。デフォルトのメソッドでは True を返し、readイベントの発生を監視します。
writable()|非同期ループ中に呼び出され、writeイベントの監視リストに加えるか否かを決定します。デフォルトのメソッドでは True を返し、writeイベントの発生を監視します。
create_socket(family=socket.AF_INET, type=socket.SOCK_STREAM)|引数も含め、通常のソケット生成と同一です。ソケットの生成については、 socket モジュールのドキュメントを参照してください。
connect(address)|通常のソケットオブジェクトと同様、address には一番目の値が接続先ホスト、2番目の値がポート番号であるタプルを指定します。
send(data)|リモート側の端点に data を送出します。
recv(buffer_size)|リモート側の端点より、最大 buffer_size バイトのデータを読み込みます。長さ0のバイト列オブジェクトが返ってきた場合、チャネルはリモートから切断された事を示します。
listen(backlog)|ソケットへの接続を待ちます。引数 backlog は、キューに追加できるコネクションの最大数 (1 以上) を指定します。最大値はシステムに依存します（通常は5)。
bind(address)|ソケットを address にバインドします。ソケットはバインド済みであってはなりません。 (address の形式は、アドレスファミリに依存します。 socket モジュールを参照のこと。) ソケットを再利用可能にする (SO_REUSEADDR オプションを設定する) には、 dispatcher オブジェクトの set_reuse_addr() メソッドを呼び出してください。
accept()|接続を受け入れます。ソケットはアドレスにバインド済みであり、listen() で接続待ち状態でなければなりません。戻り値は None か (conn, address) のペアで、conn はデータの送受信を行う 新しい ソケットオブジェクト、address は接続先ソケットがバインドされているアドレスです。None が返された場合、接続が起こらなかったことを意味します。その場合、サーバーはこのイベントを無視して後続の接続を待ち続けるべきです。
close()|ソケットをクローズします。以降の全ての操作は失敗します。リモート端点では、キューに溜まったデータ以外、これ以降のデータ受信は行えません。ソケットはガベージコレクト時に自動的にクローズされます。
class asyncore.dispatcher_with_send|dispatcher のサブクラスで、シンプルなバッファされた出力機能を持ちます。シンプルなクライアントプログラムに適しています。もっと高レベルな場合には asynchat.async_chat を利用してください。
class asyncore.file_dispatcher|file_dispatcher はファイルデスクリプタか ファイルオブジェクト とオプションとして map を引数にとって、 poll() か loop() 関数で利用できるようにラップします。与えられたファイルオブジェクトなどが fileno() メソッドを持っているとき、そのメソッドが呼び出されて戻り値が file_wrapper のコンストラクタに渡されます。利用できるプラットフォーム: UNIX。
class asyncore.file_wrapper|file_wrapper は整数のファイルデスクリプタを受け取って os.dup() を呼び出してハンドルを複製するので、元のハンドルは file_wrapper と独立してclose されます。このクラスは file_dispatcher クラスが使うために必要なソケットをエミュレートするメソッドを実装しています。利用できるプラットフォーム: UNIX。

## [18.6.1. asyncoreの例: 簡単なHTTPクライアント]()

> 基本的なサンプルとして、以下に非常に単純なHTTPクライアントを示します。このHTTPクライアントは dispatcher クラスでソケットを利用しています:

```python
import asyncore

class HTTPClient(asyncore.dispatcher):

    def __init__(self, host, path):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.connect( (host, 80) )
        self.buffer = bytes('GET %s HTTP/1.0\r\nHost: %s\r\n\r\n' %
                            (path, host), 'ascii')

    def handle_connect(self):
        pass

    def handle_close(self):
        self.close()

    def handle_read(self):
        print(self.recv(8192))

    def writable(self):
        return (len(self.buffer) > 0)

    def handle_write(self):
        sent = self.send(self.buffer)
        self.buffer = self.buffer[sent:]


client = HTTPClient('www.python.org', '/')
asyncore.loop()
```

## [18.6.2. 基本的な echo サーバーの例]()

> この例の基本的な echoサーバーは、 dispatcher を利用して接続を受けつけ、接続をハンドラーにディスパッチします:

```python
import asyncore

class EchoHandler(asyncore.dispatcher_with_send):

    def handle_read(self):
        data = self.recv(8192)
        if data:
            self.send(data)

class EchoServer(asyncore.dispatcher):

    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)

    def handle_accepted(self, sock, addr):
        print('Incoming connection from %s' % repr(addr))
        handler = EchoHandler(sock)

server = EchoServer('localhost', 8080)
asyncore.loop()
```

