# [17.5. subprocess — サブプロセス管理](https://docs.python.jp/3/library/subprocess.html)

< [17. 並行実行](https://docs.python.jp/3/library/concurrency.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

ソースコード: [Lib/subprocess.py](https://github.com/python/cpython/tree/3.6/Lib/subprocess.py)

> subprocess モジュールは新しいプロセスの開始、入力/出力/エラーパイプの接続、リターンコードの取得を可能とします。このモジュールは以下の古いモジュールや関数を置き換えることを目的としています：

* os.system
* os.spawn*

> これらのモジュールや関数の代わりに、subprocess モジュールをどのように使うかについてを以下の節で説明します。

> 参考

[PEP 324](https://www.python.org/dev/peps/pep-0324) – subprocess モジュールを提案している PEP 

## [17.5.1. subprocess モジュールを使う](https://docs.python.jp/3/library/subprocess.html#using-the-subprocess-module)

> サブプロセスを起動する推奨手段は、すべての用法を扱える run() 関数を使用することです。より高度な用法では下層の Popen インターフェースを直接使用することもできます。

> run() 関数は Python 3.5 で追加されました; 過去のバージョンとの互換性の維持が必要な場合は、古い高水準 API 節をご覧ください。

属性|説明
----|----
subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None, check=False, encoding=None, errors=None)|args で指定されたコマンドを実行します。コマンドの完了を待って、CompletedProcess インスタンスを返します。
class subprocess.CompletedProcess|run() の戻り値。プロセスが終了したことを表します。
args|プロセスを起動するときに使用された引数。1 個のリストか 1 個の文字列になります。
returncode|子プロセスの終了コード。一般に、終了ステータス 0 はプロセスが正常に終了したことを示します。
stdout|Captured stdout from the child process. A bytes sequence, or a string if run() was called with an encoding or errors. None if stdout was not captured.
stderr|Captured stderr from the child process. A bytes sequence, or a string if run() was called with an encoding or errors. None if stderr was not captured.
check_returncode()|returncode が非ゼロの場合、CalledProcessError が送出されます。
subprocess.DEVNULL|Popen の stdin, stdout, stderr 引数に渡して、標準入出力を os.devnull から入出力するように指定するための特殊値です。
subprocess.PIPE|Popen の stdin, stdout, stderr 引数に渡して、標準ストリームに対するパイプを開くことを指定するための特殊値です。Popen.communicate() に非常に有用です。
subprocess.STDOUT|Popen の stderr 引数に渡して、標準エラー出力が標準出力と同じハンドルに出力されるように指定するための特殊値です。
exception subprocess.SubprocessError|このモジュールの他のすべての例外のための基底クラスです。
exception subprocess.TimeoutExpired|SubprocessError のサブクラスです。子プロセスの終了を待機している間にタイムアウトが発生した場合に送出されます。
cmd|子プロセスの生成に使用されるコマンド本文。
timeout|タイムアウト秒数。
output|run() または check_output() によって捕捉された子プロセスの出力。捕捉されなかったら None になります。
stdout|output の別名。stderr と対になります。
stderr|run() によって捕捉された子プロセスの標準エラー出力。捕捉されなかったら None になります。
exception subprocess.CalledProcessError|SubprocessError のサブクラスです。check_call() または check_output() によって実行されたプロセスが非ゼロの終了ステータスを返した場合に送出されます。
returncode|子プロセスの終了ステータスです。もしプロセスがシグナルによって終了したなら、これは負のシグナル番号になります。
cmd|子プロセスの生成に使用されるコマンド本文。
output|run() または check_output() によって捕捉された子プロセスの出力。捕捉されなかったら None になります。
stdout|output の別名。stderr と対になります。
stderr|run() によって捕捉された子プロセスの標準エラー出力。捕捉されなかったら None になります。

### [17.5.1.1. よく使われる引数](https://docs.python.jp/3/library/subprocess.html#frequently-used-arguments)

> 幅広い使用例をサポートするために、Popen コンストラクター (とその他の簡易関数) は、多くのオプション引数を受け付けます。一般的な用法については、これらの引数の多くはデフォルト値のままで問題ありません。通常必要とされる引数は以下の通りです:

> args はすべての呼び出しに必要で、文字列あるいはプログラム引数のシーケンスでなければなりません。一般に、引数のシーケンスを渡す方が望ましいです。なぜなら、モジュールが必要な引数のエスケープやクオート (例えばファイル名中のスペースを許すこと) の面倒を見ることができるためです。単一の文字列を渡す場合、shell は True でなければなりません (以下を参照)。もしくは、その文字列は引数を指定せずに実行される単なるプログラムの名前でなければなりません。

> stdin, stdout および stderr には、実行するプログラムの標準入力、標準出力、および標準エラー出力のファイルハンドルをそれぞれ指定します。有効な値は PIPE、DEVNULL、既存のファイル記述子 (正の整数)、既存のファイルオブジェクトおよび None です。PIPE を指定すると新しいパイプが子プロセスに向けて作られます。DEVNULL を指定すると特殊ファイル os.devnull が使用されます。デフォルト設定の None を指定するとリダイレクトは起こりません。子プロセスのファイルハンドルはすべて親から受け継がれます。加えて、stderr を STDOUT にすると、子プロセスの stderr からの出力は stdout と同じファイルハンドルに出力されます。

* If encoding or errors are specified, or universal_newlines is true, the file objects stdin, stdout and stderr will be opened in text mode using the encoding and errors specified in the call or the defaults for io.TextIOWrapper.

* For stdin, line ending characters '\n' in the input will be converted to the default line separator os.linesep. For stdout and stderr, all line endings in the output will be converted to '\n'. For more information see the documentation of the io.TextIOWrapper class when the newline argument to its constructor is None.

* If text mode is not used, stdin, stdout and stderr will be opened as binary streams. No encoding or line ending conversion is performed.

> バージョン 3.6 で追加: Added encoding and errors parameters.

### 注釈

* ファイルオブジェクト Popen.stdin、Popen.stdout ならびに Popen.stderr の改行属性は Popen.communicate() メソッドで更新されません。

* shell が True なら、指定されたコマンドはシェルによって実行されます。あなたが Python を主として (ほとんどのシステムシェル以上の) 強化された制御フローのために使用していて、さらにシェルパイプ、ファイル名ワイルドカード、環境変数展開、~ のユーザーホームディレクトリへの展開のような他のシェル機能への簡単なアクセスを望むなら、これは有用かもしれません。しかしながら、Python 自身が多くのシェル的な機能の実装を提供していることに注意してください (特に glob, fnmatch, os.walk(), os.path.expandvars(), os.path.expanduser(), shutil)。

* バージョン 3.3 で変更: universal_newlines が True の場合、クラスはエンコーディング locale.getpreferredencoding() の代わりに locale.getpreferredencoding(False) を使用します。この変更についての詳細は、 io.TextIOWrapper クラスを参照してください。

### 注釈

* shell=True を使う前に セキュリティで考慮すべき点 を読んでください。

> これらのオプションは、他のすべてのオプションとともに Popen コンストラクターのドキュメントの中でより詳細に説明されています。

### [17.5.1.2. Popen コンストラクター](https://docs.python.jp/3/library/subprocess.html#popen-constructor)

> このモジュールの中で、根底のプロセス生成と管理は Popen クラスによって扱われます。簡易関数によってカバーされないあまり一般的でないケースを開発者が扱えるように、Popen クラスは多くの柔軟性を提供しています。

属性|説明
----|----
class subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None, preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=False, startupinfo=None, creationflags=0, restore_signals=True, start_new_session=False, pass_fds=(), *, encoding=None, errors=None)|新しいプロセスで子のプログラムを実行します。POSIX においては、子のプログラムを実行するために、このクラスは os.execvp() のような挙動を使用します。Windows においては、このクラスは Windows の CreateProcess() 関数を使用します。Popen への引数は以下の通りです。

> args はプログラム引数のシーケンスか、単一の文字列でなければなりません。デフォルトでは、args がシーケンスの場合に実行されるプログラムは args の最初の要素です。args が文字列の場合、解釈はプラットフォーム依存であり、下記に説明されます。デフォルトの挙動からの追加の違いについては shell および executable 引数を参照してください。特に明記されない限り、args をシーケンスとして渡すことが推奨されます。

> POSIX 上では、args が文字列の場合、その文字列は実行すべきプログラムの名前またはパスとして解釈されます。しかし、これはプログラムに引数を渡さない場合にのみ可能です。

### 注釈

> args を正しくトークン化するには、shlex.split() が便利です。このメソッドは特に複雑な状況で活躍します:

```python
>>> import shlex, subprocess
>>> command_line = input()
/bin/vikings -input eggs.txt -output "spam spam.txt" -cmd "echo '$MONEY'"
>>> args = shlex.split(command_line)
>>> print(args)
['/bin/vikings', '-input', 'eggs.txt', '-output', 'spam spam.txt', '-cmd', "echo '$MONEY'"]
>>> p = subprocess.Popen(args) # Success!
```

> 特に注意すべき点は、シェル内でスペースで区切られたオプション (-input など) と引数 (eggs.txt など) はリストの別々の要素になるのに対し、シェル内で (上記のスペースを含むファイル名や echo コマンドのように) クォーティングやバックスラッシュエスケープが必要なものは単一のリスト要素であることです。

> Windows 上では、args がシーケンスなら Windows における引数シーケンスから文字列への変換 に記述された方法で文字列に変換されます。これは根底の CreateProcess() が文字列上で動作するからです。

> shell 引数 (デフォルトでは False) は、実行するプログラムとしてシェルを使用するかどうかを指定します。 shell が True の場合、 args をシーケンスとしてではなく文字列として渡すことが推奨されます。

> POSIX で shell=True の場合、シェルのデフォルトは /bin/sh になります。args が文字列の場合、この文字列はシェルを介して実行されるコマンドを指定します。したがって、文字列は厳密にシェルプロンプトで打つ形式と一致しなければなりません。例えば、文字列の中にスペースを含むファイル名がある場合は、クォーティングやバックスラッシュエスケープが必要です。args がシーケンスの場合には、最初の要素はコマンド名を表わす文字列として、残りの要素は追加の引数としてシェルに渡されます。つまり、以下の Popen と等価ということです:

```python
Popen(['/bin/sh', '-c', args[0], args[1], ...])
```

> Windows で shell=True とすると、COMSPEC 環境変数がデフォルトシェルを指定します。Windows で shell=True を指定する必要があるのは、実行したいコマンドがシェルに組み込みの場合だけです (例えば dir や copy)。バッチファイルやコンソールベースの実行ファイルを実行するために shell=True は必要ありません。

### 注釈

> shell=True を使う前に セキュリティで考慮すべき点 を読んでください。

> bufsize は標準入力/標準出力/標準エラー出力パイプファイルオブジェクトを生成するときに open() 関数の対応する引数に渡されます:

* 0 はバッファーされないことを意味します (読み込みおよび書き出しのたびにシステムコールが行われ、すぐに復帰します)。
* 1 はラインバッファーを意味します (universal_newlines=True、すなわちテキストモードの場合のみ使用可能)。
* それ以外の正の整数はバッファーのおよそのサイズになることを意味します。
* 負のサイズ (デフォルト) は io.DEFAULT_BUFFER_SIZE のシステムデフォルトが使用されることを意味します。

> バージョン 3.3.1 で変更: ほとんどのコードが期待する振る舞いに合わせてデフォルトでバッファリングが有効となるよう bufsize のデフォルト値が -1 になりました。Python 3.2.4 および 3.3.1 より前のバージョンでは、誤ってバッファーされず短い読み込みを許可する 0 がデフォルトになっていました。これは意図したものではなく、ほとんどのコードが期待する Python 2 での振る舞いとも一致していませんでした。

> executable 引数は、実行する置換プログラムを指定します。これが必要になるのは極めて稀です。shell=False のときは、executable は args で指定されている実行プログラムを置換します。しかし、オリジナルの args は依然としてプログラムに渡されます。ほとんどのプログラムは、args で指定されたプログラムをコマンド名として扱います。そして、それは実際に実行されたプログラムとは異なる可能性があります。POSIX において、ps のようなユーティリティの中では、args 名が実行ファイルの表示名になります。shell=True の場合、POSIX において executable 引数はデフォルトの /bin/sh に対する置換シェルを指定します。

> stdin、stdout および stderr には、実行するプログラムの標準入力、標準出力、および標準エラー出力のファイルハンドルをそれぞれ指定します。有効な値は PIPE, DEVNULL, 既存のファイル記述子 (正の整数)、既存の ファイルオブジェクト 、そして None です。PIPE を指定すると新しいパイプが子プロセスに向けて作られます。DEVNULL を指定すると特殊ファイル os.devnull が使用されます。デフォルト設定の None を指定するとリダイレクトは起こりません。子プロセスのファイルハンドルはすべて親から受け継がれます。加えて、stderr を STDOUT にすると、子プロセスの標準エラー出力からの出力は標準出力と同じファイルハンドルに出力されます。

> preexec_fn に呼び出し可能オブジェクトが指定されている場合、このオブジェクトは子プロセスが実行される直前 (fork されたあと、exec される直前) に子プロセス内で呼ばれます。(POSIXのみ)

### 警告

> アプリケーション中に複数のスレッドが存在する状態で preexec_fn 引数を使用するのは安全ではありません。exec が呼ばれる前に子プロセスがデッドロックを起こすことがあります。それを使用しなければならない場合、プログラムを自明なものにしておいてください! 呼び出すライブラリの数を最小にしてください。

### 注釈

> 子プロセスのために環境を変更する必要がある場合は、preexec_fn の中でそれをするのではなく env 引数を使用します。start_new_session 引数は、子プロセスの中で os.setsid() を呼ぶ過去の一般的な preexec_fn の使用方法の代わりになります。

> close_fds が真の場合、子プロセスが実行される前に 0, 1, 2 以外のすべてのファイル記述子が閉じられます (POSIXのみ)。デフォルトはプラットフォームによって異なります: POSIX では常に真です。 Windows では stdin/stdout/stderr が None のときに真で、None 以外なら偽です。Windows で close_fds が真の場合、すべてのファイルハンドルは子プロセスに引き継がれません。 Windows の場合、close_fds を真にしながら、stdin, stdout, stderr を利用して標準ハンドルをリダイレクトすることはできません。

> バージョン 3.2 で変更: close_fds のデフォルトは、False から上記のものに変更されました。

> pass_fds はオプションで、親と子の間で開いたままにしておくファイル記述子のシーケンスを指定します。何らかの pass_fds を渡した場合、close_fds は強制的に True になります。(POSIXのみ)

> バージョン 3.2 で追加: pass_fds 引数が追加されました。

> If cwd is not None, the function changes the working directory to cwd before executing the child. cwd can be a str and path-like object. In particular, the function looks for executable (or for the first item in args) relative to cwd if the executable path is a relative path.

> バージョン 3.6 で変更: cwd parameter accepts a path-like object.

> restore_signals が真の場合 (デフォルト)、Python が SIG_IGN に設定したすべてのシグナルは子プロセスが exec される前に子プロセスの SIG_DFL に格納されます。現在これには SIGPIPE, SIGXFZ および SIGXFSZ シグナルが含まれています。(POSIX のみ)

> バージョン 3.2 で変更: restore_signals が追加されました。

> start_new_session が真の場合、サブプロセスの実行前に子プロセス内で setsid() システムコールが作成されます。(POSIX のみ)

> バージョン 3.2 で変更: start_new_session が追加されました。

> env が None 以外の場合、これは新しいプロセスでの環境変数を定義します。デフォルトでは、子プロセスは現在のプロセスの環境変数を引き継ぎます。

### 注釈

> env を指定する場合、プログラムを実行するのに必要な変数すべてを与えなければなりません。Windows で Side-by-Side アセンブリ を実行するためには、env は正しい SystemRoot を 含まなければなりません 。

> If encoding or errors are specified, the file objects stdin, stdout and stderr are opened in text mode with the specified encoding and errors, as described above in よく使われる引数. If universal_newlines is True, they are opened in text mode with default encoding. Otherwise, they are opened as binary streams.

> バージョン 3.6 で追加: encoding and errors were added.

> startupinfo は、基底の CreateProcess 関数に渡される STARTUPINFO オブジェクトになります。creationflags は、与えられるなら、CREATE_NEW_CONSOLE または CREATE_NEW_PROCESS_GROUP にできます。(Windows のみ)

> Popen オブジェクトは with 文によってコンテキストマネージャーとしてサポートされます: 終了時には標準ファイル記述子が閉じられ、プロセスを待機します:

```python
with Popen(["ifconfig"], stdout=PIPE) as proc:
    log.write(proc.stdout.read())
```

> バージョン 3.2 で変更: コンテキストマネージャーサポートが追加されました。

> バージョン 3.6 で変更: Popen destructor now emits a ResourceWarning warning if the child process is still running.

### [17.5.1.3. 例外](https://docs.python.jp/3/library/subprocess.html#exceptions)

> 子プロセス内で送出された例外は、新しいプログラムの実行開始の前に親プロセスで再送出されます。さらに、この例外オブジェクトには child_traceback という属性が追加されています。この属性は子プロセスの視点からの traceback 情報が格納された文字列です。

> もっとも一般的に起こる例外は OSError です。これは、たとえば存在しないファイルを実行しようとしたときなどに発生します。アプリケーションは OSError 例外に備えておかなければなりません。

> 不正な引数で Popen が呼ばれた場合は ValueError が発生します。

> 呼び出されたプロセスが非ゼロのリターンコードを返した場合 check_call() や check_output() は CalledProcessError を送出します。

> call() や Popen.communicate() のような timeout 引数を受け取るすべての関数とメソッドは、プロセスが終了する前にタイムアウトが発生した場合に TimeoutExpired を送出します。

> このモジュールで定義されたすべての例外は SubprocessError を継承しています。

> バージョン 3.3 で追加: SubprocessError 基底クラスが追加されました。

## [17.5.2. セキュリティで考慮すべき点](https://docs.python.jp/3/library/subprocess.html#security-considerations)

> その他一部の popen 関数と異なり、この実装は暗黙的にシステムシェルを呼び出すことはありません。これはシェルのメタ文字を含むすべての文字が子プロセスに安全に渡されることを意味します。shell=True でシェルを明示的に呼びだした場合、シェルインジェクション の脆弱性に対処するための、すべての空白やメタ文字の適切なクオートの保証はアプリケーションの責任になります。

> shell=True を使用するときは、シェルコマンドで使用される文字列の空白やメタ文字は shlex.quote() 関数を使うと正しくエスケープできます。

## [17.5.3. Popen オブジェクト](https://docs.python.jp/3/library/subprocess.html#popen-objects)

> Popen クラスのインスタンスには、以下のようなメソッドがあります:

属性|説明
----|----
Popen.poll()|子プロセスが終了しているかどうかを調べます。returncode 属性を設定して返します。
Popen.wait(timeout=None)|子プロセスが終了するまで待ちます。returncode 属性を設定して返します。
Popen.communicate(input=None, timeout=None)|Interact with process: Send data to stdin. Read data from stdout and stderr, until end-of-file is reached. Wait for process to terminate. The optional input argument should be data to be sent to the child process, or None, if no data should be sent to the child. If streams were opened in text mode, input must be a string. Otherwise, it must be bytes.
Popen.send_signal(signal)|signal シグナルを子プロセスに送ります。
Popen.terminate()|子プロセスを停止します。Posix OS では、このメソッドは SIGTERM シグナルを子プロセスに送ります。Windows では、Win32 API の TerminateProcess() 関数を利用して子プロセスを止めます。
Popen.kill()|子プロセスを kill します。Posix OS では SIGKILL シグナルを子プロセスに送ります。Windows では、kill() は terminate() の別名です。
Popen.args|Popen に渡された引数 args です – プログラム引数のシーケンスまたは 1 個の文字列になります。
Popen.stdin|If the stdin argument was PIPE, this attribute is a writeable stream object as returned by open(). If the encoding or errors arguments were specified or the universal_newlines argument was True, the stream is a text stream, otherwise it is a byte stream. If the stdin argument was not PIPE, this attribute is None.
Popen.stdout|If the stdout argument was PIPE, this attribute is a readable stream object as returned by open(). Reading from the stream provides output from the child process. If the encoding or errors arguments were specified or the universal_newlines argument was True, the stream is a text stream, otherwise it is a byte stream. If the stdout argument was not PIPE, this attribute is None.
Popen.stderr|If the stderr argument was PIPE, this attribute is a readable stream object as returned by open(). Reading from the stream provides error output from the child process. If the encoding or errors arguments were specified or the universal_newlines argument was True, the stream is a text stream, otherwise it is a byte stream. If the stderr argument was not PIPE, this attribute is None.
Popen.pid|子プロセスのプロセス ID が入ります。
Popen.returncode|poll() か wait() (か、間接的に communicate()) から設定された、子プロセスの終了ステータスが入ります。None はまだその子プロセスが終了していないことを示します。

## [17.5.4. Windows Popen ヘルパー](https://docs.python.jp/3/library/subprocess.html#windows-popen-helpers)
)

