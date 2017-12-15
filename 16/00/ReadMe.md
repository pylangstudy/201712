# 18.2. [ssl — ソケットオブジェクトに対する TLS/SSL ラッパー](https://docs.python.jp/3/library/ssl.html)

< [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

Source code: [Lib/ssl.py](https://github.com/python/cpython/tree/3.6/Lib/ssl.py)

> このモジュールは Transport Layer Security ( "Secure Sockets Layer" という名前でよく知られています) 暗号化と、クライアントサイド、サーバサイド両方のネットワークソケットのためのピア認証の仕組みを提供しています。このモジュールは OpenSSL ライブラリを利用しています。 OpenSSL は、すべてのモダンな Unix システム、 Windows 、 Mac OS X 、その他幾つかの OpenSSL がインストールされているプラットフォームで利用できます。

#### 注釈

> OSのソケットAPIに対して実装されているので、幾つかの挙動はプラットフォーム依存になるかもしれません。インストールされているOpenSSLのバージョンの違いも挙動の違いの原因になるかもしれません。例えば、TLSv1.1, TLSv1.2 は openssl version 1.0.1 以降でのみ利用できます。

#### 警告

> セキュリティで考慮すべき点 を読まずにこのモジュールを使用しないでください。SSL のデフォルト設定はアプリケーションに十分ではないので、読まない場合はセキュリティに誤った意識を持ってしまうかもしれません。

> このセクションでは、 ssl モジュールのオブジェクトと関数を解説します。 TLS, SSL, 証明書に関するより一般的な情報は、末尾にある "See Also" のセクションを参照してください。

> このモジュールは ssl.SSLSocket クラスを提供します。このクラスは socket.socket クラスを継承していて、ソケットで通信されるデータをSSLで暗号化・復号するソケットに似たラッパーになります。また、このクラスは、接続の相手側からの証明書を取得する getpeercert() メソッドや、セキュア接続で使うための暗号方式を取得する cipher() メソッドのような追加のメソッドをサポートしています。

> より洗練されたアプリケーションのために、 ssl.SSLContext クラスが設定と証明書の管理の助けとなるでしょう。それは SSLContext.wrap_socket() メソッドを通して SSL ソケットを作成することで引き継がれます。

> バージョン 3.6 で変更: OpenSSL 0.9.8, 1.0.0, 1.0.1 は廃止されており、もはやサポートされていません。ssl モジュールは、将来的に OpenSSL 1.0.2 または 1.1.0 を必要とするようになります。

## 18.2.1. [関数、定数、例外](https://docs.python.jp/3/library/ssl.html#functions-constants-and-exceptions)

属性|概要
----|----
exception ssl.SSLError|(現在のところ OpenSSL ライブラリによって提供されている)下層の SSL 実装からのエラーを伝えるための例外です。このエラーは、低レベルなネットワークの上に載っている、高レベルな暗号化と認証レイヤーでの問題を通知します。このエラーは OSError のサブタイプです。 SSLError インスタンスのエラーコードとメッセージは OpenSSL ライブラリによるものです。
    library|エラーが起こった OpenSSL サブモジュールを示すニーモニック文字列で、 SSL, PEM, X509 などです。取り得る値は OpenSSL のバージョンに依存します。
    reason|エラーが起こった原因を示すニーモニック文字列で、 CERTIFICATE_VERIFY_FAILED などです。取り得る値は OpenSSL のバージョンに依存します。
exception ssl.SSLZeroReturnError|読み出しあるいは書き込みを試みようとした際に SSL コネクションが行儀よく閉じられてしまった場合に送出される SSLError サブクラス例外です。これは下層の転送(read TCP)が閉じたことは意味しないことに注意してください。
exception ssl.SSLWantReadError|読み出しあるいは書き込みを試みようとした際に、リクエストが遂行される前に下層の TCP 転送で受け取る必要があるデータが不足した場合に non-blocking SSL socket によって送出される SSLError サブクラス例外です。
exception ssl.SSLWantWriteError|読み出しあるいは書き込みを試みようとした際に、リクエストが遂行される前に下層の TCP 転送が送信する必要があるデータが不足した場合に non-blocking SSL socket によって送出される SSLError サブクラス例外です。
exception ssl.SSLSyscallError|SSL ソケット上で操作を遂行しようとしていてシステムエラーが起こった場合に送出される SSLError サブクラス例外です。残念ながら元となった errno 番号を調べる簡単な方法はありません。
exception ssl.SSLEOFError|SSL コネクションが唐突に打ち切られた際に送出される SSLError サブクラス例外です。一般的に、このエラーが起こったら下層の転送を再利用しようと試みるべきではありません。
exception ssl.CertificateError|(ホスト名のミスマッチのような)証明書のエラーを通知するために送出されます。ただし、OpenSSL によって検出された場合の証明書エラーは SSLError です。

### 18.2.1.1. [ソケットの作成](https://docs.python.jp/3/library/ssl.html#socket-creation)

> 以下に示す関数は、スタンドアロンでソケットを作りたい場合に使います。Python 3.2 からは、これよりもっと柔軟な SSLContext.wrap_socket() が使えます。

属性|概要
----|----
ssl.wrap_socket(sock, keyfile=None, certfile=None, server_side=False, cert_reqs=CERT_NONE, ssl_version={see docs}, ca_certs=None, do_handshake_on_connect=True, suppress_ragged_eofs=True, ciphers=None)|socket.socket のインスタンス sock を受け取り、 socket.socket のサブタイプである ssl.SSLSocket のインスタンスを返します。 ssl.SSLSocket は低レイヤのソケットをSSLコンテキストでラップします。 sock は SOCK_STREAM ソケットでなければなりません; ほかのタイプのソケットはサポートされていません。

### 18.2.1.2. [コンテキストの作成](https://docs.python.jp/3/library/ssl.html#context-creation)

> コンビニエンス関数が、共通の目的で使用される SSLContext オブジェクトを作成するのに役立ちます。

属性|概要
----|----
ssl.create_default_context(purpose=Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None)|新規の SSLContext オブジェクトを、与えられた purpose のデフォルト設定で返します。設定は ssl モジュールで選択され、通常は SSLContext のコンストラクタを直接呼び出すよりも高いセキュリティレベルを表現します。

### 18.2.1.3. [乱数生成](https://docs.python.jp/3/library/ssl.html#random-generation)

属性|概要
----|----
ssl.RAND_bytes(num)|暗号学的に強固な擬似乱数の num バイトを返します。擬似乱数生成器に十分なデータでシードが与えられていない場合や、現在の RANDOM メソッドに操作がサポートされていない場合は SSLError を送出します。 RAND_status() を使って擬似乱数生成器の状態をチェックできます。 RAND_add() を使って擬似乱数生成器にシードを与えることができます。
ssl.RAND_pseudo_bytes(num)|(bytes, is_cryptographic) タプルを返却: bytes は長さ num の擬似乱数バイト列、 is_cryptographic は、生成されたバイト列が暗号として強ければ True 。 操作が現在使われている RAND メソッドでサポートされていなければ、 SSLError が送出されます。
ssl.RAND_status()|SSL 擬似乱数生成器が十分なランダム性(randomness)を受け取っている時に True を、それ以外の場合は False を返します。 ssl.RAND_egd() と ssl.RAND_add() を使って擬似乱数生成機にランダム性を加えることができます。
ssl.RAND_egd(path)|もしエントロピー収集デーモン(EGD=entropy-gathering daemon)が動いていて、 path がEGDへのソケットのパスだった場合、この関数はそのソケットから 256バイトのランダム性を読み込み、SSL擬似乱数生成器にそれを渡すことで、生成される暗号鍵のセキュリティを向上させることができます。これは、より良いランダム性のソースが無いシステムでのみ必要です。
ssl.RAND_add(bytes, entropy)|与えられた bytes をSSL擬似乱数生成器に混ぜます。 entropy 引数(float値)は、その文字列に含まれるエントロピーの下限(lower bound)です。 (なので、いつでも 0.0 を使うことができます。) エントロピーのソースについてのより詳しい情報は、 RFC 1750 を参照してください。

### 18.2.1.4. [証明書の取り扱い](https://docs.python.jp/3/library/ssl.html#certificate-handling)

属性|概要
----|----
ssl.match_hostname(cert, hostname)|Verify that cert (in decoded format as returned by SSLSocket.getpeercert()) matches the given hostname. The rules applied are those for checking the identity of HTTPS servers as outlined in RFC 2818, RFC 5280 and RFC 6125. In addition to HTTPS, this function should be suitable for checking the identity of servers in various SSL-based protocols such as FTPS, IMAPS, POPS and others.
ssl.cert_time_to_seconds(cert_time)|cert_time として証明書内の "notBefore" や "notAfter" の "%b %d %H:%M:%S %Y %Z" strptime フォーマット (C locale) 日付を渡すと、エポックからの積算秒を返します。
ssl.get_server_certificate(addr, ssl_version=PROTOCOL_TLS, ca_certs=None)|SSLで保護されたサーバーのアドレス addr を (hostname, port-number) の形で受け取り、そのサーバーから証明書を取得し、それを PEMエンコードされた文字列として返します。 ssl_version が指定された場合は、サーバーに接続を試みるときにそのバージョンのSSLプロトコルを利用します。 ca_certs が指定された場合、それは wrap_socket() の同名の引数と同じフォーマットで、ルート証明書のリストを含むファイルでなければなりません。この関数はサーバー証明書をルート証明書リストに対して認証し、認証が失敗した場合にこの関数も失敗します。
ssl.DER_cert_to_PEM_cert(DER_cert_bytes)|DERエンコードされたバイト列として与えられた証明書から、 PEMエンコードされたバージョンの同じ証明書を返します。
ssl.PEM_cert_to_DER_cert(PEM_cert_string)|PEM 形式のASCII文字列として与えられた証明書から、同じ証明書をDERエンコードしたバイト列を返します。
ssl.get_default_verify_paths()|OpenSSL デフォルトの cafile, capath を指すパスを名前付きタプルで返します。パスは SSLContext.set_default_verify_paths() で使われるものと同じです。戻り値は named tuple DefaultVerifyPaths です:
ssl.enum_certificates(store_name)|Windows のシステム証明書ストアより証明書を抽出します。 store_name は CA, ROOT, MY のうちどれか一つでしょう。Windows は追加の証明書ストアを提供しているかもしれません。
ssl.enum_crls(store_name)|Windows のシステム証明書ストアより CRLs を抽出します。 store_name は CA, ROOT, MY のうちどれか一つでしょう。Windows は追加の証明書ストアを提供しているかもしれません。

### 18.2.1.5. [定数](https://docs.python.jp/3/library/ssl.html#constants)

> すべての定数が enum.IntEnum コレクションまたは enum.IntFlag コレクションになりました。

> バージョン 3.6 で追加.

属性|概要
----|----
ssl.CERT_NONE|SSLContext.verify_mode または wrap_socket() の cert_reqs パラメータに使用する値です。このモード(これがデフォルトです)では、ソケット接続先からの証明書やその認証を必要としません。接続先から証明書を受け取っても検証は試みられません。
ssl.CERT_OPTIONAL|SSLContext.verify_mode または wrap_socket() の cert_reqs パラメータに使用する値です。このモードでは、ソケット接続先からの証明書やその認証を必要としませんが、証明書が提供されれば検証が試みられ、検証失敗時には SSLError が送出されます。
ssl.CERT_REQUIRED|SSLContext.verify_mode または wrap_socket() の cert_reqs パラメータに使用する値です。このモードでは、ソケット接続先からの証明書やその認証を必要とされ、証明書が提供されないかその検証失敗時には SSLError が送出されます。
class ssl.VerifyMode|CERT_* 定数の enum.IntEnum コレクションです。
ssl.VERIFY_DEFAULT|SSLContext.verify_flags に渡せる値です。このモードでは、証明書失効リスト(CRLs)はチェックされません。デフォルトでは OpenSSL は CRLs を必要ともしませんし検証にも使いません。
ssl.VERIFY_CRL_CHECK_LEAF|SSLContext.verify_flags に渡せる値です。このモードでは、接続先の証明書のチェックのみで仲介の CA 証明書はチェックしません。接続先証明書の発行者(その CA の直接の祖先)によって署名された妥当な CRL が必要です。 SSLContext.load_verify_locations が相応しいものをロードしていなければ、検証は失敗するでしょう。
ssl.VERIFY_CRL_CHECK_CHAIN|SSLContext.verify_flags に渡せる値です。このモードでは、接続先の証明書チェイン内のすべての証明書についての CRLs がチェックされます。
ssl.VERIFY_X509_STRICT|SSLContext.verify_flags に渡せる値で、壊れた X.509 証明書に対するワークアラウンドを無効にします。
ssl.VERIFY_X509_TRUSTED_FIRST|SSLContext.verify_flags に渡せる値です。OpenSSL に対し、証明書検証のために信頼チェインを構築する際、信頼できる証明書を選ぶように指示します。これはデフォルトで有効にされています。
class ssl.VerifyFlags|VERIFY_* 定数の enum.IntFlag コレクションです。
ssl.PROTOCOL_TLS|Selects the highest protocol version that both the client and server support. Despite the name, this option can select both "SSL" and "TLS" protocols.
ssl.PROTOCOL_TLS_CLIENT|Auto-negotiate the highest protocol version like PROTOCOL_TLS, but only support client-side SSLSocket connections. The protocol enables CERT_REQUIRED and check_hostname by default.
ssl.PROTOCOL_TLS_SERVER|Auto-negotiate the highest protocol version like PROTOCOL_TLS, but only support server-side SSLSocket connections.
ssl.PROTOCOL_SSLv23|data:PROTOCOL_TLS のエイリアスです。
ssl.PROTOCOL_SSLv2|チャンネル暗号化プロトコルとして SSL バージョン2を選択します。
ssl.PROTOCOL_SSLv3|チャンネル暗号化プロトコルとしてSSLバージョン3を選択します。
ssl.PROTOCOL_TLSv1|チャンネル暗号化プロトコルとしてTLSバージョン1.0を選択します。
ssl.PROTOCOL_TLSv1_1|チャンネル暗号化プロトコルとしてTLSバージョン1.1を選択します。 openssl version 1.0.1+ のみで利用可能です。
ssl.PROTOCOL_TLSv1_2|チャンネル暗号化プロトコルとしてTLSバージョン1.2を選択します。これは最も現代的で、接続の両サイドが利用できる場合は、たぶん最も安全な選択肢です。 openssl version 1.0.1+ のみで利用可能です。
ssl.OP_ALL|相手にする SSL 実装のさまざまなバグを回避するためのワークアラウンドを有効にします。このオプションはデフォルトで有効です。これを有効にする場合 OpenSSL 用の同じ意味のフラグ SSL_OP_ALL をセットする必要はありません。
ssl.OP_NO_SSLv2|SSLv2 接続が行われないようにします。このオプションは PROTOCOL_TLS と組み合わされている場合にのみ適用されます。ピアがプロトコルバージョンとして SSLv2 を選択しないようにします。
ssl.OP_NO_SSLv3|SSLv3 接続が行われないようにします。このオプションは PROTOCOL_TLS と組み合わされている場合にのみ適用されます。ピアがプロトコルバージョンとして SSLv3 を選択しないようにします。
ssl.OP_NO_TLSv1|TLSv1 接続が行われないようにします。このオプションは PROTOCOL_TLS と組み合わされている場合にのみ適用されます。ピアがプロトコルバージョンとして TLSv1 を選択しないようにします。
ssl.OP_NO_TLSv1_1|TLSv1.1 接続が行われないようにします。このオプションは PROTOCOL_TLS と組み合わされている場合にのみ適用されます。ピアがプロトコルバージョンとして TLSv1.1 を選択しないようにします。openssl バージョン 1.0.1 以降でのみ利用できます。
ssl.OP_NO_TLSv1_2|TLSv1.2 接続が行われないようにします。このオプションは PROTOCOL_TLS と組み合わされている場合にのみ適用されます。ピアがプロトコルバージョンとして TLSv1.2 を選択しないようにします。openssl バージョン 1.0.1 以降でのみ利用できます。
ssl.OP_NO_TLSv1_3|Prevents a TLSv1.3 connection. This option is only applicable in conjunction with PROTOCOL_TLS. It prevents the peers from choosing TLSv1.3 as the protocol version. TLS 1.3 is available with OpenSSL 1.1.1 or later. When Python has been compiled against an older version of OpenSSL, the flag defaults to 0.
ssl.OP_CIPHER_SERVER_PREFERENCE|暗号の優先順位として、クライアントのものではなくサーバのものを使います。このオプションはクライアントソケットと SSLv2 のサーバソケットでは効果はありません。
ssl.OP_SINGLE_DH_USE|SSL セッションを区別するのに同じ DH 鍵を再利用しないようにします。これはセキュリティを向上させますが、より多くの計算機リソースを必要とします。このオプションはサーバソケットに適用されます。
ssl.OP_SINGLE_ECDH_USE|SSL セッションを区別するのに同じ ECDH 鍵を再利用しないようにします。これはセキュリティを向上させますが、より多くの計算機リソースを必要とします。このオプションはサーバソケットに適用されます。
ssl.OP_NO_COMPRESSION|SSL チャネルでの圧縮を無効にします。これはアプリケーションのプロトコルが自身の圧縮方法をサポートする場合に有用です。
class ssl.Options|OP_* 定数の enum.IntFlag コレクションです。
ssl.OP_NO_TICKET|クライアントサイドがセッションチケットをリクエストしないようにします。
ssl.HAS_ALPN|OpenSSL ライブラリが、組み込みで RFC 7301 で記述されている Application-Layer Protocol Negotiation TLS 拡張をサポートしているかどうか。
ssl.HAS_ECDH|OpenSSL ライブラリが、組み込みの楕円曲線ディフィー・ヘルマン鍵共有をサポートしているかどうか。これは、ディストリビュータが明示的に無効にしていない限りは、真であるはずです。
ssl.HAS_SNI|Whether the OpenSSL library has built-in support for the Server Name Indication extension (as defined in RFC 6066).
ssl.HAS_NPN|OpenSSL ライブラリが、組み込みで、NPN draft specification で記述されている Next Protocol Negotiation をサポートしているかどうか。 true であれば、サポートしたいプロトコルを SSLContext.set_npn_protocols() メソッドで提示することができます。
ssl.HAS_TLSv1_3|Whether the OpenSSL library has built-in support for the TLS 1.3 protocol.
ssl.CHANNEL_BINDING_TYPES|サポートされている TLS のチャネルバインディングのタイプのリスト。リスト内の文字列は SSLSocket.get_channel_binding() の引数に渡せます。
ssl.OPENSSL_VERSION|インタプリタによってロードされた OpenSSL ライブラリのバージョン文字列:
ssl.OPENSSL_VERSION_INFO|OpenSSL ライブラリのバージョン情報を表す5つの整数のタプル:
ssl.OPENSSL_VERSION_NUMBER|1つの整数の形式の、 OpenSSL ライブラリの生のバージョン番号:
ssl.ALERT_DESCRIPTION_HANDSHAKE_FAILURE, ssl.ALERT_DESCRIPTION_INTERNAL_ERROR, ALERT_DESCRIPTION_*|RFC 5246 その他からのアラートの種類です。 IANA TLS Alert Registry にはこのリストとその意味が定義された RFC へのリファレンスが含まれています。
class ssl.AlertDescription|ALERT_DESCRIPTION_* 定数の enum.IntEnum コレクションです。
Purpose.SERVER_AUTH|create_default_context() と SSLContext.load_default_certs() に渡すオプションです。この値はコンテキストが Web サーバの認証に使われることを示します (ですので、クライアントサイドのソケットを作るのに使うことになるでしょう)。
Purpose.CLIENT_AUTH|create_default_context() と SSLContext.load_default_certs() に渡すオプションです。この値はコンテキストが Web クライアントの認証に使われることを示します (ですので、サーバサイドのソケットを作るのに使うことになるでしょう)。
class ssl.SSLErrorNumber|SSL_ERROR_* 定数の enum.IntEnum コレクションです。

## 18.2.2. [SSL ソケット](https://docs.python.jp/3/library/ssl.html#ssl-sockets)

属性|概要
----|----
class ssl.SSLSocket(socket.socket)|SSL ソケットは socket オブジェクト の以下のメソッドを提供します:
SSLSocket.read(len=1024, buffer=None)|SSL ソケットからデータの len バイトまでを読み出し、読み出した結果を bytes インスタンスで返します。 buffer を指定すると、結果は代わりに buffer に読み込まれ、読み込んだバイト数を返します。
SSLSocket.write(buf)|buf を SSL ソケットに書き込み、書き込んだバイト数を返します。 buf 引数はバッファインターフェイスをサポートするオブジェクトでなければなりません。
SSLSocket.do_handshake()|SSL セットアップのハンドシェイクを実行します。
SSLSocket.getpeercert(binary_form=False)|接続先に証明書が無い場合、 None を返します。SSL ハンドシェイクがまだ行われていない場合は、 ValueError が送出されます。
SSLSocket.cipher()|利用されている暗号の名前、その暗号の利用を定義しているSSLプロトコルのバージョン、利用されている鍵のbit長の3つの値を含むタプルを返します。もし接続が確立されていない場合、 None を返します。
SSLSocket.shared_ciphers()|ハンドシェイク中にクライアントにより共有される暗号方式のリストを返します。返されるリストの各要素は 3つの値を含むタプルで、その値はそれぞれ、暗号方式の名前、その暗号の利用を定義している SSL プロトコルのバージョン、暗号で使用される秘密鍵のビット長です。接続が確立されていないか、ソケットがクライアントソケットである場合、meth:~SSLSocket.shared_ciphers は None を返します。
SSLSocket.compression()|使われている圧縮アルゴリズムを文字列で返します。接続が圧縮されていなければ None を返します。
SSLSocket.get_channel_binding(cb_type="tls-unique")|現在の接続におけるチャネルバインディングのデータを取得します。未接続あるいはハンドシェイクが完了していなければ None を返します。
SSLSocket.selected_alpn_protocol()|TLS ハンドシェイクで選択されたプロトコルを返します。 SSLContext.set_alpn_protocols() が呼ばれていない場合、相手側が ALPN をサポートしていない場合、クライアントが提案したプロトコルのどれもソケットがサポートしない場合、あるいはハンドシェイクがまだ行われていない場合には、 None が返されます。
SSLSocket.selected_npn_protocol()|TLS/SSL ハンドシェイクで選択された上位レベルのプロトコルを返します。 SSLContext.set_npn_protocols() が呼ばれていない場合、相手側が NPN をサポートしていない場合、あるいはハンドシェイクがまだ行われていない場合には、 None が返されます。
SSLSocket.unwrap()|SSLシャットダウンハンドシェイクを実行します。これは下位レイヤーのソケットからTLSレイヤーを取り除き、下位レイヤーのソケットオブジェクトを返します。これは暗号化されたオペレーションから暗号化されていない接続に移行するときに利用されます。以降の通信には、オリジナルのソケットではなくこのメソッドが返したソケットのみを利用するべきです。
SSLSocket.version()|コネクションによって実際にネゴシエイトされた SSL プロトコルバージョンを文字列で、または、セキュアなコネクションが確立していなければ None を返します。これを書いている時点では、 "SSLv2", "SSLv3", "TLSv1", "TLSv1.1", "TLSv1.2" などが返ります。最新の OpenSSL はもっと色々な値を定義しているかもしれません。
SSLSocket.pending()|接続において既に復号済みで読み出し可能で保留になっているバイト列の数を返します。
SSLSocket.context|この SSL ソケットに結び付けられた SSLContext オブジェクトです。SSL ソケットが (SSLContext.wrap_socket() ではなく)トップレベルの wrap_socket() 関数を使って作られた場合、これはこの SSL ソケットのために作られたカスタムコンテキストオブジェクトです。
SSLSocket.server_side|サーバサイドのソケットに対して True 、クライアントサイドのソケットに対して False となる真偽値です。
SSLSocket.server_hostname|サーバのホスト名: str 型、またはサーバサイドのソケットの場合とコンストラクタで hostname が指定されなかった場合は None
SSLSocket.session|この SSL 接続に対する SSLSession です。このセッションは、TLS ハンドシェイクの実行後、クライアントサイドとサーバサイドのソケットで使用できます。クライアントソケットでは、このセッションを do_handshake() が呼ばれる前に設定して、セッションを再利用できます。
SSLSocket.session_reused|バージョン 3.6 で追加.

## 18.2.3. [SSL コンテキスト](https://docs.python.jp/3/library/ssl.html#ssl-contexts)

> バージョン 3.2 で追加.

> SSL コンテキストは、SSL 構成オプション、証明書(群)や秘密鍵(群)などのような、一回の SSL 接続よりも長生きするさまざまなデータを保持します。これはサーバサイドソケットの SSL セッションのキャッシュも管理し、同じクライアントからの繰り返しの接続時の速度向上に一役買います。

class ssl.SSLContext(protocol=PROTOCOL_TLS)|新しい SSL コンテキストを作成します。 protocol にはこのモジュールで定義されている PROTOCOL_* 定数のうち一つを指定しなければなりません。最大限の互換性とデフォルト値のためには、現時点での推奨は PROTOCOL_TLS です。
SSLContext.cert_store_stats()|ロードされた X.509 証明書の数、CA 証明書で活性の X.509 証明書の数、証明書失効リストの数、についての統計情報を辞書として取得します。
SSLContext.load_cert_chain(certfile, keyfile=None, password=None)|秘密鍵と対応する証明書をロードします。 certfile は、証明書と、証明書認証で必要とされる任意の数の CA 証明書を含む、PEM フォーマットの単一ファイルへのパスでなければなりません。 keyfile 文字列を指定する場合、秘密鍵が含まれるファイルを指すものでなければなりません。指定しない場合、秘密鍵も certfile から取得されます。 certfile への証明書の格納についての詳細は、 証明書 の議論を参照してください。
SSLContext.load_default_certs(purpose=Purpose.SERVER_AUTH)|デフォルトの場所から "認証局" (CA=certification authority) 証明書ファイル一式をロードします。Windows では、CA 証明書はシステム記憶域の CA と ROOT からロードします。それ以外のシステムでは、この関数は SSLContext.set_default_verify_paths() を呼び出します。将来的にはこのメソッドは、他の場所からも CA 証明書をロードするかもしれません。
SSLContext.load_verify_locations(cafile=None, capath=None, cadata=None)|verify_mode が CERT_NONE でない場合に接続先の証明書ファイルの正当性検証に使われる "認証局" (CA=certification authority) 証明書ファイル一式をロードします。少なくとも cafile か capath のどちらかは指定しなければなりません。
SSLContext.get_ca_certs(binary_form=False)|ロードされた "認証局" (CA=certification authority) 証明書のリストを取得します。 binary_form 引数が False である場合、リストのそれぞれのエントリは SSLSocket.getpeercert() が出力するような辞書になります。True である場合、このメソッドは、DER エンコード形式の証明書のリストを返します。返却されるリストには、 SSL 接続によって証明書がリクエストおよびロードされない限り、 capath からの証明書は含まれません。
SSLContext.get_ciphers()|有効な暗号化のリストを取得します。リストは暗号化優先度順に並びます。SSLContext.set_ciphers() を参照してください。
SSLContext.set_default_verify_paths()|デフォルトの "認証局" (CA=certification authority) 証明書を、OpenSSL ライブラリがビルドされた際に定義されたファイルシステム上のパスからロードします。残念ながらこのメソッドが成功したかどうかを知るための簡単な方法はありません: 証明書が見つからなくてもエラーは返りません。OpenSSL ライブラリがオペレーティングシステムの一部として提供されている際にはどうやら適切に構成できるようですが。
SSLContext.set_ciphers(ciphers)|Set the available ciphers for sockets created with this context. It should be a string in the OpenSSL cipher list format. If no cipher can be selected (because compile-time options or other configuration forbids use of all the specified ciphers), an SSLError will be raised.
SSLContext.set_alpn_protocols(protocols)|SSL/TLS ハンドシェイク時にソケットが提示すべきプロトコルを指定します。 ['http/1.1', 'spdy/2'] のような推奨順に並べた ASCII 文字列のリストでなければなりません。プロトコルの選択は RFC 7301 に従いハンドシェイク中に行われます。ハンドシェイクが正常に終了した後、 SSLSocket.selected_alpn_protocol() メソッドは合意されたプロトコルを返します。
SSLContext.set_npn_protocols(protocols)|SSL/TLS ハンドシェイク時にソケットが提示すべきプロトコルを指定します。 ['http/1.1', 'spdy/2'] のような推奨順に並べた文字列のリストでなければなりません。プロトコルの選択は NPN draft specification に従いハンドシェイク中に行われます。ハンドシェイクが正常に終了した後、 SSLSocket.selected_alpn_protocol() メソッドは合意されたプロトコルを返します。
SSLContext.set_servername_callback(server_name_callback)|TLS クライアントがサーバ名表示を指定した際の、SSL/TLS サーバによって TLS Client Hello ハンドシェイクメッセージが受け取られたあとで呼び出されるコールバック関数を登録します。サーバ名表示メカニズムは RFC 6066 セクション 3 - Server Name Indication で述べられています。
SSLContext.load_dh_params(dhfile)|ディフィー・ヘルマン(DH)鍵交換のための鍵生成パラメータをロードします。DH 鍵交換を用いることは、(サーバ、クライアントともに)計算機リソースに高い処理負荷をかけますがセキュリティを向上させます。 dhfile パラメータは PEM フォーマットの DH パラメータを含んだファイルへのパスでなければなりません。
SSLContext.set_ecdh_curve(curve_name)|楕円曲線ディフィー・ヘルマン(ECDH)鍵交換の曲線名を指定します。ECDH はもとの DH に較べて、ほぼ間違いなく同程度に安全である一方で、顕著に高速です。 curve_name パラメータは既知の楕円曲線を表す文字列でなければなりません。例えば prime256v1 が広くサポートされている曲線です。
SSLContext.wrap_socket(sock, server_side=False, do_handshake_on_connect=True, suppress_ragged_eofs=True, server_hostname=None, session=None)|既存の Python ソケット sock をラップして ssl.SSLSocket オブジェクトを返します。 sock は SOCK_STREAM ソケットでなければなりません; ほかのタイプのソケットはサポートされていません。
SSLContext.wrap_bio(incoming, outgoing, server_side=False, server_hostname=None, session=None)|BIO オブジェクトの incoming と outgoing をラップすることで、新しい SSLObject インスタンスを作成します。SSL ルーティンは、入力 BIO からの入力データを読み取り、出力 BIO にデータを書き出します。
SSLContext.session_stats()|このコンテキストによって作られた、または管理されている SSL セッションについての統計情報を取得します。 piece of information のそれぞれの名前にそれらが持つ数値をマッピングした辞書を返します。例えば、以下は、コンテキスト作成以降のセッションキャッシュのキャッシュヒットとキャッシュミスの総計です。
SSLContext.check_hostname|SSLSocket.do_handshake() 呼び出し時に、 match_hostname() を使って接続先証明書のホスト名の合致を見るかどうか。コンテキストの verify_mode には CERT_OPTIONAL か CERT_REQUIRED をセットしなければなりません。また wrap_socket() にはホスト名の合致をみるための server_hostname を渡さなければなりません。
SSLContext.options|このコンテキストで有効になっている SSL オプションを表す整数。デフォルトの値は OP_ALL ですが、 OP_NO_SSLv2 のような他の値をビット OR 演算で指定できます。
SSLContext.protocol|コンテキストの構築時に選択されたプロトコルバージョン。この属性は読み出し専用です。
SSLContext.verify_flags|証明書の検証操作のためのフラグです。 VERIFY_CRL_CHECK_LEAF などのフラグをビット OR 演算でセットできます。デフォルトでは OpenSSL は証明書失効リスト (CRLs) を必要としませんし検証にも使いません。openssl version 0.9.8+ でのみ利用可能です。
    
```python
```
    >>> ssl.create_default_context().verify_flags
    <VerifyFlags.VERIFY_X509_TRUSTED_FIRST: 32768>

> SSLContext.verify_mode|接続先の証明書の検証を試みるかどうか、また、検証が失敗した場合にどのように振舞うべきかを制御します。この属性は CERT_NONE, CERT_OPTIONAL, CERT_REQUIRED のうちどれか一つでなければなりません。

> バージョン 3.6 で変更: SSLContext.verify_mode は次のように VerifyMode enum (列挙) を返します。
    
```python
```
    >>> ssl.create_default_context().verify_mode
    <VerifyMode.CERT_REQUIRED: 2>

## 18.2.4. [証明書](https://docs.python.jp/3/library/ssl.html#certificates)

> 証明書を大まかに説明すると、公開鍵/秘密鍵システムの一種です。このシステムでは、各 principal (これはマシン、人、組織などです) は、ユニークな2つの暗号鍵を割り当てられます。1つは公開され、 公開鍵(public key) と呼ばれます。もう一方は秘密にされ、 秘密鍵(private key) と呼ばれます。 2つの鍵は関連しており、片方の鍵で暗号化したメッセージは、もう片方の鍵 のみ で復号できます。

> 証明書は2つの principal の情報を含んでいます。証明書は subject 名とその公開鍵を含んでいます。また、もう一つの principal である 発行者(issuer) からの、 subject が本人であることと、その公開鍵が正しいことの宣言(statement)を含んでいます。発行者からの宣言は、その発行者の秘密鍵で署名されています。発行者の秘密鍵は発行者しか知りませんが、誰もがその発行者の公開鍵を利用して宣言を復号し、証明書内の別の情報と比較することで認証することができます。証明書はまた、その証明書が有効である期限に関する情報も含んでいます。この期限は "notBefore" と "notAfter" と呼ばれる2つのフィールドで表現されています。

> Python において証明書を利用する場合、クライアントもサーバーも自分を証明するために証明書を利用することができます。ネットワーク接続の相手側に証明書の提示を要求する事ができ、そのクライアントやサーバーが認証を必要とするならその証明書を認証することができます。認証が失敗した場合、接続は例外を発生させます。認証は下位層のOpenSSLフレームワークが自動的に行います。アプリケーションは認証機構について意識する必要はありません。しかし、アプリケーションは認証プロセスのために幾つかの証明書を提供する必要があるかもしれません。

> Python は証明書を格納したファイルを利用します。そのファイルは "PEM" (RFC 1422 参照) フォーマットという、ヘッダー行とフッター行の間にbase-64エンコードされた形をとっている必要があります。

-----BEGIN CERTIFICATE-----
... (certificate in base64 PEM encoding) ...
-----END CERTIFICATE-----

### 18.2.4.1. [証明書チェイン](https://docs.python.jp/3/library/ssl.html#certificate-chains)

> Pythonが利用する証明書を格納したファイルは、ときには 証明書チェイン(certificate chain) と呼ばれる証明書のシーケンスを格納します。このチェインの先頭には、まずクライアントやサーバーである principal の証明書を置き、それ以降には、その証明書の発行者(issuer)の証明書などを続け、最後に証明対象(subject)と発行者が同じ 自己署名(self-signed) 証明書で終わります。この最後の証明書は ルート証明書(root certificate と呼ばれます。これらの証明書チェインは単純に1つの証明書ファイルに結合してください。例えば、3つの証明書からなる証明書チェインがある場合、私たちのサーバーの証明書から、私たちのサーバーに署名した認証局の証明書、そして認証局の証明書を発行した機関のルート証明書と続きます:

-----BEGIN CERTIFICATE-----
... (certificate for your server)...
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
... (the certificate for the CA)...
-----END CERTIFICATE-----
-----BEGIN CERTIFICATE-----
... (the root certificate for the CA's issuer)...
-----END CERTIFICATE-----

### 18.2.4.2. [CA 証明書](https://docs.python.jp/3/library/ssl.html#ca-certificates)

> もし相手から送られてきた証明書の認証をしたい場合、信頼している各発行者の証明書チェインが入った "CA certs" ファイルを提供する必要があります。繰り返しますが、このファイルは単純に、各チェインを結合しただけのものです。認証のために、Pythonはそのファイルの中の最初にマッチしたチェインを利用します。SSLContext.load_default_certs() を呼び出すことでプラットフォームの証明書ファイルも使われますが、これは create_default_context() によって自動的に行われます。

### 18.2.4.3. [秘密鍵と証明書の組み合わせ](https://docs.python.jp/3/library/ssl.html#combined-key-and-certificate)

> 多くの場合、証明書と同じファイルに秘密鍵も格納されています。この場合、 SSLContext.load_cert_chain(), wrap_socket() には certfile 引数だけが必要とされます。秘密鍵が証明書ファイルに格納されている場合、秘密鍵は証明書チェインの最初の証明書よりも先にないといけません。

-----BEGIN RSA PRIVATE KEY-----
... (private key in base64 encoding) ...
-----END RSA PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
... (certificate in base64 PEM encoding) ...
-----END CERTIFICATE-----

### 18.2.4.4. [自己署名証明書](https://docs.python.jp/3/library/ssl.html#self-signed-certificates)

> SSL暗号化接続サービスを提供するサーバーを建てる場合、適切な証明書を取得するには、認証局から買うなどの幾つかの方法があります。また、自己署名証明書を作るケースもあります。 OpenSSLを使って自己署名証明書を作るには、次のようにします。

% openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem
Generating a 1024 bit RSA private key
.......++++++
.............................++++++
writing new private key to 'cert.pem'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [AU]:US
State or Province Name (full name) [Some-State]:MyState
Locality Name (eg, city) []:Some City
Organization Name (eg, company) [Internet Widgits Pty Ltd]:My Organization, Inc.
Organizational Unit Name (eg, section) []:My Group
Common Name (eg, YOUR name) []:myserver.mygroup.myorganization.com
Email Address []:ops@myserver.mygroup.myorganization.com
%

> 自己署名証明書の欠点は、それ自身がルート証明書であり、他の人はその証明書を持っていない (そして信頼しない)ことです。

## 18.2.5. [使用例](https://docs.python.jp/3/library/ssl.html#examples)

### 18.2.5.1. [SSLサポートをテストする](https://docs.python.jp/3/library/ssl.html#testing-for-ssl-support)

> インストールされているPythonがSSLをサポートしているかどうかをテストするために、ユーザーコードは次のイディオムを利用することができます。

try:
    import ssl
except ImportError:
    pass
else:
    ...  # do something that requires SSL support

### 18.2.5.2. [クライアントサイドの処理](https://docs.python.jp/3/library/ssl.html#client-side-operation)

> この例では、自動的に証明書の検証を行うことを含む望ましいセキュリティ設定でクライアントソケットの SSL コンテキストを作ります:

```python
```
>>> context = ssl.create_default_context()

> 自分自身でセキュリティ設定を調整したい場合、コンテキストを一から作ることはできます (ただし、正しくない設定をしてしまいがちなことに注意してください):

```python
```
>>> context = ssl.SSLContext(ssl.PROTOCOL_TLS)
>>> context.verify_mode = ssl.CERT_REQUIRED
>>> context.check_hostname = True
>>> context.load_verify_locations("/etc/ssl/certs/ca-bundle.crt")

> (このスニペットはすべての CA 証明書が /etc/ssl/certs/ca-bundle.crt にバンドルされていることを仮定しています; もし違っていればエラーになりますので、適宜修正してください)

> サーバへの接続にこのコンテキストを使うと、 CERT_REQUIRED でサーバの証明書の検証が行われます: サーバの証明書が CA 証明書のいずれかに署名されていて、その署名が正しいことを保障します。


```python
```
>>> conn = context.wrap_socket(socket.socket(socket.AF_INET),
...                            server_hostname="www.python.org")
>>> conn.connect(("www.python.org", 443))

> そして証明書を持ってくることができます:


```python
```
>>> cert = conn.getpeercert()

> 証明書が、期待しているサービス (つまり、 HTTPS ホスト www.python.org) の身元を特定していることを視覚的に点検してみましょう:


```python
```
>>> pprint.pprint(cert)
{'OCSP': ('http://ocsp.digicert.com',),
 'caIssuers': ('http://cacerts.digicert.com/DigiCertSHA2ExtendedValidationServerCA.crt',),
 'crlDistributionPoints': ('http://crl3.digicert.com/sha2-ev-server-g1.crl',
                           'http://crl4.digicert.com/sha2-ev-server-g1.crl'),
 'issuer': ((('countryName', 'US'),),
            (('organizationName', 'DigiCert Inc'),),
            (('organizationalUnitName', 'www.digicert.com'),),
            (('commonName', 'DigiCert SHA2 Extended Validation Server CA'),)),
 'notAfter': 'Sep  9 12:00:00 2016 GMT',
 'notBefore': 'Sep  5 00:00:00 2014 GMT',
 'serialNumber': '01BB6F00122B177F36CAB49CEA8B6B26',
 'subject': ((('businessCategory', 'Private Organization'),),
             (('1.3.6.1.4.1.311.60.2.1.3', 'US'),),
             (('1.3.6.1.4.1.311.60.2.1.2', 'Delaware'),),
             (('serialNumber', '3359300'),),
             (('streetAddress', '16 Allen Rd'),),
             (('postalCode', '03894-4801'),),
             (('countryName', 'US'),),
             (('stateOrProvinceName', 'NH'),),
             (('localityName', 'Wolfeboro,'),),
             (('organizationName', 'Python Software Foundation'),),
             (('commonName', 'www.python.org'),)),
 'subjectAltName': (('DNS', 'www.python.org'),
                    ('DNS', 'python.org'),
                    ('DNS', 'pypi.python.org'),
                    ('DNS', 'docs.python.org'),
                    ('DNS', 'testpypi.python.org'),
                    ('DNS', 'bugs.python.org'),
                    ('DNS', 'wiki.python.org'),
                    ('DNS', 'hg.python.org'),
                    ('DNS', 'mail.python.org'),
                    ('DNS', 'packaging.python.org'),
                    ('DNS', 'pythonhosted.org'),
                    ('DNS', 'www.pythonhosted.org'),
                    ('DNS', 'test.pythonhosted.org'),
                    ('DNS', 'us.pycon.org'),
                    ('DNS', 'id.python.org')),
 'version': 3}

> SSL チャネルは今や確立されて証明書が検証されているので、サーバとのお喋りを続けることができます:


```python
```
>>> conn.sendall(b"HEAD / HTTP/1.0\r\nHost: linuxfr.org\r\n\r\n")
>>> pprint.pprint(conn.recv(1024).split(b"\r\n"))
[b'HTTP/1.1 200 OK',
 b'Date: Sat, 18 Oct 2014 18:27:20 GMT',
 b'Server: nginx',
 b'Content-Type: text/html; charset=utf-8',
 b'X-Frame-Options: SAMEORIGIN',
 b'Content-Length: 45679',
 b'Accept-Ranges: bytes',
 b'Via: 1.1 varnish',
 b'Age: 2188',
 b'X-Served-By: cache-lcy1134-LCY',
 b'X-Cache: HIT',
 b'X-Cache-Hits: 11',
 b'Vary: Cookie',
 b'Strict-Transport-Security: max-age=63072000; includeSubDomains',
 b'Connection: close',
 b'',
 b'']

> このドキュメントの下の方の、 セキュリティで考慮すべき点 に関する議論を参照してください。

### 18.2.5.3. [サーバサイドの処理](https://docs.python.jp/3/library/ssl.html#server-side-operation)

> サーバサイドの処理では、通常、サーバー証明書と秘密鍵がそれぞれファイルに格納された形で必要です。最初に秘密鍵と証明書が保持されたコンテキストを作成し、クライアントがあなたの信憑性をチェックできるようにします。そののちにソケットを開き、ポートにバインドし、そのソケットの listen() を呼び、クライアントからの接続を待ちます。

import socket, ssl

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="mycertfile", keyfile="mykeyfile")

bindsocket = socket.socket()
bindsocket.bind(('myaddr.mydomain.com', 10023))
bindsocket.listen(5)

> クライアントが接続してきた場合、 accept() を呼んで新しいソケットを作成し、接続のためにサーバサイドの SSL ソケットを、コンテキストの SSLContext.wrap_socket() メソッドで作ります:

while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = context.wrap_socket(newsocket, server_side=True)
    try:
        deal_with_client(connstream)
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()

> そして、 connstream からデータを読み、クライアントと切断する(あるいはクライアントが切断してくる)まで何か処理をします。

def deal_with_client(connstream):
    data = connstream.recv(1024)
    # empty data means the client is finished with us
    while data:
        if not do_something(connstream, data):
            # we'll assume do_something returns False
            # when we're finished with client
            break
        data = connstream.recv(1024)
    # finished with client

> そして新しいクライアント接続のために listen に戻ります。 (もちろん現実のサーバは、おそらく個々のクライアント接続ごとに別のスレッドで処理するか、ソケットを ノンブロッキングモード にし、イベントループを使うでしょう。)

## 18.2.6. [ノンブロッキングソケットについての注意事項](https://docs.python.jp/3/library/ssl.html#notes-on-non-blocking-sockets)

> SSL ソケットはノンブロッキングモードにおいては、普通のソケットとは少し違った振る舞いをします。ですのでノンブロッキングソケットとともに使う場合、いくつか気をつけなければならない事項があります:

> ほとんどの SSLSocket のメソッドは I/O 操作がブロックすると BlockingIOError ではなく SSLWantWriteError か SSLWantReadError のどちらかを送出します。 SSLWantReadError は下層のソケットで読み出しが必要な場合に送出され、 SSLWantWriteError は下層のソケットで書き込みが必要な場合に送出されます。SSL ソケットに対して 書き込み を試みると下層のソケットから最初に 読み出す 必要があるかもしれず、SSL ソケットに対して 読み出し を試みると下層のソケットに先に 書き込む 必要があるかもしれないことに注意してください。

> バージョン 3.5 で変更: 以前の Python バージョンでは、 SSLSocket.send() メソッドは SSLWantWriteError または SSLWantReadError を送出するのではなく、ゼロを返していました。

> select() 呼び出しは OS レベルでのソケットが読み出し可能(または書き込み可能)になったことを教えてくれますが、上位の SSL レイヤーでの十分なデータがあることを意味するわけではありません。例えば、SSL フレームの一部が届いただけかもしれません。ですから、 SSLSocket.recv() と SSLSocket.send() の失敗を処理することに備え、ほかの select() 呼び出し後にリトライしなければなりません。

> 反対に、SSL レイヤーは独自の枠組みを持っているため、select() が気付かない読み出し可能なデータを SSL ソケットが持っている場合があります。したがって、入手可能な可能性のあるデータをすべて引き出すために最初に SSLSocket.recv() を呼び出し、次にそれでもまだ必要な場合にだけ select() 呼び出しでブロックすべきです。

> (当然のことながら、ほかのプリミティブ、例えば poll() や selectors モジュール内のものを使う際にも似た但し書きが付きます)

> SSL ハンドシェイクそのものがノンブロッキングになります: SSLSocket.do_handshake() メソッドは成功するまでリトライしなければなりません。 select() を用いてソケットの準備が整うのを待つためには、およそ以下のようにします:

    while True:
        try:
            sock.do_handshake()
            break
        except ssl.SSLWantReadError:
            select.select([sock], [], [])
        except ssl.SSLWantWriteError:
            select.select([], [sock], [])

##### 参考

> asyncio モジュールは ノンブロッキング SSL ソケット をサポートし、より高いレベルの API を提供しています。 selectors モジュールを使ってイベントを poll し、 SSLWantWriteError, SSLWantReadError, BlockingIOError 例外を処理します。SSL ハンドシェイクも非同期に実行します。 

## 18.2.7. [メモリ BIO サポート](https://docs.python.jp/3/library/ssl.html#memory-bio-support)

> バージョン 3.5 で追加.

> Python 2.6 で SSL モジュールが導入されて以降、SSLSocket クラスは、以下の互いに関連するが別々の機能を提供してきました。

* SSL プロトコル処理
* ネットワーク IO

> ネットワーク IO API は、socket.socket が提供するものと同じです。SSLSocket も、そのクラスから継承しています。これにより、SSL ソケットは標準のソケットをそっくりそのまま置き換えるものとして使用できるため、既存のアプリケーションを SSL に対応させるのが非常に簡単になります。

> SSL プロトコルの処理とネットワーク IO を組み合わせた場合、通常は問題なく動作しますが、問題が発生する場合があります。一例を挙げると、非同期 IO フレームワークが別の多重化モデルを使用する場合、これは socket.socket と内部 OpenSSL ソケット IO ルーティンが想定する「ファイル記述子上の select/poll」モデル（準備状態ベース）とは異なります。これは、このモデルが非効率的になる Windows などのプラットフォームに主に該当します。そのため、スコープを限定した SSLSocket の変種、 SSLObject が提供されています。

属性|概要
----|----
class ssl.SSLObject|ネットワーク IO メソッドを含まない SSL プロトコルインスタンスを表す、スコープを限定した SSLSocket の変種です。一般的にこ、のクラスを使用するのは、メモリバッファを通じて SSL のための非同期 IO を実装するフレームワーク作成者です。

> このクラスは、OpenSSL が実装する低水準 SSL オブジェクトの上にインターフェイスを実装します。このオブジェクトは SSL 接続の状態をキャプチャしますが、ネットワーク IO 自体は提供しません。IO は、OpenSSL の IO 抽象レイヤである別の「BIO」オブジェクトを通じて実行する必要があります。

> SSLObject インスタンスは、 wrap_bio() メソッドを使用して作成できます。このメソッドは、SSLObject インスタンスを作成し、2 つの BIO に束縛します。incoming BIO は、Python から SSL プロトコルインスタンスにデータを渡すために使用され、outgoing BIO は、データを反対向きに渡すために使用されます。

> 次のメソッドがサポートされています:

* [context](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.context)
* [server_side](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.server_side)
* [server_hostname](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.server_hostname)
* [session](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.session)
* [session_reused](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.session_reused)
* [read()](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.read)
* [write()](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.write)
* [getpeercert()](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.getpeercert)
* [selected_npn_protocol()](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.selected_npn_protocol)
* [cipher()](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.cipher)
* [shared_ciphers()](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.shared_ciphers)
* [compression()](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.compression)
* [pending()](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.pending)
* [do_handshake()](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.do_handshake)
* [unwrap()](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.unwrap)
* [get_channel_binding()](https://docs.python.jp/3/library/ssl.html#ssl.SSLSocket.get_channel_binding)

> SSLSocket と比較すると、このオブジェクトでは以下の機能が不足しています。

* Any form of network IO; recv() and send() read and write only to the underlying MemoryBIO buffers.
* do_handshake_on_connect 機構はありません。必ず手動で do_handshake() を呼んで、ハンドシェイクを開始する必要があります。
* suppress_ragged_eofs は処理されません。プロトコルに違反するファイル末尾状態は、 SSLEOFError 例外を通じて報告されます。
* unwrap() メソッドの呼び出しは、下層のソケットを返す SSL ソケットとは異なり、何も返しません。
* SSLContext.set_servername_callback() に渡される server_name_callback コールバックは、1 つ目の引数として SSLSocket インスタンスではなく SSLObject インスタンスを受け取ります。

> SSLObject の使用に関する注意:

> SSLObject 上のすべての IO は non-blocking です。例えば、read() は入力 BIO が持つデータよりも多くのデータを必要とする場合、SSLWantReadError を送出します。
> wrap_socket() に対して存在するような、モジュールレベルの wrap_bio() 呼び出しは存在しません。SSLObject は、常に SSLContext を経由して作成されます。

> SSLObject は、メモリバッファを使用して外界と通信します。MemoryBIO クラスは、以下のように OpenSSL メモリ BIO (Basic IO) オブジェクトをラップし、この目的に使用できるメモリバッファを提供します。

属性|概要
----|----
class ssl.MemoryBIO|Python と SSL プロトコルインスタンス間でデータをやり取りするために使用できるメモリバッファ。
pending|現在メモリバッファ中にあるバイト数を返します。
eof|メモリ BIOが現在ファイルの末尾にあるかを表す真偽値です。
read(n=-1)|メモリバッファから最大 n 読み取ります。n が指定されていないか、負値の場合、すべてのバイトが返されます。
write(buf)|buf からメモリ BIO にバイトを書き込みます。buf 引数は、バッファプロトコルをサポートするオブジェクトでなければなりません。 戻り値は、書き込まれるバイト数であり、常に buf の長さと等しくなります。
write_eof()|EOF マーカーをメモリ BIO に書き込みます。このメソッドが呼び出された後に write() を呼ぶことはできません。eof 属性は、バッファ内のすべてのデータが読み出された後に True になります。

## 18.2.8. [SSL セッション](https://docs.python.jp/3/library/ssl.html#ssl-session)

> バージョン 3.6 で追加.

属性|概要
----|----
class ssl.SSLSession|session が使用するセッションオブジェクトです。
id| 
time| 
timeout| 
ticket_lifetime_hint| 
has_ticket| 

## 18.2.9. [セキュリティで考慮すべき点](https://docs.python.jp/3/library/ssl.html#security-considerations)

### 18.2.9.1. [最善のデフォルト値](https://docs.python.jp/3/library/ssl.html#best-defaults)

> クライアントでの使用 では、セキュリティポリシーによる特殊な要件がない限りは、 create_default_context() 関数を使用して SSL コンテキストを作成することを強くお勧めします。この関数は、システムの信頼済み CA 証明書をロードし、証明書の検証とホスト名のチェックを有効化し、十分にセキュアなプロトコルと暗号を選択しようとします。

例として、 smtplib.SMTP クラスを使用して SMTP サーバーに対して信頼できるセキュアな接続を行う方法を以下に示します:

```python
```
>>> import ssl, smtplib
>>> smtp = smtplib.SMTP("mail.python.org", port=587)
>>> context = ssl.create_default_context()
>>> smtp.starttls(context=context)
(220, b'2.0.0 Ready to start TLS')

> 接続にクライアントの証明書が必要な場合、 SSLContext.load_cert_chain() によって追加できます。

> 対照的に、自分自身で SSLContext クラスのコンストラクタを呼び出すことによって SSL コンテキストを作ると、デフォルトでは証明書検証もホスト名チェックも有効になりません。自分で設定を行う場合は、十分なセキュリティレベルを達成するために、以下のパラグラフをお読みください。

### 18.2.9.2. [手動での設定](https://docs.python.jp/3/library/ssl.html#manual-settings)

#### 18.2.9.2.1. [証明書の検証](https://docs.python.jp/3/library/ssl.html#verifying-certificates)

> SSLContext のコンストラクタを直接呼び出した場合、 CERT_NONE がデフォルトとして使われます。これは接続先の身元特定をしないので安全ではありませんし、特にクライアントモードでは大抵相手となるサーバの信憑性を保障したいでしょう。ですから、クライアントモードでは CERT_REQUIRED を強くお勧めします。ですが、それだけでは不十分です; SSLSocket.getpeercert() を呼び出してサーバ証明書が望んだサービスと合致するかのチェックもしなければなりません。多くのプロトコルとアプリケーションにとって、サービスはホスト名で特定されます; この場合、 match_hostname() が使えます。これらの共通的なチェックは SSLContext.check_hostname が有効な場合、自動的に行われます。

> サーバモードにおいて、(より上位のレベルでの認証メカニズムではなく) SSL レイヤーを使ってあなたのクライアントを認証したいならば、 CERT_REQUIRED を指定して同じようにクライアントの証明書を検証すべきでしょう。

##### 注釈

> クライアントモードでは anonymous ciphers が有効(デフォルトでは無効)でない限り、 CERT_OPTIONAL と CERT_REQUIRED は同じ意味になります。

#### 18.2.9.2.2. [プロトコルのバージョン](https://docs.python.jp/3/library/ssl.html#protocol-versions)

> SSL バージョン 2 と 3 は安全性に欠けると考えられており、使用するのは危険です。クライアントとサーバ間の互換性を最大限に確保したい場合、プロトコルバージョンとして PROTOCOL_TLS_CLIENT または PROTOCOL_TLS_SERVER を使用してください。 SSLv2 と SSLv3 はデフォルトで無効になっています。

```python
```
>>> client_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
>>> client_context.options |= ssl.OP_NO_TLSv1
>>> client_context.options |= ssl.OP_NO_TLSv1_1

> 上記で作成した SSL コンテキストは、TLSv1.2 以降 (システムでサポートされている場合) でのサーバへの接続のみを許可します。PROTOCOL_TLS_CLIENT は、デフォルトで証明書の検証とホスト名のチェックを意味します。コンテキスト中に証明書をロードする必要があります。

#### 18.2.9.2.3. [暗号の選択](https://docs.python.jp/3/library/ssl.html#cipher-selection)

> 高度なセキュリティが要求されている場合、SSL セッションのネゴシエーションで有効になる暗号の微調整が SSLContext.set_ciphers() によって可能です。Python 3.2.3 以降、 ssl モジュールではデフォルトで特定の弱い暗号化が無効になっていますが、暗号方式の選択をさらに厳しく制限したい場合もあるでしょう。OpenSSL ドキュメントの cipher list format を注意深く読んでください。与えられた暗号方式リストによって有効になる暗号方式をチェックするには、SSLContext.get_ciphers() メソッドまたは openssl ciphers コマンドをシステム上で実行してください。

### 18.2.9.3. [マルチプロセス化](https://docs.python.jp/3/library/ssl.html#multi-processing)

> (例えば multiprocessing や concurrent.futures を使って、)マルチプロセスアプリケーションの一部としてこのモジュールを使う場合、OpenSSL の内部の乱数発生器は fork したプロセスを適切に処理しないことに気を付けて下さい。SSL の機能を os.fork() とともに使う場合、アプリケーションは親プロセスの PRNG 状態を変更しなければなりません。 RAND_add(), RAND_bytes(), RAND_pseudo_bytes() のいずれかの呼び出し成功があれば十分です。

#### 参考

URL|概要
---|----
[socket.socket クラス](https://docs.python.jp/3/library/socket.html#socket.socket)|下位レイヤーの socket クラスのドキュメント
[SSL/TLS Strong Encryption: An Introduction](https://httpd.apache.org/docs/trunk/en/ssl/ssl_intro.html)|Apache WEBサーバのドキュメンテーションのイントロ
[RFC 1422: Privacy Enhancement for Internet Electronic Mail: Part II: Certificate-Based Key Management](https://www.ietf.org/rfc/rfc1422)|Steve Kent
[RFC 4086: Randomness Requirements for Security](http://datatracker.ietf.org/doc/rfc4086/)|Donald E., Jeffrey I. Schiller
[RFC 5280: Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile](http://datatracker.ietf.org/doc/rfc5280/)|D. Cooper
[RFC 5246: The Transport Layer Security (TLS) Protocol Version 1.2](https://tools.ietf.org/html/rfc5246)|T. Dierks et. al.
[RFC 6066: Transport Layer Security (TLS) Extensions](https://tools.ietf.org/html/rfc6066)|D. Eastlake
[IANA TLS: Transport Layer Security (TLS) Parameters](https://www.iana.org/assignments/tls-parameters/tls-parameters.xml)|IANA
[RFC 7525: Recommendations for Secure Use of Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS)](https://tools.ietf.org/html/rfc7525)|IETF
[Mozilla’s Server Side TLS recommendations](https://wiki.mozilla.org/Security/Server_Side_TLS)|Mozilla

