# [17.1. threading — スレッドベースの並列処理](https://docs.python.jp/3/library/threading.html)

< [17. 並行実行](https://docs.python.jp/3/library/concurrency.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

ソースコード: [Lib/threading.py](https://github.com/python/cpython/tree/3.6/Lib/threading.py)

> このモジュールでは、高水準のスレッドインタフェースをより低水準 な _thread モジュールの上に構築しています。 queue モジュールのドキュメントも参照してください。

> また、 _thread がないために threading を使えないような状況向けに dummy_threading を提供しています。

> 注釈

> ここには載っていませんが、Python 2.x シリーズでこのモジュールの一部のメソッドや関数に使われていた camelCase 名は、まだこのモジュールでサポートされます。

> このモジュールは以下の関数を定義しています:

属性|概要
----|----
threading.active_count()|生存中の Thread オブジェクトの数を返します。この数は enumerate() の返すリストの長さと同じです。
threading.current_thread()|関数を呼び出している処理のスレッドに対応する Thread オブジェクトを返します。関数を呼び出している処理のスレッドが threading モジュールで生成したものでない場合、限定的な機能しかもたないダミースレッドオブジェクトを返します。
threading.get_ident()|現在のスレッドの 'スレッドID' を返します。非ゼロの整数です。この値は直接の意味を持っていません; 例えばスレッド特有のデータの辞書に索引をつけるためのような、マジッククッキーとして意図されています。スレッドが終了し、他のスレッドが作られたとき、スレッド ID は再利用されるかもしれません。
threading.enumerate()|現在、生存中の Thread オブジェクト全てのリストを返します。リストには、デーモンスレッド (daemonic thread)、 current_thread() の生成するダミースレッドオブジェクト、そして主スレッドが入ります。終了したスレッドとまだ開始していないスレッドは入りません。
threading.main_thread()|main Thread オブジェクトを返します。通常の条件では、メインスレッドはPythonインタプリタが起動したスレッドを指します。
threading.settrace(func)|threading モジュールを使って開始した全てのスレッドにトレース関数を設定します。 func は各スレッドの run() を呼び出す前にスレッドの sys.settrace() に渡されます。
threading.setprofile(func)|threading モジュールを使って開始した全てのスレッドにプロファイル関数を設定します。 func は各スレッドの run() を呼び出す前にスレッドの sys.setprofile() に渡されます。
threading.stack_size([size])|新しいスレッドを作るときのスレッドスタックサイズを返します。オプションの size 引数にはこれ以降に作成するスレッドのスタックサイズを指定し、0 (プラットフォームのデフォルト値または設定されたデフォルト値) か、 32,768 (32 KiB) 以上の正の整数でなければなりません。size が指定されない場合 0 が使われます。スレッドのスタックサイズの変更がサポートされていない場合、 RuntimeError を送出します。不正なスタックサイズが指定された場合、 ValueError を送出して、スタックサイズは変更されません。32 KiB は現在のインタープリタ自身のために十分であると保証された最小のスタックサイズです。いくつかのプラットフォームではスタックサイズに対して制限があることに注意してください。例えば最小のスタックサイズが 32 KiB より大きかったり、システムのメモリページサイズ の整数倍の必要があるなどです。この制限についてはプラットフォームのドキュメントを参照してください (一般的なページサイズは 4 KiB なので、プラットフォームに関する情報がない場合は 4096 の整数倍のスタックサイズを選ぶといいかもしれません)。利用可能な環境: Windows、POSIX スレッドに対応したシステム。
threading.TIMEOUT_MAX|ブロックする関数 (Lock.acquire(), RLock.acquire(), Condition.wait() など) の timeout 引数に許される最大値。これ以上の値を timeout に指定すると OverflowError が発生します。

> このモジュールは多くのクラスを定義しています。それらは下記のセクションで詳しく説明されます。

> このモジュールのおおまかな設計は Java のスレッドモデルに基づいています。とはいえ、 Java がロックと条件変数を全てのオブジェクトの基本的な挙動にしているのに対し、 Python ではこれらを別個のオブジェクトに分けています。 Python の Thread クラスがサポートしているのは Java の Thread クラスの挙動のサブセットにすぎません; 現状では、優先度 (priority)やスレッドグループがなく、スレッドの破壊 (destroy)、中断 (stop)、一時停止 (suspend)、復帰 (resume)、割り込み (interrupt) は行えません。 Java の Thread クラスにおける静的メソッドに対応する機能が実装されている場合にはモジュールレベルの関数になっています。

> 以下に説明するメソッドは全て原子的 (atomic) に実行されます。

## [17.1.1. スレッドローカルデータ](https://docs.python.jp/3/library/threading.html#thread-local-data)

> スレッドローカルデータは、その値がスレッド固有のデータです。スレッドローカルデータを管理するには、単に local (あるいはそのサブクラス) のインスタンスを作成して、その属性に値を設定してください:

```python
mydata = threading.local()
mydata.x = 1
```

> インスタンスの値はスレッドごとに違った値になります。

属性|概要
----|----
class threading.local|スレッドローカルデータを表現するクラス。

> 詳細と例題については、 _threading_local モジュールのドキュメンテーション文字列を参照してください。

## [17.1.2. Thread オブジェクト](https://docs.python.jp/3/library/threading.html#thread-objects)

> Thread クラスは個別のスレッド中で実行される活動 (activity) を表現します。活動を決める方法は 2 つあり、一つは呼び出し可能オブジェクトをコンストラクタへ渡す方法、もう一つはサブクラスで run() メソッドをオーバライドする方法です。 (コンストラクタを除く) その他のメソッドは一切サブクラスでオーバライドしてはなりません。言い換えるならば、このクラスの __init__() と run() メソッド だけ をオーバライドしてくださいということです。

> ひとたびスレッドオブジェクトを生成すると、スレッドの start() メソッドを呼び出して活動を開始しなければなりません。 start() メソッド はそれぞれのスレッドの run() メソッドを起動します。

> スレッドの活動が始まると、スレッドは '生存中 (alive)' とみなされます。 スレッドは、通常 run() メソッドが終了するまで、もしくは捕捉されない例外が送出されるまで生存中となります。 is_alive() メソッドは、スレッドが生存中であるかどうか調べます。

> スレッドは他のスレッドの join() メソッドを呼び出すことができます。このメソッドは、 join() メソッドを呼ばれたスレッドが終了するまでメソッドの呼び出し元のスレッドをブロックします。

> スレッドは名前を持っています。名前はコンストラクタに渡すことができ、 name 属性を通して読み出したり変更したりできます。

> スレッドには "デーモンスレッド (daemon thread)" であるというフラグを立てられます。 このフラグには、残っているスレッドがデーモンスレッドだけになった時に Python プログラム全体を終了させるという意味があります。フラグの初期値はスレッドを生成したスレッドから継承します。フラグの値は daemon プロパティまたは daemon コンストラクタ引数を通して設定できます。

### 注釈

> デーモンスレッドは終了時にいきなり停止されます。デーモンスレッドで使われたリソース (開いているファイル、データベースのトランザクションなど) は適切に解放されないかもしれません。きちんと (gracefully) スレッドを停止したい場合は、スレッドを非デーモンスレッドにして、Event のような適切なシグナル送信機構を使用してください。

> スレッドには "主スレッド (main thread)" オブジェクトがあります。主スレッドは Python プログラムを最初に制御していたスレッドです。主スレッドはデーモンスレッドではありません。

> "ダミースレッド (dummy thread)" オブジェクトを作成することができます。 ダミースレッドは、 "外来スレッド (alien thread)" に対応するスレッドオブジェクトです。ダミースレッドは、 C コードから直接生成されたスレッドのような、 threading モジュールの外で開始された処理スレッドです。 ダミースレッドオブジェクトには限られた機能しかなく、常に生存中、かつデーモンスレッドであるとみなされ、 join() できません。また、外来スレッドの終了を検出するのは不可能なので、ダミースレッドは削除できません。

属性|概要
----|----
class threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None)|コンストラクタは常にキーワード引数を使って呼び出さなければなりません。各引数は以下の通りです:
start()|スレッドの活動を開始します。
run()|スレッドの活動をもたらすメソッドです。
join(timeout=None)|スレッドが終了するまで待機します。 このメソッドは、 join() を呼ばれたスレッドが正常終了あるいは処理されない例外によって終了するか、オプションのタイムアウトが発生するまで、メソッドの呼び出し元のスレッドをブロックします。
name|識別のためにのみ用いられる文字列です。名前には機能上の意味づけ (semantics) はありません。複数のスレッドに同じ名前をつけてもかまいません。名前の初期値はコンストラクタで設定されます。
getName(), setName()|name に対する古い getter/setter API; 代わりにプロパティを直接使用してください。
ident|The 'thread identifier' of this thread or None if the thread has not been started. This is a nonzero integer. See the get_ident() function. Thread identifiers may be recycled when a thread exits and another thread is created. The identifier is available even after the thread has exited.
is_alive()|スレッドが生存中かどうかを返します。
daemon|このスレッドがデーモンスレッドか (True) か否か (False) を示すブール値。この値は start() の呼び出し前に設定されなければなりません。さもなければ RuntimeError が送出されます。初期値は生成側のスレッドから継承されます; メインスレッドはデーモンスレッドではないので、メインスレッドで作成されたすべてのスレッドは、デフォルトで daemon = False になります。
isDaemon(), setDaemon()|daemon に対する古い getter/setter API; 代わりにプロパティを直接使用してください。

> CPython 実装の詳細: CPython は Global Interpreter Lock のため、ある時点で Python コードを実行できるスレッドは1つに限られます (ただし、いくつかのパフォーマンスが強く求められるライブラリはこの制限を克服しています)。アプリケーションにマルチコアマシンの計算能力をより良く利用させたい場合は、 multiprocessing モジュールや concurrent.futures.ProcessPoolExecutor の利用をお勧めします。 ただし、I/Oバウンドなタスクを並行して複数走らせたい場合においては、 マルチスレッドは正しい選択肢です。

## [17.1.3. Lock オブジェクト](https://docs.python.jp/3/library/threading.html#lock-objects)

> プリミティブロックとは、ロックが生じた際に特定のスレッドによって所有されない同期プリミティブです。 Python では現在のところ拡張モジュール _thread で直接実装されている最も低水準の同期プリミティブを使えます。

> プリミティブロックは2つの状態、 "ロック" または "アンロック" があります。ロックはアンロック状態で作成されます。ロックには基本となる二つのメソッド、 acquire() と release() があります。ロックの状態がアンロックである場合、 acquire() は状態をロックに変更して即座に処理を戻します。 状態がロックの場合、 acquire() は他のスレッドが release() を呼び出してロックの状態をアンロックに変更するまでブロックします。その後、 acquire() 呼び出しは状態を再度ロックに設定してから処理を戻します。 release() メソッドを呼び出すのはロック状態のときでなければなりません; このメソッドはロックの状態をアンロックに変更して、即座に処理を戻します。 アンロックの状態のロックを解放しようとすると RuntimeError が送出されます。

> ロックは コンテキストマネージメントプロトコル もサポートします。

> 複数のスレッドにおいて acquire() がアンロック状態への遷移を待っているためにブロックが起きている時に release() を呼び出してロックの状態をアンロックにすると、一つのスレッドだけが処理を進行できます。 どのスレッドが処理を進行できるのかは定義されておらず、実装によって異なるかもしれません。

> 全てのメソッドはアトミックに実行されます。

属性|概要
----|----
class threading.Lock|プリミティブロック (primitive lock) オブジェクトを実装しているクラスです。スレッドが一度ロックを獲得すると、それ以後のロック獲得の試みはロックが解放されるまでブロックします。どのスレッドでもロックを解放できます。
acquire(blocking=True, timeout=-1)|ブロックあり、またはブロックなしでロックを獲得します。
release()|ロックを解放します。これはロックを獲得したスレッドだけでなく、任意のスレッドから呼ぶことができます。

## [17.1.4. RLock オブジェクト](https://docs.python.jp/3/library/threading.html#rlock-objects)

> 再入可能ロック (reentrant lock) とは、同じスレッドが複数回獲得できるような同期プリミティブです。再入可能ロックの内部では、プリミティブロックの使うロック／アンロック状態に加え、 "所有スレッド (owning thread)" と "再帰レベル (recursion level)" という概念を用いています。ロック状態では何らかのスレッドがロックを所有しており、アンロック状態ではいかなるスレッドもロックを所有していません。

> このロックの状態をロックにするには、スレッドがロックの acquire() メソッドを呼び出します。このメソッドはスレッドがロックを所有すると処理を戻します。ロックの状態をアンロックにするには release() メソッドを呼び出します。 acquire() / release() からなるペアの呼び出しはネストできます; 最後に呼び出した release() (最も外側の呼び出しペアの release()) だけがロックの状態をアンロックにリセットして、 acquire() でブロック中の別のスレッドの処理を進行させることができます。

> 再入可能ロックは コンテキストマネージメントプロトコル もサポートします。

属性|概要
----|----
class threading.RLock|このクラスは再入可能ロックオブジェクトを実装します。再入可能ロックはそれを獲得したスレッドによって解放されなければなりません。いったんスレッドが再入可能ロックを獲得すると、同じスレッドはブロックされずにもう一度それを獲得できます ; そのスレッドは獲得した回数だけ解放しなければいけません。
acquire(blocking=True, timeout=-1)|ブロックあり、またはブロックなしでロックを獲得します。
release()|再帰レベルをデクリメントしてロックを解放します。デクリメント後に再帰レベルがゼロになった場合、ロックの状態をアンロック (いかなるスレッドにも所有されていない状態) にリセットし、ロックの状態がアンロックになるのを待ってブロックしているスレッドがある場合にはその中のただ一つだけが処理を進行できるようにします。デクリメント後も再帰レベルがゼロでない場合、ロックの状態はロックのままで、呼び出し側のスレッドに所有されたままになります。

## [17.1.5. Condition オブジェクト](https://docs.python.jp/3/library/threading.html#condition-objects)

> 条件変数 (condition variable) は、常にある種のロックに関連付けられています; このロックは明示的に渡すことも、デフォルトで生成させることもできます。複数の条件変数で同じロックを共有しなければならない場合には、引渡しによる関連付けが便利です。ロックは条件オブジェクトの一部です: それを別々に扱う必要はありません。

> 条件変数は コンテキスト管理プロトコル に従います: with 文を使って囲まれたブロックの間だけ関連付けられたロックを獲得することができます。 acquire() メソッドと release() メソッドは、さらに関連付けられたロックの対応するメソッドを呼び出します。

> 他のメソッドは、関連付けられたロックを保持した状態で呼び出さなければなりません。 wait() メソッドはロックを解放します。そして別のスレッドが notify() または notify_all() を呼ぶことによってスレッドを起こすまでブロックします。一旦起こされたなら、 wait() は再びロックを得て戻ります。タイムアウトを指定することも可能です。

> notify() メソッドは条件変数待ちのスレッドを1つ起こします。 notify_all() メソッドは条件変数待ちの全てのスレッドを起こします。

> 注意: notify() と notify_all() はロックを解放しません; 従って、スレッドが起こされたとき、 wait() の呼び出しは即座に処理を戻すわけではなく、 notify() または notify_all() を呼び出したスレッドが最終的にロックの所有権を放棄したときに初めて処理を返すのです。

> 条件変数を使う典型的なプログラミングスタイルでは、何らかの共有された状態変数へのアクセスを同期させるためにロックを使います; 状態変数が特定の状態に変化したことを知りたいスレッドは、自分の望む状態になるまで繰り返し wait() を呼び出します。その一方で、状態変更を行うスレッドは、前者のスレッドが待ち望んでいる状態であるかもしれないような状態へ変更を行ったときに notify() や notify_all() を呼び出します。例えば、以下のコードは無制限のバッファ容量のときの一般的な生産者-消費者問題です:

```python
# Consume one item
with cv:
    while not an_item_is_available():
        cv.wait()
    get_an_available_item()

# Produce one item
with cv:
    make_an_item_available()
    cv.notify()
```

> アプリケーションの条件をチェックする while ループは必須です。なぜなら、 wait() が任意の長時間の後で返り、 notify() 呼び出しを促した条件がもはや真でないことがありえるからです。これはマルチスレッドプログラミングに固有です。条件チェックを自動化するために wait_for() メソッドを使うことができ、それはタイムアウトの計算を簡略化します:

```python
# Consume an item
with cv:
    cv.wait_for(an_item_is_available)
    get_an_available_item()
```

> notify() と notify_all() のどちらを使うかは、その状態の変化に興味を持っている待ちスレッドが一つだけなのか、あるいは複数なのかで考えます。例えば、典型的な生産者-消費者問題では、バッファに1つの要素を加えた場合には消費者スレッドを 1 つしか起こさなくてかまいません。

属性|概要
----|----
class threading.Condition(lock=None)|このクラスは条件変数 (condition variable) オブジェクトを実装します。条件変数を使うと、ある複数のスレッドを別のスレッドの通知があるまで待機させられます。
acquire(*args)|根底にあるロックを獲得します。このメソッドは根底にあるロックの対応するメソッドを呼び出します。そのメソッドの戻り値を返します。
release()|根底にあるロックを解放します。このメソッドは根底にあるロックの対応するメソッドを呼び出します。戻り値はありません。
wait(timeout=None)|通知 (notify) を受けるか、タイムアウトするまで待機します。呼び出し側のスレッドがロックを獲得していないときにこのメソッドを呼び出すと RuntimeError が送出されます。
wait_for(predicate, timeout=None)|条件が真と判定されるまで待ちます。 predicate は呼び出し可能オブジェクトでなければならず、その結果はブール値として解釈されます。 最大の待ち時間を指定する timeout を与えることができます。
notify(n=1)|デフォルトで、この条件変数を待っている1つのスレッドを起こします。 呼び出し側のスレッドがロックを獲得していないときにこのメソッドを呼び出すと RuntimeError が送出されます。
notify_all()|この条件を待っているすべてのスレッドを起こします。このメソッドは notify() のように動作しますが、 1 つではなくすべての待ちスレッドを起こします。呼び出し側のスレッドがロックを獲得していない場合、 RuntimeError が送出されます。

## [17.1.6. Semaphore オブジェクト](https://docs.python.jp/3/library/threading.html#semaphore-objects)

> セマフォ (semaphore) は、計算機科学史上最も古い同期プリミティブの一つ で、草創期のオランダ計算機科学者 Edsger W. Dijkstra によって発明されました (彼は acquire() と release() の代わりに P() と V() を使いました)。

> セマフォは acquire() でデクリメントされ release() でインクリメントされるような内部カウンタを管理します。 カウンタは決してゼロより小さくはなりません; acquire() は、カウンタがゼロになっている場合、他のスレッドが release() を呼び出すまでブロックします。

> セマフォは コンテキストマネージメントプロトコル もサポートします。

属性|概要
----|----
class threading.Semaphore(value=1)|このクラスはセマフォ (semaphore) オブジェクトを実装します。セマフォは、 release() を呼び出した数から acquire() を呼び出した数を引き、初期値を足した値を表すカウンタを管理します。 acquire() メソッドは、カウンタの値を負にせずに処理を戻せるまで必要ならば処理をブロックします。 value を指定しない場合、デフォルトの値は 1 になります。
acquire(blocking=True, timeout=None)|セマフォを獲得します。
release()|内部カウンタを 1 インクリメントして、セマフォを解放します。 release() 処理に入ったときにカウンタがゼロであり、カウンタの値がゼロより大きくなるのを待っている別のスレッドがあった場合、そのスレッドを起こします。
class threading.BoundedSemaphore(value=1)|有限セマフォ (bounded semaphore) オブジェクトを実装しているクラスです。有限セマフォは、現在の値が初期値を超過しないようチェックを行います。超過を起こした場合、 ValueError を送出します。たいていの場合、セマフォは限られた容量のリソースを保護するために使われるものです。従って、あまりにも頻繁なセマフォの解放はバグが生じているしるしです。 value を指定しない場合、デフォルトの値は 1 になります。

### [17.1.6.1. Semaphore の例](https://docs.python.jp/3/library/threading.html#semaphore-example)

> セマフォはしばしば、容量に限りのある資源、例えばデータベースサーバなどを保護するために使われます。リソースが固定の状況では、常に有限セマフォを使わなければなりません。主スレッドは、作業スレッドを立ち上げる前にセマフォを初期化します:

```python
maxconnections = 5
# ...
pool_sema = BoundedSemaphore(value=maxconnections)
```

> 作業スレッドは、ひとたび立ち上がると、サーバへ接続する必要が生じたときにセマフォの acquire() および release() メソッドを呼び出します:

```python
with pool_sema:
    conn = connectdb()
    try:
        # ... use connection ...
    finally:
        conn.close()
```

> 有限セマフォを使うと、セマフォを獲得回数以上に解放してしまうというプログラム上の間違いを見逃しにくくします。

## [17.1.7. Event オブジェクト](https://docs.python.jp/3/library/threading.html#event-objects)

> イベントは、あるスレッドがイベントを発信し、他のスレッドはそれを待つという、スレッド間で通信を行うための最も単純なメカニズムの一つです。

> イベントオブジェクトは内部フラグを管理します。このフラグは set() メソッドで値を true に、 clear() メソッドで値を false にリセットします。 wait() メソッドはフラグが true になるまでブロックします。

属性|概要
----|----
class threading.Event|イベントオブジェクトを実装しているクラスです。イベントは set() メソッドを使うと True に、 clear() メソッドを使うと False にセットされるようなフラグを管理します。 wait() メソッドは、全てのフラグが true になるまでブロックするようになっています。フラグの初期値は false です。
is_set()|内部フラグの値が true である場合にのみ true を返します。
set()|内部フラグの値を true にセットします。フラグの値が true になるのを待っている全てのスレッドを起こします。一旦フラグが true になると、スレッドが wait() を呼び出しても全くブロックしなくなります。
clear()|内部フラグの値を false にリセットします。以降は、 set() を呼び出して再び内部フラグの値を true にセットするまで、 wait() を呼び出したスレッドはブロックするようになります。
wait(timeout=None)|内部フラグの値が true になるまでブロックします。 wait() 処理に入った時点で内部フラグの値が true であれば、直ちに処理を戻します。そうでない場合、他のスレッドが set() を呼び出してフラグの値を true にセットするか、オプションのタイムアウトが発生するまでブロックします。

## [17.1.8. Timer オブジェクト](https://docs.python.jp/3/library/threading.html#timer-objects)

> このクラスは、一定時間経過後に実行される活動、すなわちタイマ活動を表現します。 Timer は Thread のサブクラスであり、自作のスレッドを構築した一例でもあります。

> タイマは start() メソッドを呼び出すとスレッドとして作動し始めします。 (活動を開始する前に) cancel() メソッドを呼び出すと、タイマを停止できます。タイマが活動を実行するまでの待ち時間は、ユーザが指定した待ち時間と必ずしも厳密には一致しません。

> 例えば:

```python
def hello():
    print("hello, world")

t = Timer(30.0, hello)
t.start()  # after 30 seconds, "hello, world" will be printed
```

属性|概要
----|----
class threading.Timer(interval, function, args=None, kwargs=None)|interval 秒後に引数 args キーワード引数 kwargs で function を実行するようなタイマを生成します。args*が ``None`` (デフォルト) なら空のリストが使用されます。*kwargs が None (デフォルト) なら空の辞書が使用されます。
cancel()|タイマをストップして、その動作の実行をキャンセルします。このメソッドはタイマがまだ活動待ち状態にある場合にのみ動作します。

## [17.1.9. バリアオブジェクト](https://docs.python.jp/3/library/threading.html#barrier-objects)

> This class provides a simple synchronization primitive for use by a fixed number of threads that need to wait for each other. Each of the threads tries to pass the barrier by calling the wait() method and will block until all of the threads have made their wait() calls. At this point, the threads are released simultaneously.

> バリアは同じ数のスレッドに対して何度でも再利用することができます。

> 例として、クライアントとサーバの間でスレッドを同期させる単純な方法を紹介します:

```python
b = Barrier(2, timeout=5)

def server():
    start_server()
    b.wait()
    while True:
        connection = accept_connection()
        process_server_connection(connection)

def client():
    b.wait()
    while True:
        connection = make_connection()
        process_client_connection(connection)
```

属性|概要
----|----
class threading.Barrier(parties, action=None, timeout=None)|parties 個のスレッドのためのバリアオブジェクトを作成します。 action は、もし提供されるなら呼び出し可能オブジェクトで、スレッドが解放される時にそのうちの1つによって呼ばれます。 timeout は、 wait() メソッドに対して none が指定された場合のデフォルトのタイムアウト値です。
wait(timeout=None)|バリアを通ります。バリアに対するすべてのスレッドがこの関数を呼んだ時に、それらは同時にすべて解放されます。timeout が提供される場合、それはクラスコンストラクタに渡された値に優先して使用されます。
reset()|バリアをデフォルトの空の状態に戻します。そのバリアの上で待っているすべてのスレッドは BrokenBarrierError 例外を受け取ります。
abort()|バリアを broken な状態にします。これによって、現在または将来の wait() 呼び出しが BrokenBarrierError とともに失敗するようになります。これを使うと、例えば異常終了する必要がある場合にアプリケーションがデッドロックするのを避けることができます。
parties|バリアを通るために要求されるスレッドの数。
n_waiting|現在バリアの中で待っているスレッドの数。
broken|バリアが broken な状態である場合に True となるブール値。

exception threading.BrokenBarrierError|Barrier オブジェクトがリセットされるか broken な場合に、この例外 (RuntimeError のサブクラス) が送出されます。

## [17.1.10. with 文でのロック・条件変数・セマフォの使い方](https://docs.python.jp/3/library/threading.html#using-locks-conditions-and-semaphores-in-the-with-statement)

> このモジュールのオブジェクトのうち acquire() メソッドと release() メソッドを備えているものは全て with 文のコンテキストマネージャ として使うことができます。 with 文のブロックに入るときに acquire() メソッドが 呼び出され、ブロック脱出時には release() メソッドが呼ばれます。したがって、次のコード:


```python
with some_lock:
    # do something...
```

> は、以下と同じです


```python
some_lock.acquire()
try:
    # do something...
finally:
    some_lock.release()
```

> 現在のところ、 Lock 、 RLock 、 Condition 、 Semaphore 、 BoundedSemaphore を with 文のコンテキストマネージャとして使うことができます。