> STARTUPINFO クラスと以下の定数は、Windows のみで利用できます。

属性|説明
----|----
class subprocess.STARTUPINFO|Popen の生成に使われる Windows STARTUPINFO 構造の部分的なサポートです。
dwFlags|特定の STARTUPINFO の属性が、プロセスがウィンドウを生成するときに使われるかを決定するビットフィールドです:
hStdInput|dwFlags が STARTF_USESTDHANDLES を指定すれば、この属性がプロセスの標準入力処理です。STARTF_USESTDHANDLES が指定されなければ、標準入力のデフォルトはキーボードバッファーです。
hStdOutput|dwFlags が STARTF_USESTDHANDLES を指定すれば、この属性がプロセスの標準出力処理です。そうでなければ、この属性は無視され、標準出力のデフォルトはコンソールウィンドウのバッファーです。
hStdError|dwFlags が STARTF_USESTDHANDLES を指定すれば、この属性がプロセスの標準エラー処理です。そうでなければ、この属性は無視され、標準エラー出力のデフォルトはコンソールウィンドウのバッファーです。
wShowWindow|dwFlags が STARTF_USESHOWWINDOW を指定すれば、この属性は ShowWindow 関数の nCmdShow 引数で指定された値なら、 SW_SHOWDEFAULT 以外の任意のものにできます。しかし、この属性は無視されます。

