# [18.5.2. イベントループ](https://docs.python.jp/3/library/asyncio-eventloops.html#event-loops)

< [18.5. asyncio — 非同期 I/O、イベントループ、コルーチンおよびタスク](https://docs.python.jp/3/library/asyncio.html) < [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

## [18.5.2.1. イベントループ関数](https://docs.python.jp/3/library/asyncio-eventloops.html#event-loop-functions)

> 以下の関数は、グローバルポリシーのメソッドにアクセスするための便利なショートカットです。これらはデフォルトポリシーへのアクセス手段を提供するものであり、プロセスの実行前に set_event_loop_policy() を呼び出して設定された代替ポリシーには適用できないことに注意してください。

属性|概要
----|----
asyncio.get_event_loop()|get_event_loop_policy().get_event_loop() の呼び出しと等価です。
asyncio.set_event_loop(loop)|get_event_loop_policy().set_event_loop(loop) の呼び出しと等価です。
asyncio.new_event_loop()|get_event_loop_policy().new_event_loop() の呼び出しと等価です。

## [18.5.2.2. 利用可能なイベントループ](https://docs.python.jp/3/library/asyncio-eventloops.html#available-event-loops)

> asyncio は現在 2 種類の実装のイベントループ、SelectorEventLoop と ProactorEventLoop を提供しています。

属性|概要
----|----
class asyncio.SelectorEventLoop|selectors モジュールベースのイベントループで、AbstractEventLoop のサブクラスです。プラットフォームで利用できる最も効率的なセレクターを使用します。Windows ではソケットのみサポートされています (例えばパイプは未サポート): MSDN の select のドキュメント を参照してください。
class asyncio.ProactorEventLoop|"I/O Completion Ports" (IOCP) を使用した Windows 用のプロアクターイベントループで、AbstractEventLoop のサブクラスです。利用できる環境 : Windows. 参考 [MSDN の I/O Completion Ports のドキュメント](https://msdn.microsoft.com/en-us/library/windows/desktop/aa365198%28v=vs.85%29.aspx)。

> Windows で ProactorEventLoop を使用した例:

```python
import asyncio, sys

if sys.platform == 'win32':
    loop = asyncio.ProactorEventLoop()
    asyncio.set_event_loop(loop)
```

## [18.5.2.3. プラットフォームでのサポート](https://docs.python.jp/3/library/asyncio-eventloops.html#platform-support)

> asyncio モジュールは移植性を考慮して設計されていますが、プラットフォームごとにわずかな違いがあり、asyncio の全機能をサポートしているわけではありません。

### [18.5.2.3.1. Windows](https://docs.python.jp/3/library/asyncio-eventloops.html#windows)

> Windows のイベントループでの共通の制限:

* create_unix_connection() および create_unix_server() はサポートされていません: ソケットファミリー socket.AF_UNIX は UNIX 固有です
* add_signal_handler() と remove_signal_handler() はサポートされていません
* EventLoopPolicy.set_child_watcher() は未サポート: ProactorEventLoop はサブプロセスをサポートします。これは子プロセスを監視できる唯一の実装で、構成設定を必要としません。

> SelectorEventLoop 固有の制限:

* SelectSelector が使用されるがサポートしているのはソケットのみで 512 ソケットに制限される
* add_reader() および add_writer() はソケットのファイル記述子受け取るだけです
* パイプは未サポート (例: connect_read_pipe(), connect_write_pipe())
* サブプロセス は未サポート (例: subprocess_exec(), subprocess_shell())

> ProactorEventLoop 固有の制限:

* create_datagram_endpoint() (UDP) は未サポート
* add_reader() および add_writer() は未サポート

> Windows のモノトニック時計の時間分解能は、通常約 15.6 秒です。 最高分解能は 0.5 秒です。 分解能はハードウェア (HPET の可否) および Windows の設定に依存します。 asyncio 遅延呼び出し を参照してください。

バージョン 3.5 で変更: ProactorEventLoop は SSL をサポートしました。

## [18.5.2.3.2. Mac OS X](https://docs.python.jp/3/library/asyncio-eventloops.html#mac-os-x)

> PTY のようなキャラクターデバイスは Mavericks (Mac OS 10.9) 以降でのみ十分サポートされています。Mac OS 10.5 以前ではサポートされていません。

> Mac OS 10.6、10.7 および 10.8 では、デフォルトのイベントループは SelectorEventLoop で、selectors.KqueueSelector を使用します。selectors.KqueueSelector はこれらのバージョンではキャラクターデバイスをサポートしていません。これらのバージョンでキャラクターデバイスをサポートするには SelectorEventLoop で SelectSelector または PollSelector を使用します。例:

```python
import asyncio
import selectors

selector = selectors.SelectSelector()
loop = asyncio.SelectorEventLoop(selector)
asyncio.set_event_loop(loop)
```

## [18.5.2.4. イベントループのポリシーとデフォルトポリシー](https://docs.python.jp/3/library/asyncio-eventloops.html#event-loop-policies-and-the-default-policy)

> イベントループの管理は、カスタムプラットフォームやフレームワークのために最大限の柔軟性を提供するため ポリシー パターンによって抽象化されます。プロセスの実行中、単一のポリシーオブジェクトが、コンテキスト呼び出しベースのプロセスから利用可能なイベントループを管理します。一つのポリシーは一つの AbstractEventLoopPolicy インターフェースを実装するオブジェクトです。

> ほとんどの asyncio 利用者にとってデフォルトのグローバルポリシーで十分であるため、ポリシーを明示的に追加する必要はありません。

> デフォルトポリシーは現在のスレッドをコンテキストとして定義し、asyncio と情報のやり取りを行うスレッドごとにイベントループを管理します。モジュールレベル関数 get_event_loop() および set_event_loop() は、デフォルトポリシーによって管理されるイベントループへの便利なアクセス手段を提供します。

## [18.5.2.5. イベントループポリシーインターフェース](https://docs.python.jp/3/library/asyncio-eventloops.html#event-loop-policy-interface)

> イベントループのポリシーは以下のインターフェースを実装しなければなりません:

属性|概要
----|----
class asyncio.AbstractEventLoopPolicy|イベントループポリシーです。
get_event_loop()|現在のコンテクストのイベントループを取得します。
set_event_loop(loop)|現在のコンテキストにイベントループ loop を設定します。
new_event_loop()|このポリシーのルールに従った新しいイベントループを作成して返します。

## [18.5.2.6. グローバルループポリシーへのアクセス](https://docs.python.jp/3/library/asyncio-eventloops.html#access-to-the-global-loop-policy)

属性|概要
----|----
asyncio.get_event_loop_policy()|現在のイベントループポリシーを取得します。
asyncio.set_event_loop_policy(policy)|現在のイベントループポリシーを設定します。policy が None の場合、デフォルトポリシーが復元されます。

