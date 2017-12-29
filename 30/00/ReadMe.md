# [18.8. signal — 非同期イベントにハンドラを設定する](https://docs.python.jp/3/library/signal.html)

< [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

> このモジュールでは Python でシグナルハンドラを使うための機構を提供します。

## [18.8.1. 一般的なルール](https://docs.python.jp/3/library/signal.html#general-rules)

> signal.signal() 関数を使って、シグナルを受信した時に実行されるハンドラを定義することができます。 Python は標準でごく少数のシグナルハンドラをインストールしています: SIGPIPE は無視され (したがって、 pipe や socket に対する書き込みで生じたエラーは通常の Python 例外として報告されます)、 SIGINT は KeyboardInterrupt 例外に変換されます。これらはどれも上書きすることができます。

> 特定のシグナルに対するハンドラが一度設定されると、明示的にリセットしないかぎり設定されたままになります (Python は背後の実装系に関係なく BSD 形式のインタフェースをエミュレートします)。例外は SIGCHLD のハンドラで、この場合は背後の実装系の仕様に従います。

### [18.8.1.1. Python のシグナルハンドラの実行](https://docs.python.jp/3/library/signal.html#execution-of-python-signal-handlers)

> Python のシグナルハンドラは、低水準 (C言語) のシグナルハンドラ内で実行されるわけではありません。代わりに、低水準のシグナルハンドラが virtual machine が対応する Python のシグナルハンドラを後から (例えば次の bytecode 命令時に) 実行するようにフラグを立てます:

* It makes little sense to catch synchronous errors like SIGFPE or SIGSEGV that are caused by an invalid operation in C code. Python will return from the signal handler to the C code, which is likely to raise the same signal again, causing Python to apparently hang. From Python 3.3 onwards, you can use the faulthandler module to report on synchronous errors.
* 完全にCで実装された長時間かかる計算 (大きいテキストに対する正規表現のマッチなど) は、どのシグナルを受信しても中断されないまま長時間実行され続ける可能性があります。Python のシグナルハンドラはその計算が終了してから呼び出されます。

### [18.8.1.2. シグナルとスレッド](https://docs.python.jp/3/library/signal.html#signals-and-threads)

> Python のシグナルハンドラは、もしシグナルを受け取ったのが別のスレッドだったとしても、常に Python のメインスレッドで実行されます。このためシグナルをスレッド間通信に使うことはできません。代わりに threading モジュールが提供している同期プリミティブを利用できます。

> また、メインスレッドだけが新しいシグナルハンドラを登録できます。

## [18.8.2. モジュールの内容](https://docs.python.jp/3/library/signal.html#module-contents)

> バージョン 3.5 で変更: signal (SIG*), handler (SIG_DFL, SIG_IGN) and sigmask (SIG_BLOCK, SIG_UNBLOCK, SIG_SETMASK) related constants listed below were turned into enums. getsignal(), pthread_sigmask(), sigpending() and sigwait() functions return human-readable enums.

> 以下に signal モジュールで定義されている変数を示します:

属性|概要
----|----
signal.SIG_DFL|二つある標準シグナル処理オプションのうちの一つです; 単純にシグナルに対する標準の関数を実行します。例えば、ほとんどのシステムでは、 SIGQUIT に対する標準の動作はコアダンプと終了で、 SIGCHLD に対する標準の動作は単にシグナルの無視です。
signal.SIG_IGN|もう一つの標準シグナル処理オプションで、受け取ったシグナルを単に無視します。
SIG*|全てのシグナル番号はシンボル定義されています。例えば、ハングアップシグナルは signal.SIGHUP で定義されています; 変数名は C 言語のプログラムで使われているのと同じ名前で、 <signal.h> にあります。 'signal()' に関する Unix マニュアルページでは、システムで定義されているシグナルを列挙しています (あるシステムではリストは signal(2) に、別のシステムでは signal(7) に列挙されています)。全てのシステムで同じシグナル名のセットを定義しているわけではないので注意してください; このモジュールでは、システムで定義されているシグナル名だけを定義しています。
signal.CTRL_C_EVENT|CTRL+C キーストロークに該当するシグナル。このシグナルは os.kill() でだけ利用できます。 利用できる環境 : Windows.
signal.CTRL_BREAK_EVENT|CTRL+BREAK キーストロークに該当するシグナル。このシグナルは os.kill() でだけ利用できます。 利用できる環境 : Windows.
signal.NSIG|最も大きいシグナル番号に 1 を足した値です。
signal.ITIMER_REAL|実時間でデクリメントするインターバルタイマーです。タイマーが発火したときに SIGALRM を送ります。
signal.ITIMER_VIRTUAL|プロセスの実行時間だけデクリメントするインターバルタイマーです。タイマーが発火したときに SIGVTALRM を送ります。
signal.ITIMER_PROF|プロセスの実行中と、システムがそのプロセスのために実行している時間だけデクリメントするインターバルタイマーです。ITIMER_VIRTUAL と組み合わせて、このタイマーはよくアプリケーションがユーザー空間とカーネル空間で消費した時間のプロファイリングに利用されます。タイマーが発火したときに SIGPROF を送ります。
signal.SIG_BLOCK|pthread_sigmask() の how 引数に渡せる値で、シグナルがブロックされることを意味します。
signal.SIG_UNBLOCK|pthread_sigmask() の how 引数に渡せる値で、シグナルがブロック解除されることを意味します。
signal.SIG_SETMASK|pthread_sigmask() の how 引数に渡せる値で、シグナルが置換されることを意味します。
exception signal.ItimerError|背後の setitimer() または getitimer() 実装からエラーを通知するために送出されます。無効なインタバルタイマーや負の時間が setitimer() に渡された場合、このエラーを予期してください。このエラーは OSError を継承しています。
signal.alarm(time)|time がゼロでない値の場合、この関数は time 秒後頃に SIGALRM をプロセスに送るように要求します。それ以前にスケジュールしたアラームはキャンセルされます (常に一つのアラームしかスケジュールできません)。この場合、戻り値は以前に設定されたアラームシグナルが通知されるまであと何秒だったかを示す値です。 time がゼロの場合、アラームは一切スケジュールされず、現在スケジュールされているアラームがキャンセルされます。戻り値がゼロの場合、現在アラームがスケジュールされていないことを示します。(Unix マニュアルページ alarm(2) を参照してください)。利用できる環境: Unix。
signal.getsignal(signalnum)|シグナル signalnum に対する現在のシグナルハンドラを返します。戻り値は呼び出し可能な Python オブジェクトか、 signal.SIG_IGN、 signal.SIG_DFL、および None といった特殊な値のいずれかです。ここで signal.SIG_IGN は以前そのシグナルが無視されていたことを示し、 signal.SIG_DFL は以前そのシグナルの標準の処理方法が使われていたことを示し、 None はシグナルハンドラがまだ Python によってインストールされていないことを示します。
signal.pause()|シグナルを受け取るまでプロセスを一時停止します; その後、適切なハンドラが呼び出されます。戻り値はありません。Windows では利用できません。(Unix マニュアルページ signal(2) を参照してください。)
signal.pthread_kill(thread_id, signalnum)|Send the signal signalnum to the thread thread_id, another thread in the same process as the caller. The target thread can be executing any code (Python or not). However, if the target thread is executing the Python interpreter, the Python signal handlers will be executed by the main thread. Therefore, the only point of sending a signal to a particular Python thread would be to force a running system call to fail with InterruptedError.
signal.pthread_sigmask(how, mask)|これを呼び出すスレッドにセットされているシグナルマスクを取り出したり変更したりします。シグナルマスクは、呼び出し側のために現在どのシグナルの配送がブロックされているかを示す集合 (set) です。呼び出し前のもとのシグナルマスクを集合として返却します。
signal.setitimer(which, seconds[, interval])|which で指定されたタイマー (signal.ITIMER_REAL, signal.ITIMER_VIRTUAL, signal.ITIMER_PROF のどれか) を、 seconds 秒後と (alarm() と異なり、floatを指定できます)、それから interval 秒間隔で起動するように設定します。 seconds に0を指定すると、which で指定されたタイマーをクリアすることができます。
signal.getitimer(which)|which で指定されたインターバルタイマーの現在の値を返します。利用できる環境: Unix。
signal.set_wakeup_fd(fd)|Set the wakeup file descriptor to fd. When a signal is received, the signal number is written as a single byte into the fd. This can be used by a library to wakeup a poll or select call, allowing the signal to be fully processed.
signal.siginterrupt(signalnum, flag)|システムコールのリスタートの動作を変更します。 flag が False の場合、 signalnum シグナルに中断されたシステムコールは再実行されます。それ以外の場合、システムコールは中断されます。戻り値はありません。利用できる環境: Unix (詳しい情報についてはマニュアルページ siginterrupt(3) を参照してください)。
signal.signal(signalnum, handler)|シグナル signalnum に対するハンドラを関数 handler にします。 handler は二つの引数 (下記参照) を取る呼び出し可能な Python オブジェクトか、 signal.SIG_IGN あるいは signal.SIG_DFL といった特殊な値にすることができます。以前に使われていたシグナルハンドラが返されます (上記の getsignal() の記述を参照してください)。 (Unix マニュアルページ signal(2) を参照してください。)
signal.sigwait(sigset)|sigset 集合で指定されたシグナルのうちどれか一つが届くまで呼び出しスレッドを一時停止します。この関数はそのシグナルを受け取ると (それを保留シグナルリストから取り除いて) そのシグナル番号を返します。
signal.sigwaitinfo(sigset)|Suspend execution of the calling thread until the delivery of one of the signals specified in the signal set sigset. The function accepts the signal and removes it from the pending list of signals. If one of the signals in sigset is already pending for the calling thread, the function will return immediately with information about that signal. The signal handler is not called for the delivered signal. The function raises an InterruptedError if it is interrupted by a signal that is not in sigset.
signal.sigtimedwait(sigset, timeout)|Like sigwaitinfo(), but takes an additional timeout argument specifying a timeout. If timeout is specified as 0, a poll is performed. Returns None if a timeout occurs.


### signal.pthread_sigmask(how, mask)

> この関数の振る舞いは how に依存して以下のようになります。

引数how|説明
-------|----
SIG_BLOCK|mask で指定されるシグナルが現時点のシグナルマスクに追加されます。
SIG_UNBLOCK|mask で指定されるシグナルが現時点のシグナルマスクから取り除かれます。もともとブロックされていないシグナルをブロック解除しようとしても問題ありません。
SIG_SETMASK|シグナルマスク全体を mask としてセットします。

## [18.8.3. 使用例](https://docs.python.jp/3/library/signal.html#example)

> 以下は最小限のプログラム例です。この例では alarm() を使ってファイルを開く処理を待つのに費やす時間を制限します; 例えば、電源の入っていないシリアルデバイスを開こうとすると、通常 os.open() は未定義の期間ハングアップしてしまいますが、この方法はそうした場合に便利です。ここではファイルを開くまで 5 秒間のアラームを設定することで解決しています; ファイルを開く処理が長くかかりすぎると、アラームシグナルが送信され、ハンドラが例外を送出するようになっています。

```python
import signal, os

def handler(signum, frame):
    print('Signal handler called with signal', signum)
    raise OSError("Couldn't open device!")

# Set the signal handler and a 5-second alarm
signal.signal(signal.SIGALRM, handler)
signal.alarm(5)

# This open() may hang indefinitely
fd = os.open('/dev/ttyS0', os.O_RDWR)

signal.alarm(0)          # Disable the alarm
```