### [17.5.4.1. 定数](https://docs.python.jp/3/library/subprocess.html#constants)

> subprocess モジュールは、以下の定数を公開しています。

属性|説明
----|----
subprocess.STD_INPUT_HANDLE|標準入力デバイスです。この初期値は、コンソール入力バッファ、 CONIN$ です。
subprocess.STD_OUTPUT_HANDLE|標準出力デバイスです。この初期値は、アクティブコンソールスクリーン、 CONOUT$ です。
subprocess.STD_ERROR_HANDLE|標準エラーデバイスです。この初期値は、アクティブコンソールスクリーン、 CONOUT$ です。
subprocess.SW_HIDE|ウィンドウを隠します。別のウィンドウがアクティブになります。
subprocess.STARTF_USESTDHANDLES|追加情報を保持する、STARTUPINFO.hStdInput, STARTUPINFO.hStdOutput, および STARTUPINFO.hStdError 属性を指定します。
subprocess.STARTF_USESHOWWINDOW|追加情報を保持する、 STARTUPINFO.wShowWindow 属性を指定します。
subprocess.CREATE_NEW_CONSOLE|新しいプロセスが、親プロセスのコンソールを継承する (デフォルト) のではなく、新しいコンソールを持ちます。
subprocess.CREATE_NEW_PROCESS_GROUP|新しいプロセスグループが生成されることを指定する Popen creationflags パラメーターです。このフラグは、サブプロセスで os.kill() を使うのに必要です。

