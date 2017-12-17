# [18.4. selectors — 高水準の I/O 多重化](https://docs.python.jp/3/library/selectors.html)

< [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

> バージョン 3.4 で追加.

ソースコード: [Lib/selectors.py](https://github.com/python/cpython/tree/3.6/Lib/selectors.py)

## [18.4.1. はじめに](https://docs.python.jp/3/library/selectors.html#introduction)

> このモジュールにより、select モジュールプリミティブに基づく高水準かつ効率的な I/O の多重化が行えます。OS 水準のプリミティブを使用した正確な制御を求めない限り、このモジュールの使用が推奨されます。

> このモジュールは BaseSelector 抽象基底クラスと、いくつかの具象実装 (KqueueSelector, EpollSelector…) を定義しており、これらは複数のファイルオブジェクトの I/O の準備状況の通知の待機に使用できます。以下では、 "ファイルオブジェクト" は、fileno() メソッドを持つあらゆるオブジェクトか、あるいは Raw ファイル記述子を意味します。ファイルオブジェクト を参照してください。

> DefaultSelector は、現在のプラットフォームで利用できる、もっとも効率的な実装の別名になります: これはほとんどのユーザーにとってのデフォルトの選択になるはずです。

### 注釈

> プラットフォームごとにサポートされているファイルオブジェクトのタイプは異なります: Windows ではソケットはサポートされますが、パイプはされません。Unix では両方がサポートされます (その他の fifo やスペシャルファイルデバイスなどのタイプもサポートされます)。

### 参考

Module|概要
------|----
select|低水準の I/O 多重化モジュールです。

## [18.4.2. クラス](https://docs.python.jp/3/library/selectors.html#classes)

> クラス階層:

```
BaseSelector
+-- SelectSelector
+-- PollSelector
+-- EpollSelector
+-- DevpollSelector
+-- KqueueSelector
```

> 以下では、events は与えられたファイルオブジェクトを待機すべき I/O イベントを示すビット単位のマスクになります。これには以下のモジュール定数の組み合わせを設定できます:

    定数 	意味
    EVENT_READ 	読み込み可能
    EVENT_WRITE 	書き込み可能

属性|概要
----|----
class selectors.SelectorKey|A SelectorKey is a namedtuple used to associate a file object to its underlying file descriptor, selected event mask and attached data. It is returned by several BaseSelector methods.
fileobj|登録されたファイルオブジェクトです。
fd|下層のファイル記述子です。
events|このファイルオブジェクトで待機しなければならないイベントです。
data|このファイルオブジェクトに関連付けられたオプションの不透明型 (Opaque) データです。例えば、これはクライアントごとのセッション ID を格納するために使用できます。

属性|概要
----|----
class selectors.BaseSelector|BaseSelector は複数のファイルオブジェクトの I/O イベントの準備状況の待機に使用されます。これはファイルストリームを登録、登録解除、およびこれらのストリームでの I/O イベントを待機 (オプションでタイムアウト) するメソッドをサポートします。これは抽象基底クラスであるため、インスタンスを作成できません。使用する実装を明示的に指定したい、そしてプラットフォームがそれをサポートしている場合は、代わりに DefaultSelector を使用するか、SelectSelector や KqueueSelector などの一つを使用します。BaseSelector とその具象実装は コンテキストマネージャー プロトコルをサポートしています。

属性|概要
----|----
abstractmethod register(fileobj, events, data=None)|I/O イベントを監視するファイルオブジェクトをセレクションに登録します。

属性|概要
----|----
abstractmethod unregister(fileobj)|ファイルオブジェクトのセレクション登録を解除し、監視対象から外します。ファイルオブジェクトの登録解除はそのクローズより前に行われます。
modify(fileobj, events, data=None)|登録されたファイルオブジェクトの監視されたイベントや付属データを変更します。

属性|概要
----|----
abstractmethod select(timeout=None)|登録されたいくつかのファイルオブジェクトが準備できたか、タイムアウトするまで待機します。
close()|セレクタを閉じます。
get_key(fileobj)|登録されたファイルオブジェクトに関連付けられたキーを返します。

属性|概要
----|----
abstractmethod get_map()|ファイルオブジェクトからセレクタキーへのマッピングを返します。
class selectors.DefaultSelector|デフォルトの selector クラスで、現在のプラットフォームで利用できる最も効率的な実装を使用しています。大半のユーザはこれをデフォルトにすべきです。

属性|概要
----|----
class selectors.SelectSelector|select.select() を基底とするセレクタです。
class selectors.PollSelector|select.poll() を基底とするセレクタです。
class selectors.EpollSelector|select.epoll() を基底とするセレクタです。
fileno()|下層の select.epoll() オブジェクトが使用しているファイル記述子を返します。

属性|概要
----|----
class selectors.DevpollSelector|select.devpoll() を基底とするセレクタです。
fileno()|下層の select.devpoll() オブジェクトが使用しているファイル記述子を返します。

属性|概要
----|----
class selectors.KqueueSelector|select.kqueue() を基底とするセレクタです。
fileno()|下層の select.kqueue() オブジェクトが使用しているファイル記述子を返します。

## [18.4.3. 使用例](https://docs.python.jp/3/library/selectors.html#examples)

> 簡単なエコーサーバの実装です:

```python
import selectors
import socket

sel = selectors.DefaultSelector()

def accept(sock, mask):
    conn, addr = sock.accept()  # Should be ready
    print('accepted', conn, 'from', addr)
    conn.setblocking(False)
    sel.register(conn, selectors.EVENT_READ, read)

def read(conn, mask):
    data = conn.recv(1000)  # Should be ready
    if data:
        print('echoing', repr(data), 'to', conn)
        conn.send(data)  # Hope it won't block
    else:
        print('closing', conn)
        sel.unregister(conn)
        conn.close()

sock = socket.socket()
sock.bind(('localhost', 1234))
sock.listen(100)
sock.setblocking(False)
sel.register(sock, selectors.EVENT_READ, accept)

while True:
    events = sel.select()
    for key, mask in events:
        callback = key.data
        callback(key.fileobj, mask)
```

