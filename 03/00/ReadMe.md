# [16.16. ctypes — Pythonのための外部関数ライブラリ](https://docs.python.jp/3/library/ctypes.html)

< [16. 汎用オペレーティングシステムサービス](https://docs.python.jp/3/library/allos.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

> ctypes は Python のための外部関数ライブラリです。このライブラリは C と互換性のあるデータ型を提供し、動的リンク/共有ライブラリ内の関数呼び出しを可能にします。動的リンク/共有ライブラリを純粋な Python でラップするために使うことができます。

## [16.16.2. ctypesリファレンス](https://docs.python.jp/3/library/ctypes.html#ctypes-reference)

### [16.16.2.1. 共有ライブラリを見つける](https://docs.python.jp/3/library/ctypes.html#finding-shared-libraries)

> コンパイルされる言語でプログラミングしている場合、共有ライブラリはプログラムをコンパイル/リンクしているときと、そのプログラムが動作しているときにアクセスされます。

> ctypes ライブラリローダーはプログラムが動作しているときのように振る舞い、ランタイムローダーを直接呼び出すのに対し、 find_library() 関数の目的はコンパイラまたはランタイムローダーが行うのと似た方法でライブラリを探し出すことです。 (複数のバージョンの共有ライブラリがあるプラットホームでは、一番最近に見つかったものがロードされます)。

> ctypes.util モジュールはロードするライブラリを決めるのに役立つ関数を提供します。

属性|概要
----|----
ctypes.util.find_library(name)|ライブラリを見つけてパス名を返そうと試みます。 name は lib のような接頭辞、 .so, .dylib のような接尾辞、あるいは、バージョン番号が何も付いていないライブラリの名前です (これは posix リンカのオプション -l に使われている形式です)。 ライブラリが見つからないときは None を返します。

> 厳密な機能はシステムに依存します。

> Linux では、 find_library() はライブラリファイルを見つけるために外部プログラム (/sbin/ldconfig, gcc, objdump と ld) を実行しようとします。ライブラリファイルのファイル名を返します。

> バージョン 3.6 で変更: Linux では、ライブラリを検索する際に、他の方法でライブラリが見つけられない場合は、 LD_LIBRARY_PATH 環境変数の値が使われます

> ここに例があります:

```python
>>> from ctypes.util import find_library
>>> find_library("m")
'libm.so.6'
>>> find_library("c")
'libc.so.6'
>>> find_library("bz2")
'libbz2.so.1.0'
```

> OS X では、 find_library() はライブラリの位置を探すために、予め定義された複数の命名方法とパスを試し、成功すればフルパスを返します。:

```python
>>> from ctypes.util import find_library
>>> find_library("c")
'/usr/lib/libc.dylib'
>>> find_library("m")
'/usr/lib/libm.dylib'
>>> find_library("bz2")
'/usr/lib/libbz2.dylib'
>>> find_library("AGL")
'/System/Library/Frameworks/AGL.framework/AGL'
```

> Windows では、 find_library() はシステムの探索パスに沿って探し、フルパスを返します。しかし、予め定義された命名方法がないため、 find_library("c") のような呼び出しは失敗し、 None を返します。

> ctypes で共有ライブラリをラップする場合、 find_library() を使って実行時にライブラリの場所を特定するのではなく、共有ライブラリの名前を開発時に決めておいて、ラッパーモジュールにハードコードする方が良い かもしれません 。

### [16.16.2.2. 共有ライブラリをロードする](https://docs.python.jp/3/library/ctypes.html#loading-shared-libraries)

> 共有ライブラリを Python プロセスへロードする方法はいくつかあります。一つの方法は下記のクラスの一つをインスタンス化することです:

属性|概要
----|----
class ctypes.CDLL(name, mode=DEFAULT_MODE, handle=None, use_errno=False, use_last_error=False)|このクラスのインスタンスはロードされた共有ライブラリをあらわします。これらのライブラリの関数は標準 C 呼び出し規約を使用し、 int を返すと仮定されます。
class ctypes.OleDLL(name, mode=DEFAULT_MODE, handle=None, use_errno=False, use_last_error=False)|Windows 用: このクラスのインスタンスはロードされた共有ライブラリをあらわします。これらのライブラリの関数は stdcall 呼び出し規約を使用し、 windows 固有の HRESULT コードを返すと仮定されます。 HRESULT 値には関数呼び出しが失敗したのか成功したのかを特定する情報とともに、補足のエラーコードが含まれます。戻り値が失敗を知らせたならば、 OSError が自動的に送出されます。
class ctypes.WinDLL(name, mode=DEFAULT_MODE, handle=None, use_errno=False, use_last_error=False)|Windows 用: このクラスのインスタンスはロードされた共有ライブラリをあらわします。これらのライブラリの関数は stdcall 呼び出し規約を使用し、デフォルトでは int を返すと仮定されます。
class ctypes.PyDLL(name, mode=DEFAULT_MODE, handle=None)|Python GIL が関数呼び出しの間解放 されず 、関数実行の後に Python エラーフラグがチェックされるということを除けば、このクラスのインスタンスは CDLL インスタンスのように振る舞います。エラーフラグがセットされた場合、 Python 例外が送出されます。

> これらすべてのクラスは少なくとも一つの引数、すなわちロードする共有ライブラリのパスを渡して呼び出すことでインスタンス化されます。すでにロード済みの共有ライブラリへのハンドルがあるなら、 handle 名前付き引数として渡すことができます。土台となっているプラットフォームの dlopen または LoadLibrary 関数がプロセスへライブラリをロードするために使われ、そのライブラリに対するハンドルを得ます。

> mode パラメータを使うと、ライブラリがどうやってロードされたかを特定できます。 詳細は dlopen(3) マニュアルページを参考にしてください。 Windows では mode は無視されます。 POSIX システムでは RTLD_NOW が常に追加され、設定変更はできません。

> use_errno 変数が真に設定されたとき、システムの errno エラーナンバーに安全にアクセスする ctypes の仕組みが有効化されます。 ctypes はシステムの errno 変数のスレッド限定のコピーを管理します。もし、 use_errno=True の状態で作られた外部関数を呼び出したなら、関数呼び出し前の errno 変数は ctypes のプライベートコピーと置き換えられ、同じことが関数呼び出しの直後にも発生します。

> ctypes.get_errno() 関数は ctypes のプライベートコピーの値を返します。そして、 ctypes.set_errno() 関数は ctypes のプライベートコピーを置き換え、以前の値を返します。

> use_last_error パラメータは、真に設定されたとき、 GetLastError() と SetLastError() Windows API によって管理される Windows エラーコードに対するのと同じ仕組みが有効化されます。 ctypes.get_last_error() と ctypes.set_last_error() は Windows エラーコードの ctypes プライベートコピーを変更したり要求したりするのに使われます。

属性|概要
----|----
ctypes.RTLD_GLOBAL|mode パラメータとして使うフラグ。このフラグが利用できないプラットフォームでは、整数のゼロと定義されています。
ctypes.RTLD_LOCAL|mode パラメータとして使うフラグ。これが利用できないプラットフォームでは、 RTLD_GLOBAL と同様です。
ctypes.DEFAULT_MODE|共有ライブラリをロードするために使われるデフォルトモード。 OSX 10.3 では RTLD_GLOBAL であり、そうでなければ RTLD_LOCAL と同じです。

> これらのクラスのインスタンスには公開メソッドはありません。共有ライブラリからエクスポートされた関数は、属性として、もしくは添字でアクセスできます。属性を通した関数へのアクセスは結果がキャッシュされ、従って繰り返しアクセスされると毎回同じオブジェクトを返すことに注意してください。それとは反対に、添字を通したアクセスは毎回新しいオブジェクトを返します:

```python
>>> libc.time == libc.time
True
>>> libc['time'] == libc['time']
False
```

> 次に述べる公開属性が利用できます。それらの名前はエクスポートされた関数名に衝突しないように下線で始まります。:

属性|概要
----|----
PyDLL._handle|ライブラリへのアクセスに用いられるシステムハンドル。
PyDLL._name|コンストラクタに渡されたライブラリの名前。

> 共有ライブラリは (LibraryLoader クラスのインスタンスである) 前もって作られたオブジェクトの一つを使うことによってロードすることもできます。それらの LoadLibrary() メソッドを呼び出すか、ローダーインスタンスの属性としてライブラリを取り出すかのどちらかによりロードします。

属性|概要
----|----
class ctypes.LibraryLoader(dlltype)|共有ライブラリをロードするクラス。 dlltype は CDLL 、 PyDLL 、 WinDLL もしくは OleDLL 型の一つであるべきです。
    LoadLibrary(name)|    共有ライブラリをプロセスへロードし、それを返します。このメソッドはライブラリの新しいインスタンスを常に返します。

> これらの前もって作られたライブラリローダーを利用することができます。:

属性|概要
----|----
ctypes.cdll|CDLL インスタンスを作ります。
ctypes.windll|Windows 用: WinDLL インスタンスを作ります。
ctypes.oledll|Windows 用: OleDLL インスタンスを作ります。
ctypes.pydll|PyDLL インスタンスを作ります。C Python api に直接アクセスするために、すぐに使用できる Python 共有ライブラリオブジェクトが次のように用意されています。
ctypes.pythonapi|属性として Python C api 関数を公開する PyDLL のインスタンス。これらすべての関数は C int を返すと仮定されますが、もちろん常に正しいとは限りません。そのため、これらの関数を使うためには正しい restype 属性を代入しなければなりません。

### [16.16.2.3. 外部関数](https://docs.python.jp/3/library/ctypes.html#foreign-functions)

> 前節で説明した通り、外部関数はロードされた共有ライブラリの属性としてアクセスできます。デフォルトではこの方法で作成された関数オブジェクトはどんな数の引数でも受け取り、引数としてどんな ctypes データのインスタンスをも受け取り、そして、ライブラリローダーが指定したデフォルトの結果の値の型を返します。関数オブジェクトはプライベートクラスのインスタンスです。:

属性|概要
----|----
class ctypes._FuncPtr|C の呼び出し可能外部関数のためのベースクラス。
restype|外部関数の結果の型を指定するために ctypes 型を代入する。何も返さない関数を表す void に対しては None を使います。
argtypes|関数が受け取る引数の型を指定するために ctypes 型のタプルを代入します。stdcall 呼び出し規約を使う関数はこのタプルの長さと同じ数の引数で呼び出されます。C 呼び出し規約を使う関数は、追加の不特定の引数も取ります。
errcheck|Python 関数または他の呼び出し可能オブジェクトをこの属性に代入します。呼び出し可能オブジェクトは三つ以上の引数とともに呼び出されます。
exception ctypes.ArgumentError|この例外は外部関数呼び出しが渡された引数を変換できなかったときに送出されます。

### [16.16.2.4. 関数プロトタイプ](https://docs.python.jp/3/library/ctypes.html#function-prototypes)

> 外部関数は関数プロトタイプをインスタンス化することによって作成されます。関数プロトタイプは C の関数プロトタイプと似ています。実装を定義せずに、関数 (戻り値、引数の型、呼び出し規約) を記述します。ファクトリ関数は関数に要求する戻り値の型と引数の型とともに呼び出されます。

属性|概要
----|----
ctypes.CFUNCTYPE(restype, *argtypes, use_errno=False, use_last_error=False)|返された関数プロトタイプは標準 C 呼び出し規約をつかう関数を作成します。関数は呼び出されている間 GIL を解放します。 use_errno が真に設定されれば、呼び出しの前後で System 変数 errno の ctypesプライベートコピーは本当の errno の値と交換されます。 use_last_error も Windows エラーコードに対するのと同様です。
ctypes.WINFUNCTYPE(restype, *argtypes, use_errno=False, use_last_error=False)|Windows のみ: 返された関数プロトタイプは stdcall 呼び出し規約を使う関数を作成します。ただし、 WINFUNCTYPE() が CFUNCTYPE() と同じである Windows CE を除きます。関数は呼び出されている間 GIL を解放します。 use_errno と use_last_error は前述と同じ意味を持ちます。
ctypes.PYFUNCTYPE(restype, *argtypes)|返された関数プロトタイプは Python 呼び出し規約を使う関数を作成します。関数は呼び出されている間 GIL を解放 しません。

> ファクトリ関数によって作られた関数プロトタイプは呼び出しのパラメータの型と数に依存した別の方法でインスタンス化することができます。 :

属性|概要
----|----
prototype(address)|指定されたアドレス(整数でなくてはなりません)の外部関数を返します。
prototype(callable)|Python の callable から C の呼び出し可能関数(コールバック関数) を作成します。
prototype(func_spec[, paramflags])|共有ライブラリがエクスポートしている外部関数を返します。 func_spec は 2 要素タプル (name_or_ordinal, library) でなければなりません。第一要素はエクスポートされた関数の名前である文字列、またはエクスポートされた関数の序数である小さい整数です。第二要素は共有ライブラリインスタンスです。
prototype(vtbl_index, name[, paramflags[, iid]])|COM メソッドを呼び出す外部関数を返します。 vtbl_index は仮想関数テーブルのインデックスで、非負の小さい整数です。 name は COM メソッドの名前です。 iid はオプションのインターフェイス識別子へのポインタで、拡張されたエラー情報の提供のために使われます。 COM メソッドは特殊な呼び出し規約を用います。このメソッドは argtypes タプルに指定されたパラメータに加えて、第一引数として COM インターフェイスへのポインタを必要とします。

> オプションの paramflags パラメータは上述した機能より多機能な外部関数ラッパーを作成します。

> paramflags は argtypes と同じ長さのタプルでなければなりません。

> このタプルの個々の要素はパラメータについてのより詳細な情報を持ち、 1 、 2 もしくは 3 要素を含むタプルでなければなりません。

>   第一要素はパラメータについてのフラグの組み合わせを含んだ整数です。

整数|意味
----|----
1|入力パラメータを関数に指定します。
2|出力パラメータ。外部関数が値を書き込みます。
4|デフォルトで整数ゼロになる入力パラメータ。

> オプションの第二要素はパラメータ名の文字列です。これが指定された場合は、外部関数を名前付きパラメータで呼び出すことができます。

> オプションの第三要素はこのパラメータのデフォルト値です。

> この例では、デフォルトパラメータと名前付き引数をサポートするために Windows の MessageBoxW 関数をラップする方法を示します。 windows のヘッダファイルの C の宣言は次の通りです:


```c
WINUSERAPI int WINAPI
MessageBoxW(
    HWND hWnd,
    LPCWSTR lpText,
    LPCWSTR lpCaption,
    UINT uType);
```

ctypes を使ってラップします。:

```python
>>> from ctypes import c_int, WINFUNCTYPE, windll
>>> from ctypes.wintypes import HWND, LPCWSTR, UINT
>>> prototype = WINFUNCTYPE(c_int, HWND, LPCWSTR, LPCWSTR, UINT)
>>> paramflags = (1, "hwnd", 0), (1, "text", "Hi"), (1, "caption", "Hello from ctypes"), (1, "flags", 0)
>>> MessageBox = prototype(("MessageBoxW", windll.user32), paramflags)
```

> これで外部関数の MessageBox を次のような方法で呼び出すことができるようになりました:

```python
>>> MessageBox()
>>> MessageBox(text="Spam, spam, spam")
>>> MessageBox(flags=2, text="foo bar")
```

二番目の例は出力パラメータについて説明します。 win32 の GetWindowRect 関数は、指定されたウィンドウの大きさを呼び出し側が与える RECT 構造体へコピーすることで取り出します。 C の宣言はこうです。:

```c
WINUSERAPI BOOL WINAPI
GetWindowRect(
     HWND hWnd,
     LPRECT lpRect);
```

> ctypes を使ってラップします。:

```python
>>> from ctypes import POINTER, WINFUNCTYPE, windll, WinError
>>> from ctypes.wintypes import BOOL, HWND, RECT
>>> prototype = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
>>> paramflags = (1, "hwnd"), (2, "lprect")
>>> GetWindowRect = prototype(("GetWindowRect", windll.user32), paramflags)
```

> 出力パラメータを持つ関数は、単一のパラメータがある場合にはその出力パラメータ値を、複数のパラメータがある場合には出力パラメータ値が入ったタプルを、それぞれ自動的に返します。そのため、GetWindowRect 関数は呼び出されると RECT インスタンスを返します。

> さらに出力処理やエラーチェックを行うために、出力パラメータを errcheck プロトコルと組み合わせることができます。 win32 GetWindowRect api 関数は成功したか失敗したかを知らせるために BOOL を返します。そのため、この関数はエラーチェックを行って、 api 呼び出しが失敗した場合に例外を送出させることができます。:

```python
>>> def errcheck(result, func, args):
...     if not result:
...         raise WinError()
...     return args
...
>>> GetWindowRect.errcheck = errcheck
```

> errcheck 関数が受け取った引数タプルを変更なしに返した場合、 ctypes は出力パラメータに対する通常の処理を続けます。 RECT インスタンスの代わりに window 座標のタプルを返すには、関数のフィールドを取り出し、代わりにそれらを返すことができます。この場合、通常処理は行われなくなります:

```python
>>> def errcheck(result, func, args):
...     if not result:
...         raise WinError()
...     rc = args[1]
...     return rc.left, rc.top, rc.bottom, rc.right
...
>>> GetWindowRect.errcheck = errcheck
```

### [16.16.2.5. ユーティリティー関数](https://docs.python.jp/3/library/ctypes.html#utility-functions)

属性|概要
----|----
ctypes.addressof(obj)|メモリバッファのアドレスを示す整数を返します。 obj は ctypes 型のインスタンスでなければなりません。
ctypes.alignment(obj_or_type)|ctypes 型のアライメントの必要条件を返します。 obj_or_type は ctypes 型またはインスタンスでなければなりません。
ctypes.byref(obj[, offset])|obj (ctypes 型のインスタンスでなければならない) への軽量ポインタを返します。 offset はデフォルトでは 0 で、内部ポインターへ加算される整数です。byref(obj, offset) は、 C コードとしては、以下のようにみなされます。: `(((char *)&obj) + offset)` 返されるオブジェクトは外部関数呼び出しのパラメータとしてのみ使用できます。pointer(obj) と似たふるまいをしますが、作成が非常に速く行えます。
ctypes.cast(obj, type)|この関数は C のキャスト演算子に似ています。obj と同じメモリブロックを指している type の新しいインスタンスを返します。type はポインタ型でなければならず、obj はポインタとして解釈できるオブジェクトでなければなりません。
ctypes.create_string_buffer(init_or_size, size=None)|この関数は変更可能な文字バッファを作成します。返されるオブジェクトは c_char の ctypes 配列です。
ctypes.create_unicode_buffer(init_or_size, size=None)|この関数は変更可能な Unicode 文字バッファを作成します。返されるオブジェクトは c_wchar の ctypes 配列です。
ctypes.DllCanUnloadNow()|Windows 用: この関数は ctypes をつかってインプロセス COM サーバーを実装できるようにするためのフックです。_ctypes 拡張 dll がエクスポートしている DllCanUnloadNow 関数から呼び出されます。
ctypes.DllGetClassObject()|Windows 用: この関数は ctypes をつかってインプロセス COM サーバーを実装できるようにするためのフックです。_ctypes 拡張 dll がエクスポートしている DllGetClassObject 関数から呼び出されます。
ctypes.util.find_library(name)|ライブラリを検索し、パス名を返します。 name は lib のような接頭辞、 .so や .dylib のような接尾辞、そして、バージョンナンバーを除くライブラリ名です (これは posix のリンカーオプション -l で使われる書式です) 。もしライブラリが見つからなければ、 None を返します。
ctypes.util.find_msvcrt()|Windows 用: Python と拡張モジュールで使われる VC ランタイムライブラリのファイル名を返します。もしライブラリ名が同定できなければ、 None を返します。
ctypes.FormatError([code])|Windows 用: エラーコード code の説明文を返します。エラーコードが指定されない場合は、 Windows api 関数 GetLastError を呼び出して、もっとも新しいエラーコードが使われます。
ctypes.GetLastError()|Windows 用: 呼び出し側のスレッド内で Windows によって設定された最新のエラーコードを返します。この関数は Windows の GetLastError() 関数を直接実行します。 ctypes のプライベートなエラーコードのコピーを返したりはしません。
ctypes.get_errno()|システムの errno 変数の、スレッドローカルなプライベートコピーを返します。
ctypes.get_last_error()|Windows 用: システムの LastError 変数の、スレッドローカルなプライベートコピーを返します。
ctypes.memmove(dst, src, count)|標準 C の memmove ライブラリ関数と同じものです。: count バイトを src から dst へコピーします。 dst と src はポインタへ変換可能な整数または ctypes インスタンスでなければなりません。
ctypes.memset(dst, c, count)|標準 C の memset ライブラリ関数と同じものです。: アドレス dst のメモリブロックを値 c を count バイト分書き込みます。 dst はアドレスを指定する整数または ctypes インスタンスである必要があります。
ctypes.POINTER(type)|このファクトリ関数は新しい ctypes ポインタ型を作成して返します。ポインタ型はキャッシュされ、内部で再利用されます。したがって、この関数を繰り返し呼び出してもコストは小さいです。type は ctypes 型でなければなりません。
ctypes.pointer(obj)|この関数は obj を指す新しいポインタインスタンスを作成します。戻り値は POINTER(type(obj)) 型のオブジェクトです。
ctypes.resize(obj, size)|この関数は obj の内部メモリバッファのサイズを変更します。 obj は ctypes 型のインスタンスでなければなりません。バッファを sizeof(type(obj)) で与えられるオブジェクト型の本来のサイズより小さくすることはできませんが、バッファを拡大することはできます。
ctypes.set_errno(value)|システム変数 errno の、呼び出し元スレッドでの ctypes のプライベートコピーの現在値を value に設定し、前の値を返します。
ctypes.set_last_error(value)|Windows 用: システム変数 LastError の、呼び出し元スレッドでの ctypes のプライベートコピーの現在値を value に設定し、前の値を返します。
ctypes.sizeof(obj_or_type)|ctypes の型やインスタンスのメモリバッファのサイズをバイト数で返します。C の sizeof 演算子と同様の動きをします。
ctypes.string_at(address, size=-1)|この関数はメモリアドレス address から始まる C 文字列を返します。size が指定された場合はサイズとして使われます。指定されなければ、文字列がゼロ終端されていると仮定します。
ctypes.WinError(code=None, descr=None)|Windows 用: この関数はおそらく ctypes の中で最悪の名前でしょう。これは OSError のインスタンスを作成します。 code が指定されていなかった場合、エラーコードを判別するために GetLastError が呼び出されます。 descr が指定されていなかった場合、エラーの説明文を得るために FormatError() が呼び出されます。
ctypes.wstring_at(address, size=-1)|この関数は文字列としてメモリアドレス address から始まるワイドキャラクタ文字列を返します。size が指定されたならば、文字列の文字数として使われます。指定されなければ、文字列がゼロ終端されていると仮定します。

### [16.16.2.6. データ型](https://docs.python.jp/3/library/ctypes.html#data-types)

属性|概要
----|----
class ctypes._CData|この非公開クラスはすべての ctypes データ型の共通のベースクラスです。他のことはさておき、すべての ctypes 型インスタンスは C 互換データを保持するメモリブロックを内部に持ちます。このメモリブロックのアドレスは addressof() ヘルパー関数が返します。別のインスタンス変数が _objects として公開されます。これはメモリブロックがポインタを含む場合に存続し続ける必要のある他の Python オブジェクトを含んでいます。
from_buffer(source[, offset])|このメソッドは source オブジェクトのバッファを共有する ctypes のインスタンスを返します。 source オブジェクトは書き込み可能バッファインターフェースをサポートしている必要があります。オプションの offset 引数では source バッファのオフセットをバイト単位で指定します。デフォルトではゼロです。もし source バッファが十分に大きくなければ、 ValueError が送出されます。
from_buffer_copy(source[, offset])|このメソッドは source オブジェクトの読み出し可能バッファをコピーすることで、ctypes のインスタンスを生成します。オプションの offset 引数では source バッファのオフセットをバイト単位で指定します。デフォルトではゼロです。もし source バッファが十分に大きくなければ、 ValueError が送出されます。
from_address(address)|このメソッドは address で指定されたメモリを使って ctypes 型のインスタンスを返します。 address は整数でなければなりません。
from_param(obj)|このメソッドは obj を ctypes 型に適合させます。外部関数の argtypes タプルに、その型があるとき、外部関数呼び出しで実際に使われるオブジェクトと共に呼び出されます。
in_dll(library, name)|このメソッドは、共有ライブラリによってエクスポートされた ctypes 型のインスタンスを返します。 name はエクスポートされたデータの名前で、 library はロードされた共有ライブラリです。

> ctypes データ型共通のインスタンス変数:

属性|概要
----|----
_b_base_|ctypes 型データのインスタンスは、それ自身のメモリブロックを持たず、基底オブジェクトのメモリブロックの一部を共有することがあります。 _b_base_ 読み出し専用属性は、メモリブロックを保持する ctypes の基底オブジェクトです。
_b_needsfree_|この読み出し専用の変数は、 ctypes データインスタンスが、それ自身に割り当てられたメモリブロックを持つとき true になります。それ以外の場合は false になります。
_objects|このメンバは None 、または、メモリブロックの内容が正しく保つために、生存させておかなくてはならない Python オブジェクトを持つディクショナリです。このオブジェクトはデバッグでのみ使われます。決してディクショナリの内容を変更しないで下さい。

### [16.16.2.7. 基本データ型](https://docs.python.jp/3/library/ctypes.html#ctypes-fundamental-data-types-2)

属性|概要
----|----
class ctypes._SimpleCData|この非公開クラスは、全ての基本的な ctypes データ型の基底クラスです。これは基本的な ctypes データ型に共通の属性を持っているので、ここで触れておきます。 _SimpleCData は _CData の子クラスなので、そのメソッドと属性を継承しています。ポインタでないかポインタを含まない ctypes データ型は、現在は pickle 化できます。
value|この属性は、インスタンスの実際の値を持ちます。整数型とポインタ型に対しては整数型、文字型に対しては一文字のバイト列オブジェクト、文字へのポインタに対しては Python のバイト列オブジェクトもしくは文字列となります。

> 基本データ型は、外部関数呼び出しの結果として返されたときや、例えば構造体のフィールドメンバーや配列要素を取り出すときに、ネイティブの Python 型へ透過的に変換されます。言い換えると、外部関数が c_char_p の restype を持つ場合は、 c_char_p インスタンスでは なく 常に Python バイト列オブジェクトを受け取ることでしょう。

> 基本データ型のサブクラスはこの振る舞いを継承 しません 。したがって、外部関数の restype が c_void_p のサブクラスならば、関数呼び出しからこのサブクラスのインスタンスを受け取ります。もちろん、 value 属性にアクセスしてポインタの値を得ることができます。

> これらが基本 ctypes データ型です:

属性|概要
----|----
class ctypes.c_byte|C の signed char データ型を表し、小整数として値を解釈します。コンストラクタはオプションの整数初期化子を受け取ります。オーバーフローのチェックは行われません。
class ctypes.c_char|C char データ型を表し、単一の文字として値を解釈します。コンストラクタはオプションの文字列初期化子を受け取り、その文字列の長さちょうど一文字である必要があります。
class ctypes.c_char_p|C char * データ型を表し、ゼロ終端文字列へのポインタでなければなりません。バイナリデータを指す可能性のある一般的なポインタに対しては POINTER(c_char) を使わなければなりません。コンストラクタは整数のアドレスもしくはバイト列オブジェクトを受け取ります。
class ctypes.c_double|C double データ型を表します。コンストラクタはオプションの浮動小数点数初期化子を受け取ります。
class ctypes.c_longdouble|C long double データ型を表します。コンストラクタはオプションで浮動小数点数初期化子を受け取ります。 sizeof(long double) == sizeof(double) であるプラットフォームでは c_double の別名です。
class ctypes.c_float|C float データ型を表します。コンストラクタはオプションの浮動小数点数初期化子を受け取ります。
class ctypes.c_int|C signed int データ型を表します。コンストラクタはオプションの整数初期化子を受け取ります。オーバーフローのチェックは行われません。 sizeof(int) == sizeof(long) であるプラットフォームでは、 c_long の別名です。
class ctypes.c_int8|C 8-bit signed int データ型を表します。たいていは、 c_byte の別名です。
class ctypes.c_int16|C 16-bit signed int データ型を表します。たいていは、 c_short の別名です。
class ctypes.c_int32|C 32-bit signed int データ型を表します。たいていは、 c_int の別名です。
class ctypes.c_int64|C 64-bit signed int データ型を表します。たいていは、 c_longlong の別名です。
class ctypes.c_long|C signed long データ型を表します。コンストラクタはオプションの整数初期化子を受け取ります。オーバーフローのチェックは行われません。
class ctypes.c_longlong|C signed long long データ型を表します。コンストラクタはオプションの整数初期化子を受け取ります。オーバーフローのチェックは行われません。
class ctypes.c_short|C signed short データ型を表します。コンストラクタはオプションの整数初期化子を受け取ります。オーバーフローのチェックは行われません。
class ctypes.c_size_t|C size_t データ型を表します。
class ctypes.c_ssize_t|C ssize_t データ型を表します。
class ctypes.c_ubyte|C の unsigned char データ型を表し、小さな整数として値を解釈します。コンストラクタはオプションの整数初期化子を受け取ります; オーバーフローのチェックは行われません。
class ctypes.c_uint|C の unsigned int データ型を表します。コンストラクタはオプションの整数初期化子を受け取ります; オーバーフローのチェックは行われません。これは、 sizeof(int) == sizeof(long) であるプラットフォームでは c_ulong の別名です。
class ctypes.c_uint8|C 8-bit unsigned int データ型を表します。たいていは、 c_ubyte の別名です。
class ctypes.c_uint16|C 16-bit unsigned int データ型を表します。たいていは、 c_ushort の別名です。
class ctypes.c_uint32|C 32-bit unsigned int データ型を表します。たいていは、 c_uint の別名です。
class ctypes.c_uint64|C 64-bit unsigned int データ型を表します。たいていは、 c_ulonglong の別名です。
class ctypes.c_ulong|C unsigned long データ型を表します。コンストラクタはオプションの整数初期化子を受け取ります。オーバーフローのチェックは行われません。
class ctypes.c_ulonglong|C unsigned long long データ型を表します。コンストラクタはオプションの整数初期化子を受け取ります。オーバーフローのチェックは行われません。
class ctypes.c_ushort|C unsigned short データ型を表します。コンストラクタはオプションの整数初期化子を受け取ります。オーバーフローのチェックは行われません。
class ctypes.c_void_p|C void * データ型を表します。値は整数として表されます。コンストラクタはオプションの整数初期化子を受け取ります。
class ctypes.c_wchar|C wchar_t データ型を表し、値は Unicode 文字列の単一の文字として解釈されます。コンストラクタはオプションの文字列初期化子を受け取り、その文字列の長さはちょうど一文字である必要があります。
class ctypes.c_wchar_p|C wchar_t * データ型を表し、ゼロ終端ワイド文字列へのポインタでなければなりません。コンストラクタは整数のアドレスもしくは文字列を受け取ります。
class ctypes.c_bool|C の bool データ型 (より正確には、 C99 以降の _Bool) を表します。 True または False の値を持ち、コンストラクタは真偽値と解釈できるオブジェクトを受け取ります。
class ctypes.HRESULT|Windows用: HRESULT 値を表し、関数またはメソッド呼び出しに対する成功またはエラーの情報を含んでいます。
class ctypes.py_object|C PyObject * データ型を表します。引数なしでこれを呼び出すと NULL PyObject * ポインタを作成します。

> ctypes.wintypes モジュールは他の Windows 固有のデータ型を提供します。例えば、 HWND, WPARAM, DWORD です。 MSG や RECT のような有用な構造体も定義されています。

### [16.16.2.8. 構造化データ型](https://docs.python.jp/3/library/ctypes.html#structured-data-types)

属性|概要
----|----
class ctypes.Union(*args, **kw)|ネイティブのバイトオーダーでの共用体のための抽象ベースクラス。
class ctypes.BigEndianStructure(*args, **kw)|ビックエンディアン バイトオーダーでの構造体のための抽象ベースクラス。
class ctypes.LittleEndianStructure(*args, **kw)|リトルエンディアン バイトオーダーでの構造体のための抽象ベースクラス。
class ctypes.Structure(*args, **kw)|ネイティブ のバイトオーダーでの構造体のための抽象ベースクラス。
_fields_|構造体のフィールドを定義するシーケンス。要素は2要素タプルか3要素タプルでなければなりません。第一要素はフィールドの名前です。第二要素はフィールドの型を指定します。それはどんな ctypes データ型でも構いません。
_pack_|インスタンスの構造体フィールドのアライメントを上書きできるようにするオブションの小整数。 _pack_ は _fields_ が代入されたときすでに定義されていなければなりません。そうでなければ、何の効果もありません。
_anonymous_|無名 (匿名) フィールドの名前が並べあげられたオプションのシーケンス。 _fields_ が代入されたとき、 _anonymous_ がすでに定義されていなければなりません。そうでなければ、何ら影響はありません。

### [16.16.2.9. 配列とポインタ](https://docs.python.jp/3/library/ctypes.html#arrays-and-pointers)

属性|概要
----|----
class ctypes.Array(*args)|配列のための抽象基底クラスです。
_length_|配列の要素数を指定する正の整数。範囲外の添え字を指定すると、 IndexError が送出されます。len() がこの整数を返します。
_type_|配列内の各要素の型を指定します。
class ctypes._Pointer|ポインタのためのプライベートな抽象基底クラスです。
_type_|ポイント先の型を指定します。
contents|ポインタが指すオブジェクトを返します。この属性に割り当てると、ポインタが割り当てられたオブジェクトを指すようになります。