## [17.5.5. 古い高水準 API](https://docs.python.jp/3/library/subprocess.html#older-high-level-api)

> Python 3.5 より前のバージョンでは、サブプロセスに対して以下の 3 つの関数からなる高水準 API が用意されていました。現在多くの場合 run() の使用で済みますが、既存の多くのコードではこれらの関数が使用されています。

属性|説明
----|----
subprocess.call(args, *, stdin=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None)|args で指定されたコマンドを実行します。コマンドの終了を待ち、returncode 属性を返します。
subprocess.check_call(args, *, stdin=None, stdout=None, stderr=None, shell=False, cwd=None, timeout=None)|指定された引数でコマンドを実行し、完了を待ちます。コマンドのリターンコードがゼロならば返りますが、非ゼロなら CalledProcessError 例外が送出されます。CalledProcessError オブジェクトにはリターンコードが returncode 属性として格納されています。
subprocess.check_output(args, *, stdin=None, stderr=None, shell=False, cwd=None, encoding=None, errors=None, universal_newlines=False, timeout=None)|引数でコマンドを実行し、その出力を返します。
## [17.5.6. 古い関数を subprocess モジュールで置き換える](https://docs.python.jp/3/library/subprocess.html#replacing-older-functions-with-the-subprocess-module)

> この節では、 "a becomes b" と書かれているものは a の代替として b が使えるということを表します。

