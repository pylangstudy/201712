# [16.16. ctypes — Pythonのための外部関数ライブラリ](https://docs.python.jp/3/library/ctypes.html)

< [16. 汎用オペレーティングシステムサービス](https://docs.python.jp/3/library/allos.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

> ctypes は Python のための外部関数ライブラリです。このライブラリは C と互換性のあるデータ型を提供し、動的リンク/共有ライブラリ内の関数呼び出しを可能にします。動的リンク/共有ライブラリを純粋な Python でラップするために使うことができます。

## [16.16.1. ctypesチュートリアル](https://docs.python.jp/3/library/ctypes.html#ctypes-tutorial)

> 注意: このチュートリアルのコードサンプルは動作確認のために doctest を使います。コードサンプルの中には Linux、 Windows、あるいは Mac OS X 上で異なる動作をするものがあるため、サンプルのコメントに doctest 命令を入れてあります。

> 注意: いくつかのコードサンプルで ctypes の c_int 型を参照しています。 sizeof(long) == sizeof(int) であるようなプラットフォームでは、この型は c_long のエイリアスです。そのため、 c_int 型を想定しているときに c_long が表示されたとしても、混乱しないようにしてください — 実際には同じ型なのです。

## [16.16.1.1. 動的リンクライブラリをロードする](https://docs.python.jp/3/library/ctypes.html#loading-dynamic-link-libraries)

> 動的リンクライブラリをロードするために、 ctypes は cdll をエクスポートします。 Windows では windll と oledll オブジェクトをエクスポートします。

> これらのオブジェクトの属性としてライブラリにアクセスすることでライブラリをロードします。 cdll は、標準 cdecl 呼び出し規約を用いて関数をエクスポートしているライブラリをロードします。それに対して、 windll ライブラリは stdcall 呼び出し規約を用いる関数を呼び出します。 oledll も stdcall 呼び出し規約を使いますが、関数が Windows HRESULT エラーコードを返すことを想定しています。このエラーコードは関数呼び出しが失敗したとき、 OSError 例外を自動的に送出させるために使われます。

> バージョン 3.3 で変更: Windows エラーは以前は WindowsError を送出していましたが、これは現在では OSError の別名になっています。

> Windows用の例ですが、 msvcrt はほとんどの標準 C 関数が含まれている MS 標準 C ライブラリであり、 cdecl 呼び出し規約を使うことに注意してください:

```python
>>> from ctypes import *
>>> print(windll.kernel32)  
<WinDLL 'kernel32', handle ... at ...>
>>> print(cdll.msvcrt)      
<CDLL 'msvcrt', handle ... at ...>
>>> libc = cdll.msvcrt      
```

> Windows では通常の .dll ファイル拡張子を自動的に追加します。

### 注釈

> cdll.msvcrt 経由で標準 C ライブラリにアクセスすると、Python が使用しているライブラリとは互換性のない可能性のある、古いバージョンのライブラリが使用されます。可能な場合には、ネイティブ Python の機能を使用するか、msvcrt モジュールをインポートして使用してください。

> Linux ではライブラリをロードするために拡張子を 含む ファイル名を指定する必要があるので、ロードしたライブラリに対する属性アクセスはできません。 dll ローダーの LoadLibrary() メソッドを使うか、コンストラクタを呼び出して CDLL のインスタンスを作ることでライブラリをロードするかのどちらかを行わなければなりません:

```python
>>> cdll.LoadLibrary("libc.so.6")  
<CDLL 'libc.so.6', handle ... at ...>
>>> libc = CDLL("libc.so.6")       
>>> libc                           
<CDLL 'libc.so.6', handle ... at ...>
>>>
```

## [16.16.1.2. ロードしたdllから関数にアクセスする](https://docs.python.jp/3/library/ctypes.html#accessing-functions-from-loaded-dlls)

dll オブジェクトの属性として関数にアクセスします:

```python
>>> from ctypes import *
>>> libc.printf
<_FuncPtr object at 0x...>
>>> print(windll.kernel32.GetModuleHandleA)  
<_FuncPtr object at 0x...>
>>> print(windll.kernel32.MyOwnFunction)     
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "ctypes.py", line 239, in __getattr__
    func = _StdcallFuncPtr(name, self)
AttributeError: function 'MyOwnFunction' not found
```

> kernel32 や user32 のような win32 システム dll は、多くの場合関数の UNICODE バージョンに加えて ANSI バージョンもエクスポートすることに注意してください。 UNICODE バージョンは後ろに W が付いた名前でエクスポートされ、 ANSI バージョンは A が付いた名前でエクスポートされます。与えられたモジュールの モジュールハンドル を返す win32 GetModuleHandle 関数は次のような C プロトタイプを持ちます。 UNICODE バージョンが定義されているかどうかにより GetModuleHandle としてどちらか一つを公開するためにマクロが使われます:


```c
/* ANSI version */
HMODULE GetModuleHandleA(LPCSTR lpModuleName);
/* UNICODE version */
HMODULE GetModuleHandleW(LPCWSTR lpModuleName);
```

> windll は魔法を使ってどちらか一つを選ぶようなことはしません。GetModuleHandleA もしくは GetModuleHandleW を明示的に指定して必要とするバージョンにアクセスし、バイト列か文字列を使ってそれぞれ呼び出さなければなりません。

> 時には、 dll が関数を "??2@YAPAXI@Z" のような Python 識別子として有効でない名前でエクスポートすることがあります。このような場合に関数を取り出すには、 getattr() を使わなければなりません。:

```python
>>> getattr(cdll.msvcrt, "??2@YAPAXI@Z")  
<_FuncPtr object at 0x...>
```

> Windows では、名前ではなく序数によって関数をエクスポートする dll もあります。こうした関数には序数を使って dll オブジェクトにインデックス指定することでアクセスします:

```python
>>> cdll.kernel32[1]  
<_FuncPtr object at 0x...>
>>> cdll.kernel32[0]  
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "ctypes.py", line 310, in __getitem__
    func = _StdcallFuncPtr(name, self)
AttributeError: function ordinal 0 not found
```

## [16.16.1.3. 関数を呼び出す](https://docs.python.jp/3/library/ctypes.html#calling-functions)

> これらの関数は他の Python 呼び出し可能オブジェクトと同じように呼び出すことができます。この例では time() 関数 (Unixエポックからのシステム時間を秒単位で返す) と、 GetModuleHandleA() 関数 (win32モジュールハンドルを返す) を使います。

> この例は両方の関数を NULL ポインタとともに呼び出します (None を NULL ポインタとして使う必要があります):

```python
>>> print(libc.time(None))  
1150640792
>>> print(hex(windll.kernel32.GetModuleHandleA(None)))  
0x1d000000
```

> 注釈

> 不正な数の引数が渡されたことを検知した場合、 ctypes は関数を呼び出した後に ValueError を送出することがあります。 この動作には依存するべきではありません。 この動作は 3.6.2 で非推奨であり、 3.7 で削除予定です。

> cdecl 呼び出し規約を使って stdcall 関数を呼び出したときには、 ValueError が送出されます。逆の場合も同様です:

```python
>>> cdll.kernel32.GetModuleHandleA(None)  
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: Procedure probably called with not enough arguments (4 bytes missing)

>>> windll.msvcrt.printf(b"spam")  
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: Procedure probably called with too many arguments (4 bytes in excess)
```

> 正しい呼び出し規約を知るためには、呼び出したい関数についての C ヘッダファイルもしくはドキュメントを見なければなりません。

> Windows では、関数が無効な引数とともに呼び出された場合の一般保護例外によるクラッシュを防ぐために、 ctypes は win32 構造化例外処理を使います:

```python
>>> windll.kernel32.GetModuleHandleA(32)  
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: exception: access violation reading 0x00000020
```

> しかしそれでも他に ctypes で Python がクラッシュする状況はあるので、どちらにせよ気を配るべきです。クラッシュのデバッグには、 faulthandler モジュールが役に立つ場合があります (例えば、誤った C ライブラリ呼び出しによって引き起こされたセグメンテーション違反) 。

> None 、整数、バイト列オブジェクトおよび (Unicode) 文字列だけが、こうした関数呼び出しにおいてパラメータとして直接使えるネイティブの Python オブジェクトです。 None は C の NULL ポインタとして渡され、バイト文字列とユニコード文字列はそのデータを含むメモリブロックへのポインタ (char * または wchar_t *) として渡されます。 Python 整数はプラットホームのデフォルトの C int 型として渡され、その値は C int 型に合うようにマスクされます。

> 他のパラメータ型をもつ関数呼び出しに移る前に、 ctypes データ型についてさらに学ぶ必要があります。

## [16.16.1.4. 基本データ型](https://docs.python.jp/3/library/ctypes.html#fundamental-data-types)

> ctypes ではいくつもの C 互換のプリミティブなデータ型を定義しています:

ctypes の型|C の型|Python の型
-----------|------|-----------
c_bool|_Bool|bool (1)
c_char|char|1文字のバイト列オブジェクト
c_wchar|wchar_t|1文字の文字列
c_byte|char|int
c_ubyte|unsigned char|int
c_short|short|int
c_ushort|unsigned short|int
c_int|int|int
c_uint|unsigned int|int
c_long|long|int
c_ulong|unsigned long|int
c_longlong|__int64 または long long|int
c_ulonglong|unsigned __int64 または unsigned long long|int
c_size_t|size_t|int
c_ssize_t|ssize_t または Py_ssize_t|int
c_float|float|浮動小数点数
c_double|double|浮動小数点数
c_longdouble|long double|浮動小数点数
c_char_p|char * (NUL 終端)|バイト列オブジェクトまたは None
c_wchar_p|wchar_t * (NUL 終端)|文字列または None
c_void_p|void *|整数または None

> コンストラクタは任意のオブジェクトをその真偽値として受け取ります。

> これら全ての型はその型を呼び出すことによって作成でき、オプションとして型と値が合っている初期化子を指定することができます:

```python
>>> c_int()
c_long(0)
>>> c_wchar_p("Hello, World")
c_wchar_p(140018365411392)
>>> c_ushort(-3)
c_ushort(65533)
```

> これらの型は変更可能であり、値を後で変更することもできます:

```python
>>> i = c_int(42)
>>> print(i)
c_long(42)
>>> print(i.value)
42
>>> i.value = -99
>>> print(i.value)
-99
```

> 新しい値をポインタ型 c_char_p, c_wchar_p および c_void_p のインスタンスへ代入すると、変わるのは指している メモリ位置 であって、メモリブロックの 内容ではありません (これは当然で、なぜなら、 Python バイト列オブジェクトは変更不可能だからです):

```python
>>> s = "Hello, World"
>>> c_s = c_wchar_p(s)
>>> print(c_s)
c_wchar_p(139966785747344)
>>> print(c_s.value)
Hello World
>>> c_s.value = "Hi, there"
>>> print(c_s)              # the memory location has changed
c_wchar_p(139966783348904)
>>> print(c_s.value)
Hi, there
>>> print(s)                # first object is unchanged
Hello, World
```

> しかし、変更可能なメモリを指すポインタであることを想定している関数へそれらを渡さないように注意すべきです。もし変更可能なメモリブロックが必要なら、 ctypes には create_string_buffer() 関数があり、いろいろな方法で作成することできます。現在のメモリブロックの内容は raw プロパティを使ってアクセス (あるいは変更) することができます。もし現在のメモリブロックに NUL 終端文字列としてアクセスしたいなら、 value プロパティを使ってください:

```python
>>> from ctypes import *
>>> p = create_string_buffer(3)            # create a 3 byte buffer, initialized to NUL bytes
>>> print(sizeof(p), repr(p.raw))
3 b'\x00\x00\x00'
>>> p = create_string_buffer(b"Hello")     # create a buffer containing a NUL terminated string
>>> print(sizeof(p), repr(p.raw))
6 b'Hello\x00'
>>> print(repr(p.value))
b'Hello'
>>> p = create_string_buffer(b"Hello", 10) # create a 10 byte buffer
>>> print(sizeof(p), repr(p.raw))
10 b'Hello\x00\x00\x00\x00\x00'
>>> p.value = b"Hi"
>>> print(sizeof(p), repr(p.raw))
10 b'Hi\x00lo\x00\x00\x00\x00\x00'
```

> create_string_buffer() 関数は初期の ctypes リリースにあった c_string() 関数だけでなく、 (エイリアスとしてはまだ利用できる) c_buffer() 関数をも置き換えるものです。 C の型 wchar_t の Unicode 文字を含む変更可能なメモリブロックを作成するには、 create_unicode_buffer() 関数を使ってください。

## [16.16.1.5. 続・関数を呼び出す](https://docs.python.jp/3/library/ctypes.html#calling-functions-continued)

> printf は sys.stdout では なく 、本物の標準出力チャンネルへプリントすることに注意してください。したがって、これらの例はコンソールプロンプトでのみ動作し、 IDLE や PythonWin では動作しません。:

```python
>>> printf = libc.printf
>>> printf(b"Hello, %s\n", b"World!")
Hello, World!
14
>>> printf(b"Hello, %S\n", "World!")
Hello, World!
14
>>> printf(b"%d bottles of beer\n", 42)
42 bottles of beer
19
>>> printf(b"%f bottles of beer\n", 42.5)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ArgumentError: argument 2: exceptions.TypeError: Don't know how to convert parameter 2
```

> 前に述べたように、必要な C のデータ型へ変換できるようにするためには、整数、文字列およびバイト列オブジェクトを除くすべての Python 型を対応する ctypes 型でラップしなければなりません:

```python
>>> printf(b"An int %d, a double %f\n", 1234, c_double(3.14))
An int 1234, a double 3.140000
31
```

## [16.16.1.6. 自作のデータ型とともに関数を呼び出す](https://docs.python.jp/3/library/ctypes.html#calling-functions-with-your-own-custom-data-types)

> 自作のクラスのインスタンスを関数引数として使えるように、 ctypes 引数変換をカスタマイズすることもできます。 ctypes は _as_parameter_ 属性を探し出し、関数引数として使います。もちろん、整数、文字列もしくはバイト列オブジェクトの中の一つでなければなりません:

```python
>>> class Bottles:
...     def __init__(self, number):
...         self._as_parameter_ = number
...
>>> bottles = Bottles(42)
>>> printf(b"%d bottles of beer\n", bottles)
42 bottles of beer
19
```

> _as_parameter_ インスタンス変数にインスタンスのデータを保持したくない場合は、必要に応じて利用できる属性を作る property を定義しても構いません。

## [16.16.1.7. 要求される引数の型を指定する (関数プロトタイプ)](https://docs.python.jp/3/library/ctypes.html#specifying-the-required-argument-types-function-prototypes)

> argtypes 属性を設定することによって、 DLL からエクスポートされている関数に要求される引数の型を指定することができます。

> argtypes は C データ型のシーケンスでなければなりません (この場合 printf 関数はおそらく良い例ではありません。なぜなら、引数の数が可変であり、フォーマット文字列に依存した異なる型のパラメータを取るからです。一方では、この機能の実験にはとても便利です)。:

```python
>>> printf.argtypes = [c_char_p, c_char_p, c_int, c_double]
>>> printf(b"String '%s', Int %d, Double %f\n", b"Hi", 10, 2.2)
String 'Hi', Int 10, Double 2.200000
37
```

> (C の関数のプロトタイプのように) 書式を指定すると互換性のない引数型になるのを防ぎ、引数を有効な型へ変換しようとします。:

```python
>>> printf(b"%d %d %d", 1, 2, 3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ArgumentError: argument 2: exceptions.TypeError: wrong type
>>> printf(b"%s %d %f\n", b"X", 2, 3)
X 2 3.000000
13
```

> 関数呼び出しへ渡す自作のクラスを定義した場合には、 argtypes シーケンスの中で使えるようにするために、そのクラスに from_param() クラスメソッドを実装しなければなりません。 from_param() クラスメソッドは関数呼び出しへ渡された Python オブジェクトを受け取り、型チェックもしくはこのオブジェクトが受け入れ可能であると確かめるために必要なことはすべて行ってから、オブジェクト自身、 _as_parameter_ 属性、あるいは、この場合に C 関数引数として渡したい何かの値を返さなければなりません。繰り返しになりますが、その返される結果は整数、文字列、バイト列、 ctypes インスタンス、あるいは _as_parameter_ 属性をもつオブジェクトであるべきです。

## [16.16.1.8. 戻り値の型](https://docs.python.jp/3/library/ctypes.html#return-types)

> デフォルトでは、関数は C int を返すと仮定されます。他の戻り値の型を指定するには、関数オブジェクトの restype 属性に設定します。

> さらに高度な例として、 strchr 関数を使います。この関数は文字列ポインタと char を受け取り、文字列へのポインタを返します。:

```python
>>> strchr = libc.strchr
>>> strchr(b"abcdef", ord("d"))  
8059983
>>> strchr.restype = c_char_p    # c_char_p is a pointer to a string
>>> strchr(b"abcdef", ord("d"))
b'def'
>>> print(strchr(b"abcdef", ord("x")))
None
```

> 上の ord("x") 呼び出しを避けたいなら、 argtypes 属性を設定することができます。二番目の引数が一文字の Python バイト列オブジェクトから C の char へ変換されます:

```python
>>> strchr.restype = c_char_p
>>> strchr.argtypes = [c_char_p, c_char]
>>> strchr(b"abcdef", b"d")
'def'
>>> strchr(b"abcdef", b"def")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ArgumentError: argument 2: exceptions.TypeError: one character string expected
>>> print(strchr(b"abcdef", b"x"))
None
>>> strchr(b"abcdef", b"d")
'def'
```

> 外部関数が整数を返す場合は、 restype 属性として呼び出し可能な Python オブジェクト (例えば、関数またはクラス) を使うこともできます。呼び出し可能オブジェクトは C 関数が返す 整数 とともに呼び出され、この呼び出しの結果は関数呼び出しの結果として使われるでしょう。これはエラーの戻り値をチェックして自動的に例外を送出させるために役に立ちます。:

```python
>>> GetModuleHandle = windll.kernel32.GetModuleHandleA  
>>> def ValidHandle(value):
...     if value == 0:
...         raise WinError()
...     return value
...
>>>
>>> GetModuleHandle.restype = ValidHandle  
>>> GetModuleHandle(None)  
486539264
>>> GetModuleHandle("something silly")  
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in ValidHandle
OSError: [Errno 126] The specified module could not be found.
```

> WinError はエラーコードの文字列表現を得るために Windows の FormatMessage() api を呼び出し、例外を 返す 関数です。 WinError はオプションでエラーコードパラメータを取ります。このパラメータが使われない場合は、エラーコードを取り出すために GetLastError() を呼び出します。

> errcheck 属性によってもっと強力なエラーチェック機構を利用できることに注意してください。詳細はリファレンスマニュアルを参照してください。

## [16.16.1.9. ポインタを渡す(または、パラメータの参照渡し)](https://docs.python.jp/3/library/ctypes.html#passing-pointers-or-passing-parameters-by-reference)

> 時には、 C api 関数がパラメータのデータ型として ポインタ を想定していることがあります。おそらくパラメータと同一の場所に書き込むためか、もしくはそのデータが大きすぎて値渡しできない場合です。これは パラメータの参照渡し としても知られています。

> ctypes は byref() 関数をエクスポートしており、パラメータを参照渡しするために使用します。 pointer() 関数を使っても同じ効果が得られます。しかし、 pointer() は本当のポインタオブジェクトを構築するためより多くの処理を行うことから、 Python 側でポインタオブジェクト自体を必要としないならば byref() を使う方がより高速です。:

```python
>>> i = c_int()
>>> f = c_float()
>>> s = create_string_buffer(b'\000' * 32)
>>> print(i.value, f.value, repr(s.value))
0 0.0 b''
>>> libc.sscanf(b"1 3.14 Hello", b"%d %f %s",
...             byref(i), byref(f), s)
3
>>> print(i.value, f.value, repr(s.value))
1 3.1400001049 b'Hello'
```

## [16.16.1.10. 構造体と共用体](https://docs.python.jp/3/library/ctypes.html#structures-and-unions)

> 構造体と共用体は ctypes モジュールに定義されている Structure および Union ベースクラスからの派生クラスでなければなりません。それぞれのサブクラスは _fields_ 属性を定義する必要があります。 _fields_ は フィールド名 と フィールド型 を持つ 2要素タプル のリストでなければなりません。

> フィールド型は c_int か他の ctypes 型 (構造体、共用体、配列、ポインタ) から派生した ctypes 型である必要があります。

> 以下は、 x と y という名前の二つの整数からなる簡単な POINT 構造体の例です。コンストラクタで構造体を初期化する方法も説明しています:

```python
>>> from ctypes import *
>>> class POINT(Structure):
...     _fields_ = [("x", c_int),
...                 ("y", c_int)]
...
>>> point = POINT(10, 20)
>>> print(point.x, point.y)
10 20
>>> point = POINT(y=5)
>>> print(point.x, point.y)
0 5
>>> POINT(1, 2, 3)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: too many initializers
```

> しかし、もっと複雑な構造体を構築することもできます。ある構造体は、他の構造体をフィールド型として使うことで、他の構造体を含むことができます。

upperleft と lowerright という名前の二つの POINT を持つ RECT 構造体です。:

```python
>>> class RECT(Structure):
...     _fields_ = [("upperleft", POINT),
...                 ("lowerright", POINT)]
...
>>> rc = RECT(point)
>>> print(rc.upperleft.x, rc.upperleft.y)
0 5
>>> print(rc.lowerright.x, rc.lowerright.y)
0 0
```

> 入れ子になった構造体はいくつかの方法を用いてコンストラクタで初期化することができます。:

```python
>>> r = RECT(POINT(1, 2), POINT(3, 4))
>>> r = RECT((1, 2), (3, 4))
```

> フィールド descriptor (記述子)は クラス から取り出せます。デバッグするときに役に立つ情報を得ることができます:

```python
>>> print(POINT.x)
<Field type=c_long, ofs=0, size=4>
>>> print(POINT.y)
<Field type=c_long, ofs=4, size=4>
```

> 警告

> ctypes では、ビットフィールドのある共用体や構造体の関数への値渡しはサポートしていません。これは 32-bit の x86 環境では動くかもしれませんが、このライブラリでは一般の場合に動作することは保証していません。

## [16.16.1.11. 構造体/共用体アライメントとバイトオーダー](https://docs.python.jp/3/library/ctypes.html#structure-union-alignment-and-byte-order)

> デフォルトでは、構造体 (Structure) と共用体(Union) のフィールドは C コンパイラが行うのと同じ方法でアライメントされています。サブクラスを定義するときに _pack_ クラス属性を指定することでこの動作を変えることは可能です。このクラス属性には正の整数を設定する必要があり、フィールドの最大アライメントを指定します。これは MSVC で #pragma pack(n) が行っていること同じです。

> ctypes は Structure と Union に対してネイティブのバイトオーダーを使います。ネイティブではないバイトオーダーの構造体を作成するには、 BigEndianStructure, LittleEndianStructure, BigEndianUnion および LittleEndianUnion ベースクラスの中の一つを使います。これらのクラスにポインタフィールドを持たせることはできません。

## [16.16.1.12. 構造体と共用体におけるビットフィールド](https://docs.python.jp/3/library/ctypes.html#bit-fields-in-structures-and-unions)

> ビットフィールドを含む構造体と共用体を作ることができます。ビットフィールドは整数フィールドに対してのみ作ることができ、ビット幅は _fields_ タプルの第三要素で指定します。:

```python
>>> class Int(Structure):
...     _fields_ = [("first_16", c_int, 16),
...                 ("second_16", c_int, 16)]
...
>>> print(Int.first_16)
<Field type=c_long, ofs=0:0, bits=16>
>>> print(Int.second_16)
<Field type=c_long, ofs=0:16, bits=16>
```

## [16.16.1.13. 配列](https://docs.python.jp/3/library/ctypes.html#arrays)

> 配列 (Array) はシーケンスであり、決まった数の同じ型のインスタンスを持ちます。

> 推奨されている配列の作成方法はデータ型に正の整数を掛けることです。:

```python
TenPointsArrayType = POINT * 10
```

ややわざとらしいデータ型の例になりますが、他のものに混ざって 4 個の POINT がある構造体です:

```python
>>> from ctypes import *
>>> class POINT(Structure):
...     _fields_ = ("x", c_int), ("y", c_int)
...
>>> class MyStruct(Structure):
...     _fields_ = [("a", c_int),
...                 ("b", c_float),
...                 ("point_array", POINT * 4)]
>>>
>>> print(len(MyStruct().point_array))
4
```

> インスタンスはクラスを呼び出す通常の方法で作成します。:

```python
arr = TenPointsArrayType()
for pt in arr:
    print(pt.x, pt.y)
```

上記のコードは 0 0 という行が並んだものを表示します。配列の要素がゼロで初期化されているためです。

正しい型の初期化子を指定することもできます。:

```python
>>> from ctypes import *
>>> TenIntegers = c_int * 10
>>> ii = TenIntegers(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
>>> print(ii)
<c_long_Array_10 object at 0x...>
>>> for i in ii: print(i, end=" ")
...
1 2 3 4 5 6 7 8 9 10
```

## [16.16.1.14. ポインタ](https://docs.python.jp/3/library/ctypes.html#pointers)

> ポインタのインスタンスは ctypes 型に対して pointer() 関数を呼び出して作成します。:

```python
>>> from ctypes import *
>>> i = c_int(42)
>>> pi = pointer(i)
```

> 次のように、ポインタインスタンスは、ポインタが指すオブジェクト (上の例では i) を返す contents 属性を持ちます:

```python
>>> pi.contents
c_long(42)
```

> ctypes は OOR (original object return 、元のオブジェクトを返すこと) ではないことに注意してください。属性を取り出す度に、新しい同等のオブジェクトを作成しているのです。:

```python
>>> pi.contents is i
False
>>> pi.contents is pi.contents
False
```

> 別の c_int インスタンスがポインタの contents 属性に代入されると、これが記憶されているメモリ位置を指すポインタに変化します。:

```python
>>> i = c_int(99)
>>> pi.contents = i
>>> pi.contents
c_long(99)
```

> ポインタインスタンスは整数でインデックス指定することもできます。:

```python
>>> pi[0]
99
```

> 整数インデックスへ代入するとポインタが指す値が変更されます。:

```python
>>> print(i)
c_long(99)
>>> pi[0] = 22
>>> print(i)
c_long(22)
```

> 0 ではないインデックスを使うこともできますが、 C の場合と同じように自分が何をしているかを理解している必要があります。任意のメモリ位置にアクセスもしくは変更できるのです。一般的にこの機能を使うのは、 C 関数からポインタを受け取り、そのポインタが単一の要素ではなく実際に配列を指していると 分かっている 場合だけです。

> 舞台裏では、 pointer() 関数は単にポインタインスタンスを作成するという以上のことを行っています。はじめにポインタ 型 を作成する必要があります。これは任意の ctypes 型を受け取る POINTER() 関数を使って行われ、新しい型を返します:

```python
>>> PI = POINTER(c_int)
>>> PI
<class 'ctypes.LP_c_long'>
>>> PI(42)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: expected c_long instead of int
>>> PI(c_int(42))
<ctypes.LP_c_long object at 0x...>
```

> ポインタ型を引数なしで呼び出すと NULL ポインタを作成します。 NULL ポインタは False ブール値を持っています。:

```python
>>> null_ptr = POINTER(c_int)()
>>> print(bool(null_ptr))
False
```

ctypes はポインタの指す値を取り出すときに NULL かどうかを調べます(しかし、 NULL でない不正なポインタの指す値の取り出す行為は Python をクラッシュさせるでしょう)。:

```python
>>> null_ptr[0]
Traceback (most recent call last):
    ....
ValueError: NULL pointer access
```

```python
>>> null_ptr[0] = 1234
Traceback (most recent call last):
    ....
ValueError: NULL pointer access
```

## [16.16.1.15. 型変換](https://docs.python.jp/3/library/ctypes.html#type-conversions)

> たいていの場合、 ctypes は厳密な型チェックを行います。これが意味するのは、関数の argtypes リスト内に、もしくは、構造体定義におけるメンバーフィールドの型として POINTER(c_int) がある場合、厳密に同じ型のインスタンスだけを受け取るということです。このルールには ctypes が他のオブジェクトを受け取る場合に例外がいくつかあります。例えば、ポインタ型の代わりに互換性のある配列インスタンスを渡すことができます。このように、 POINTER(c_int) に対して、 ctypes は c_int の配列を受け取ります。:

```python
>>> class Bar(Structure):
...     _fields_ = [("count", c_int), ("values", POINTER(c_int))]
...
>>> bar = Bar()
>>> bar.values = (c_int * 3)(1, 2, 3)
>>> bar.count = 3
>>> for i in range(bar.count):
...     print(bar.values[i])
...
1
2
3
```

> それに加えて、 argtypes で関数の引数が明示的に (POINTER(c_int) などの) ポインタ型であると宣言されていた場合、ポインタ型が指し示している型のオブジェクト (この場合では c_int) を関数に渡すことができます。この場合 ctypes は、必要となる byref() での変換を自動的に適用します。

> POINTER型フィールドを NULL に設定するために、 None を代入してもかまいません。:

```python
>>> bar.values = None
```

> 時には、非互換な型のインスタンスであることもあります。 C では、ある型を他の型へキャストすることができます。 ctypes は同じやり方で使える cast() 関数を提供しています。上で定義した Bar 構造体は POINTER(c_int) ポインタまたは c_int 配列を values フィールドに対して受け取り、他の型のインスタンスは受け取りません:

```python
>>> bar.values = (c_byte * 4)()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
TypeError: incompatible types, c_byte_Array_4 instance instead of LP_c_long instance
```

> このような場合には、 cast() 関数が便利です。

> cast() 関数は ctypes インスタンスを異なる ctypes データ型を指すポインタへキャストするために使えます。 cast() は二つのパラメータ、ある種のポインタかそのポインタへ変換できる ctypes オブジェクトと、 ctypes ポインタ型を取ります。そして、第二引数のインスタンスを返します。このインスタンスは第一引数と同じメモリブロックを参照しています:

```python
>>> a = (c_byte * 4)()
>>> cast(a, POINTER(c_int))
<ctypes.LP_c_long object at ...>
```

> したがって、 cast() を Bar 構造体の values フィールドへ代入するために使うことができます:

```python
>>> bar = Bar()
>>> bar.values = cast((c_byte * 4)(), POINTER(c_int))
>>> print(bar.values[0])
0
```

## [16.16.1.16. 不完全型](https://docs.python.jp/3/library/ctypes.html#incomplete-types)

> 不完全型 はメンバーがまだ指定されていない構造体、共用体もしくは配列です。 C では、前方宣言により指定され、後で定義されます。:

```c
struct cell; /* forward declaration */

struct cell {
    char *name;
    struct cell *next;
};
```

> ctypes コードへの直接的な変換ではこうなるでしょう。しかし、動作しません:

```python
>>> class cell(Structure):
...     _fields_ = [("name", c_char_p),
...                 ("next", POINTER(cell))]
...
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 2, in cell
NameError: name 'cell' is not defined
```

> なぜなら、新しい class cell はクラス文自体の中では利用できないからです。 ctypes では、 cell クラスを定義して、 _fields_ 属性をクラス文の後で設定することができます。:

```python
>>> from ctypes import *
>>> class cell(Structure):
...     pass
...
>>> cell._fields_ = [("name", c_char_p),
...                  ("next", POINTER(cell))]
```

> 試してみましょう。 cell のインスタンスを二つ作り、互いに参照し合うようにします。最後に、つながったポインタを何度かたどります。:

```python
>>> c1 = cell()
>>> c1.name = "foo"
>>> c2 = cell()
>>> c2.name = "bar"
>>> c1.next = pointer(c2)
>>> c2.next = pointer(c1)
>>> p = c1
>>> for i in range(8):
...     print(p.name, end=" ")
...     p = p.next[0]
...
foo bar foo bar foo bar foo bar
```

## [16.16.1.17. コールバック関数](https://docs.python.jp/3/library/ctypes.html#callback-functions)

> ctypes は C の呼び出し可能な関数ポインタを Python 呼び出し可能オブジェクトから作成できるようにします。これらは コールバック関数 と呼ばれることがあります。

> 最初に、コールバック関数のためのクラスを作る必要があります。そのクラスには呼び出し規約、戻り値の型およびこの関数が受け取る引数の数と型についての情報があります。

> CFUNCTYPE() ファクトリ関数は通常の cdecl 呼び出し規約を用いてコールバック関数のための型を作成します。 Windows では、 WINFUNCTYPE() ファクトリ関数が stdcall 呼び出し規約を用いてコールバック関数の型を作成します。

> これらのファクトリ関数はともに最初の引数に戻り値の型、残りの引数としてコールバック関数が想定する引数の型を渡して呼び出されます。

> 標準 C ライブラリの qsort() 関数を使う例を示します。これはコールバック関数の助けをかりて要素をソートするために使われます。 qsort() は整数の配列をソートするために使われます:

```python
>>> IntArray5 = c_int * 5
>>> ia = IntArray5(5, 1, 7, 33, 99)
>>> qsort = libc.qsort
>>> qsort.restype = None
```

> qsort() はソートするデータを指すポインタ、データ配列の要素の数、要素の一つの大きさ、およびコールバック関数である比較関数へのポインタを引数に渡して呼び出さなければなりません。そして、コールバック関数は要素を指す二つのポインタを渡されて呼び出され、一番目が二番目より小さいなら負の数を、等しいならゼロを、それ以外なら正の数を返さなければなりません。

> コールバック関数は整数へのポインタを受け取り、整数を返す必要があります。まず、コールバック関数のための type を作成します。:

```python
>>> CMPFUNC = CFUNCTYPE(c_int, POINTER(c_int), POINTER(c_int))
```

> まず初めに、これが受け取った変数を表示するだけのシンプルなコールバックです:

```python
>>> def py_cmp_func(a, b):
...     print("py_cmp_func", a[0], b[0])
...     return 0
...
>>> cmp_func = CMPFUNC(py_cmp_func)
```

> 結果は以下の通りです:

```python
>>> qsort(ia, len(ia), sizeof(c_int), cmp_func)  
py_cmp_func 5 1
py_cmp_func 33 99
py_cmp_func 7 33
py_cmp_func 5 7
py_cmp_func 1 7
```

> ここで 2 つの要素を実際に比較し、役に立つ結果を返します:

```python
>>> def py_cmp_func(a, b):
...     print("py_cmp_func", a[0], b[0])
...     return a[0] - b[0]
...
>>>
>>> qsort(ia, len(ia), sizeof(c_int), CMPFUNC(py_cmp_func)) 
py_cmp_func 5 1
py_cmp_func 33 99
py_cmp_func 7 33
py_cmp_func 1 7
py_cmp_func 5 7
```

> 簡単に確認できるように、配列を次のようにソートしました:

```python
>>> for i in ia: print(i, end=" ")
...
1 5 7 33 99
```

> 注釈

> C コードから CFUNCTYPE() オブジェクトが使用される限り、そのオブジェクトへの参照を確実に保持してください。 ctypes は参照を保持しないため、あなたが参照を保持しないと、オブジェクトはガベージコレクションの対象となり、コールバックが行われたときにプログラムをクラッシュさせる場合があります。

> 同様に、コールバック関数が Python の管理外 (例えば、コールバックを呼び出す外部のコード) で作られたスレッドで呼び出された場合、 ctypes は全ての呼び出しごとに新しいダミーの Python スレッドを作成することに注意してください。 この動作はほとんどの目的に対して正しいものですが、同じ C スレッドからの呼び出しだったとしても、 threading.local で格納された値は異なるコールバックをまたいで生存は しません 。

## [16.16.1.18. dllからエクスポートされた値へアクセスする](https://docs.python.jp/3/library/ctypes.html#accessing-values-exported-from-dlls)

> 共有ライブラリの一部は関数だけでなく変数もエクスポートしています。 Python ライブラリにある例としては Py_OptimizeFlag 、起動時の -O または -OO フラグに依存して、 0 , 1 または 2 が設定される整数があります。

> ctypes は型の in_dll() クラスメソッドを使ってこのように値にアクセスできます。 pythonapi はPython C api へアクセスできるようにするための予め定義されたシンボルです。:

```python
>>> opt_flag = c_int.in_dll(pythonapi, "Py_OptimizeFlag")
>>> print(opt_flag)
c_long(0)
```

> インタープリタが -O を指定されて動き始めた場合、サンプルは c_long(1) を表示するでしょうし、 -OO が指定されたならば c_long(2) を表示するでしょう。

> ポインタの使い方を説明する拡張例では、 Python がエクスポートする PyImport_FrozenModules ポインタにアクセスします。

> この値のドキュメントから引用すると:

>     このポインタは struct _frozen のレコードからなり、終端の要素のメンバが NULL かゼロになっているような配列を指すよう初期化されます。フリーズされたモジュールをインポートするとき、このテーブルを検索します。サードパーティ製のコードからこのポインタに仕掛けを講じて、動的に生成されたフリーズ化モジュールの集合を提供するようにできます。

> これで、このポインタを操作することが役に立つことを証明できるでしょう。例の大きさを制限するために、このテーブルを ctypes を使って読む方法だけを示します。:

```python
>>> from ctypes import *
>>>
>>> class struct_frozen(Structure):
...     _fields_ = [("name", c_char_p),
...                 ("code", POINTER(c_ubyte)),
...                 ("size", c_int)]
...
```

> 私たちは struct _frozen データ型を定義済みなので、このテーブルを指すポインタを得ることができます:

```python
>>> FrozenTable = POINTER(struct_frozen)
>>> table = FrozenTable.in_dll(pythonapi, "PyImport_FrozenModules")
```

> table が struct_frozen レコードの配列への pointer なので、その配列に対して反復処理を行えます。しかし、ループが確実に終了するようにする必要があります。なぜなら、ポインタに大きさの情報がないからです。遅かれ早かれ、アクセス違反か何かでクラッシュすることになるでしょう。 NULL エントリに達したときはループを抜ける方が良いです。:

```python
>>> for item in table:
...     if item.name is None:
...         break
...     print(item.name.decode("ascii"), item.size)
...
_frozen_importlib 31764
_frozen_importlib_external 41499
__hello__ 161
__phello__ -161
__phello__.spam 161
```

> 標準 Python はフローズンモジュールとフローズンパッケージ (負のサイズのメンバーで表されています) を持っているという事実はあまり知られておらず、テストにだけ使われています。例えば、 import __hello__ を試してみてください。

## [16.16.1.19. びっくり仰天](https://docs.python.jp/3/library/ctypes.html#surprises)

> There are some edges in ctypes where you might expect something other than what actually happens.

次に示す例について考えてみてください。:

```python
>>> from ctypes import *
>>> class POINT(Structure):
...     _fields_ = ("x", c_int), ("y", c_int)
...
>>> class RECT(Structure):
...     _fields_ = ("a", POINT), ("b", POINT)
...
>>> p1 = POINT(1, 2)
>>> p2 = POINT(3, 4)
>>> rc = RECT(p1, p2)
>>> print(rc.a.x, rc.a.y, rc.b.x, rc.b.y)
1 2 3 4
>>> # now swap the two points
>>> rc.a, rc.b = rc.b, rc.a
>>> print(rc.a.x, rc.a.y, rc.b.x, rc.b.y)
3 4 3 4
```

> うーん、最後の文に 3 4 1 2 と表示されることを期待していたはずです。何が起きたのでしょうか? 上の行の rc.a, rc.b = rc.b, rc.a の各段階はこのようになります。:

```python
>>> temp0, temp1 = rc.b, rc.a
>>> rc.a = temp0
>>> rc.b = temp1
```

> temp0 と temp1 は前記の rc オブジェクトの内部バッファでまだ使われているオブジェクトです。したがって、 rc.a = temp0 を実行すると temp0 のバッファ内容が rc のバッファへコピーされます。さらに、これは temp1 の内容を変更します。そのため、最後の代入 rc.b = temp1 は、期待する結果にはならないのです。

> Structure 、 Union および Array のサブオブジェクトを取り出しても、そのサブオブジェクトが コピー されるわけではなく、ルートオブジェクトの内部バッファにアクセスするラッパーオブジェクトを取り出すことを覚えておいてください。

> 期待とは違う振る舞いをする別の例はこれです。:

```python
>>> s = c_char_p()
>>> s.value = "abc def ghi"
>>> s.value
'abc def ghi'
>>> s.value is s.value
False
```

> なぜ False と表示されるのでしょうか? ctypes インスタンスはメモリと、メモリの内容にアクセスするいくつかの descriptor (記述子)を含むオブジェクトです。メモリブロックに Python オブジェクトを保存してもオブジェクト自身が保存される訳ではなく、オブジェクトの contents が保存されます。その contents に再アクセスすると新しい Python オブジェクトがその度に作られます。

## [16.16.1.20. 可変サイズのデータ型](https://docs.python.jp/3/library/ctypes.html#variable-sized-data-types)

> ctypes は可変サイズの配列と構造体をサポートしています。

> resize() 関数は既存の ctypes オブジェクトのメモリバッファのサイズを変更したい場合に使えます。この関数は第一引数にオブジェクト、第二引数に要求されたサイズをバイト単位で指定します。メモリブロックはオブジェクト型で指定される通常のメモリブロックより小さくすることはできません。これをやろうとすると、 ValueError が送出されます。:

```python
>>> short_array = (c_short * 4)()
>>> print(sizeof(short_array))
8
>>> resize(short_array, 4)
Traceback (most recent call last):
    ...
ValueError: minimum size is 8
>>> resize(short_array, 32)
>>> sizeof(short_array)
32
>>> sizeof(type(short_array))
8
```

> これはこれで上手くいっていますが、この配列の追加した要素へどうやってアクセスするのでしょうか? この型は要素の数が 4 個であるとまだ認識しているので、他の要素にアクセスするとエラーになります。:

```python
>>> short_array[:]
[0, 0, 0, 0]
>>> short_array[7]
Traceback (most recent call last):
    ...
IndexError: invalid index
```

> ctypes で可変サイズのデータ型を使うもう一つの方法は、必要なサイズが分かった後に Python の動的性質を使って一つ一つデータ型を(再)定義することです。