### 注釈

> この節で紹介されている "a" 関数は全て、実行するプログラムが見つからないときは (おおむね) 静かに終了します。それに対して "b" 代替手段は OSError 例外を送出します。

> また、要求された操作が非ゼロの終了コードを返した場合、check_output() を使用した置き換えは CalledProcessError で失敗します。その出力は、送出された例外の output 属性として利用可能です。

> 以下の例では、適切な関数が subprocess モジュールからすでにインポートされていることを前提としています。


### [17.5.6.1. /bin/sh シェルのバッククォートを置き換える](https://docs.python.jp/3/library/subprocess.html#replacing-bin-sh-shell-backquote)

```python
output=`mycmd myarg`
```

> これは以下のようになります:

```python
output = check_output(["mycmd", "myarg"])
```

### [17.5.6.2. シェルのパイプラインを置き換える](https://docs.python.jp/3/library/subprocess.html#replacing-shell-pipeline)

```python
output=`dmesg | grep hda`
```

> これは以下のようになります:

```python
p1 = Popen(["dmesg"], stdout=PIPE)
p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
output = p2.communicate()[0]
```

> p2 を開始した後の p1.stdout.close() の呼び出しは、p1 が p2 の前に存在した場合に、p1 が SIGPIPE を受け取るために重要です。

> あるいは、信頼された入力に対しては、シェル自身のパイプラインサポートを直接使用することもできます:

```python
output=`dmesg | grep hda`
```

> これは以下のようになります:

```python
output=check_output("dmesg | grep hda", shell=True)
```

### [17.5.6.3. os.system() を置き換える](https://docs.python.jp/3/library/subprocess.html#replacing-os-system)

```python
sts = os.system("mycmd" + " myarg")
# becomes
sts = call("mycmd" + " myarg", shell=True)
```

### 注釈:

> このプログラムは普通シェル経由で呼び出す必要はありません。

> より現実的な例ではこうなるでしょう:

```python
try:
    retcode = call("mycmd" + " myarg", shell=True)
    if retcode < 0:
        print("Child was terminated by signal", -retcode, file=sys.stderr)
    else:
        print("Child returned", retcode, file=sys.stderr)
except OSError as e:
    print("Execution failed:", e, file=sys.stderr)
```

### [17.5.6.4. os.spawn 関数群を置き換える](https://docs.python.jp/3/library/subprocess.html#replacing-the-os-spawn-family)

> P_NOWAIT の例:

```python
pid = os.spawnlp(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg")
==>
pid = Popen(["/bin/mycmd", "myarg"]).pid
```

> P_WAIT の例:

```python
retcode = os.spawnlp(os.P_WAIT, "/bin/mycmd", "mycmd", "myarg")
==>
retcode = call(["/bin/mycmd", "myarg"])
```

> シーケンスを使った例:

```python
os.spawnvp(os.P_NOWAIT, path, args)
==>
Popen([path] + args[1:])
```

> 環境変数を使った例:

```python
os.spawnlpe(os.P_NOWAIT, "/bin/mycmd", "mycmd", "myarg", env)
==>
Popen(["/bin/mycmd", "myarg"], env={"PATH": "/usr/bin"})
```

### [17.5.6.5. os.popen(), os.popen2(), os.popen3() を置き換える](https://docs.python.jp/3/library/subprocess.html#replacing-os-popen-os-popen2-os-popen3)

```python
(child_stdin, child_stdout) = os.popen2(cmd, mode, bufsize)
==>
p = Popen(cmd, shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdin, child_stdout) = (p.stdin, p.stdout)

(child_stdin,
 child_stdout,
 child_stderr) = os.popen3(cmd, mode, bufsize)
==>
p = Popen(cmd, shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True)
(child_stdin,
 child_stdout,
 child_stderr) = (p.stdin, p.stdout, p.stderr)

(child_stdin, child_stdout_and_stderr) = os.popen4(cmd, mode, bufsize)
==>
p = Popen(cmd, shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, stderr=STDOUT, close_fds=True)
(child_stdin, child_stdout_and_stderr) = (p.stdin, p.stdout)
```

> 終了コードハンドリングは以下のように解釈します:

```python
pipe = os.popen(cmd, 'w')
...
rc = pipe.close()
if rc is not None and rc >> 8:
    print("There were some errors")
==>
process = Popen(cmd, stdin=PIPE)
...
process.stdin.close()
if process.wait() != 0:
    print("There were some errors")
```

### [17.5.6.6. popen2 モジュールの関数群を置き換える](https://docs.python.jp/3/library/subprocess.html#replacing-functions-from-the-popen2-module)

> 注釈

> popen2 関数の cmd 引数が文字列の場合、コマンドは /bin/sh によって実行されます。リストの場合、コマンドは直接実行されます。

```python
(child_stdout, child_stdin) = popen2.popen2("somestring", bufsize, mode)
==>
p = Popen("somestring", shell=True, bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdout, child_stdin) = (p.stdout, p.stdin)

(child_stdout, child_stdin) = popen2.popen2(["mycmd", "myarg"], bufsize, mode)
==>
p = Popen(["mycmd", "myarg"], bufsize=bufsize,
          stdin=PIPE, stdout=PIPE, close_fds=True)
(child_stdout, child_stdin) = (p.stdout, p.stdin)
```

> popen2.Popen3 および popen2.Popen4 は以下の点を除けば、基本的に subprocess.Popen と同じです:

* Popen は実行が失敗した場合に例外を送出します。
* capturestderr 引数は stderr 引数に代わりました。
* stdin=PIPE および stdout=PIPE を指定する必要があります。
* popen2 はデフォルトですべてのファイル記述子を閉じます。しかし、全てのプラットフォーム上で、あるいは過去の Python バージョンでこの挙動を保証するためには、 Popen に対して close_fds=True を指定しなければなりません。

## [17.5.7. レガシーなシェル呼び出し関数](https://docs.python.jp/3/library/subprocess.html#legacy-shell-invocation-functions)

> このモジュールでは、以下のような 2.x commands モジュールからのレガシー関数も提供しています。これらの操作は、暗黙的にシステムシェルを起動します。また、セキュリティに関して上述した保証や例外処理一貫性は、これらの関数では有効ではありません。

属性|説明
----|----
subprocess.getstatusoutput(cmd)|Return (exitcode, output) of executing cmd in a shell.
subprocess.getoutput(cmd)|シェル中の cmd を実行して出力 (stdout と stderr) を返します。

## [17.5.8. 注釈](https://docs.python.jp/3/library/subprocess.html#notes)

### [17.5.8.1. Windows における引数シーケンスから文字列への変換](https://docs.python.jp/3/library/subprocess.html#converting-an-argument-sequence-to-a-string-on-windows)

> Windows では、 args シーケンスは以下の (MS C ランタイムで使われる規則に対応する) 規則を使って解析できる文字列に変換されます:

1. 引数は、スペースかタブのどちらかの空白で分けられます。
1. ダブルクオーテーションマークで囲まれた文字列は、空白が含まれていたとしても 1 つの引数として解釈されます。クオートされた文字列は引数に埋め込めます。
1. バックスラッシュに続くダブルクオーテーションマークは、リテラルのダブルクオーテーションマークと解釈されます。
1. バックスラッシュは、ダブルクオーテーションが続かない限り、リテラルとして解釈されます。
1. 複数のバックスラッシュにダブルクオーテーションマークが続くなら、バックスラッシュ 2 つで 1 つのバックスラッシュ文字と解釈されます。バックスラッシュの数が奇数なら、最後のバックスラッシュは規則 3 に従って続くダブルクオーテーションマークをエスケープします。

### 参考

モジュール|概要
----------|----
[shlex](https://docs.python.jp/3/library/shlex.html#module-shlex)|コマンドラインを解析したりエスケープしたりする関数を提供するモジュール。

