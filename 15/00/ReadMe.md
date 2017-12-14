# [18.1. socket — 低水準ネットワークインターフェイス](https://docs.python.jp/3/library/socket.html)

< [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

ソースコード: [Lib/socket.py](https://github.com/python/cpython/tree/3.6/Lib/socket.py)

> このモジュールはBSDの ソケット(socket) インターフェイスへのアクセスを提供します。これは、近代的なUnixシステム、Windows、MacOS、その他多くのプラットフォームで動作します。

### 注釈

> いくつかの挙動はプラットフォームに依存します。オペレーティングシステムのソケットAPIを呼び出しているためです。

> Pythonインターフェースは、Unixのソケット用システムコールとライブラリインターフェースを、そのままPythonのオブジェクト指向スタイルに変換したものです。各種ソケット関連のシステムコールは、 socket() 関数で生成される socket オブジェクト のメソッドとして実装されています。 メソッドの引数は C のインターフェイスよりも多少高水準で、例えばファイルに対する read() や write() メソッドと同様に、 受信時のバッファ確保は自動的に処理され、送信時のバッファ長は暗黙的に決まります。

### 参考

Module|概要
------|----
[socketserver](https://docs.python.jp/3/library/socketserver.html#module-socketserver)|ネットワークサーバの開発を省力化するためのクラス群。
[ssl](https://docs.python.jp/3/library/ssl.html#module-ssl)|ソケットオブジェクトに対する TLS/SSL ラッパー.

## [18.1.1. ソケットファミリー](https://docs.python.jp/3/library/socket.html#socket-families)

> どのシステムで実行するかとビルドオプションに依存しますが、このモジュールによって多様なソケットファミリーをサポートします。

> 特定のソケットオブジェクトによって必要とされるアドレスフォーマットは、ソケットオブジェクトが生成されたときに指定されたアドレスファミリーを元に自動的に選択されます。ソケットアドレスは次の通りです。

* ファイルシステム上のノードに束縛された AF_UNIX ソケットのアドレスは、ファイルシステムエンコーディングと 'surrogateescape' エラーハンドラ (PEP 383 を参照) を使って文字列として表現されます。 Linux の抽象名前空間のアドレスは、先頭が null バイトとなる bytes-like object として返されます。この名前空間のソケットは通常のファイルシステム上のソケットと通信できるので、 Linux 上で動作することを意図したプログラムは両方のアドレスを扱う必要がある可能性があります。文字列と bytes-like オブジェクトはどちらのタイプのアドレスにも引数として渡すことができます。
* AF_INET アドレスファミリーには、 (host, port) ペアがアドレスとして利用されます。 host はホスト名か 'daring.cwi.nl' のようなインターネットドメインか、 '100.50.200.5' のような IPv4 アドレスで、 port は整数です。
* AF_INET6 アドレスファミリーでは、 (host, port, flowinfo, scopeid) の4 要素のタプルが利用されます。 flowinfo と scopeid はそれぞれC言語の struct sockaddr_in6 の sin6_flowinfo と sin6_scope_id メンバーを表します。 socket モジュールのメソッドでは、後方互換性のために flowinfo と scopeid の省略を許しています。しかし、 scopeid を省略すると scope された IPv6 アドレスを操作するときに問題が起こる場合があることに注意してください。
* AF_NETLINK ソケットのアドレスは (pid, groups) のペアで表されます。
* Linux 限定で、 AF_TIPC アドレスファミリーを用いて TIPC がサポートされます。 TIPC は、クラスタコンピューティング環境のために設計された、IP ベースではないオープンなネットワークプロトコルです。アドレスはタプルで表現され、フィールドはアドレスタイプに依存します。一般的なタプルの形式は (addr_type, v1, v2, v3 [, scope]) で、それぞれは次の通りです:
    * addr_type は TIPC_ADDR_NAMESEQ, TIPC_ADDR_NAME, TIPC_ADDR_ID の1つ。
    * scope は TIPC_ZONE_SCOPE, TIPC_CLUSTER_SCOPE, TIPC_NODE_SCOPE の1つ。
    * addr_type が TIPC_ADDR_NAME の場合、 v1 はサーバータイプ、 v2 はポートID (the port identifier)、そして v3 は 0 であるべきです。 addr_type が TIPC_ADDR_NAMESEQ の場合、 v1 はサーバータイプ、 v2 はポート番号下位(lower port number)、 v3 はポート番号上位(upper port number) です。 addr_type が TIPC_ADDR_ID の場合、 v1 はノード、 v2 は参照、 v3 は0であるべきです。
* AF_CAN アドレスファミリーには (interface,) というタプルを利用します。 interface は 'can0' のようなネットワークインタフェース名を表す文字列です。このファミリーの全てのネットワークインタフェースからパケットを受信するために、ネットワークインタフェース名 '' を利用できます。
* 文字列またはタプル (id, unit) は PF_SYSTEM ファミリーの SYSPROTO_CONTROL プロトコルのために使用されます。この文字列は、動的に割り当てられたIDによるカーネルコントロールの名前です。このタプルは、カーネルコントロールのIDとユニット番号が既知の場合、または登録済みIDが使用中の場合に使用することができます。
* AF_BLUETOOTH は以下のプロトコルとアドレスフォーマットをサポートしています。
    * BTPROTO_L2CAP は (bdaddr, psm) を受け取ります。 bdaddr は Bluetooth アドレスを表す文字列で、 psm は整数です。
    * BTPROTO_RFCOMM は (bdaddr, channel) を受け取ります。 bdaddr は Bluetooth アドレスを表す文字列で、 channel は整数です。
    * BTPROTO_HCI は (device_id,) を受け取ります。 device_id は、数値またはインターフェイスの Bluetooth アドレスを表す文字列です。(OS に依存します。NetBSD と DragonFlyBSD は Bluetooth アドレスを期待しますが、その他すべての OS は、数値を期待します。)
    * BTPROTO_SCO は bdaddr を受け取ります。ここで、 bdaddr は Bluetooth アドレスを文字列形式で持つ bytes オブジェクトです (例: b'12:23:34:45:56:67')。このプロトコルは、 FreeBSD ではサポートされていません。
* AF_ALG はカーネル暗号へのソケットベースのインターフェイスで、Linux でのみ使用できます。アルゴリズムソケットは、2 つから 4 つの要素を持つタプル (type, name [, feat [, mask]]) で構成されます。各要素の意味は、以下の通りです。
    * type はアルゴリズムタイプを示す文字列です。例: aead, hash, skcipher または rng。
    * name はアルゴリズム名及び操作モードを示す文字列です。例: sha256, hmac(sha256), cbc(aes) または drbg_nopr_ctr_aes256。
    * feat と mask は、符号を持たない 32 ビットの整数です。
* その他の特定のアドレスファミリー (AF_PACKET, AF_CAN) は、それぞれ固有の形式をサポートしています。

> IPv4 アドレスでは、ホストアドレスの代わりに2つの特殊な形式を利用できます。 IPv4アドレスのホストアドレスが空文字列の場合、 INADDR_ANY として処理されます。また、 '<broadcast>' の場合は INADDR_BROADCAST として処理されます。 IPv6では後方互換性のためこの機能は用意されていませんので、IPv6をサポートするPythonプログラムでは利用しないで下さい。

> IPv4/v6ソケットの host 部にホスト名を指定すると、処理結果が一定ではない場合があります。これはPythonはDNSから取得したアドレスのうち最初のアドレスを使用するので、 DNSの処理やホストの設定によって異なるIPv4/6アドレスを取得する場合があるためです。常に同じ結果が必要であれば、 host に数値のアドレスを指定してください。

> 全てのエラーは例外を発生させます。引数型のエラーやメモリ不足の場合には通常の例外が発生し、ソケットやアドレス関連のエラーは Python 3.3 からは OSError かそのサブクラスを発生させます (Python 3.3 以前は socket.error を発生させていました)。

> setblocking() メソッドで、非ブロッキングモードを使用することができます。また、より汎用的に settimeout() メソッドでタイムアウトを指定する事ができます。

## [18.1.2. モジュールの内容](https://docs.python.jp/3/library/socket.html#module-contents)

> socket モジュールは以下の要素を公開しています。

### [18.1.2.1. 例外](https://docs.python.jp/3/library/socket.html#exceptions)

属性|概要
----|----
exception socket.error|OSError の非推奨のエイリアスです。
exception socket.herror|OSError のサブクラス。この例外はアドレス関連のエラー、つまり gethostbyname_ex() と gethostbyaddr() などの、 POSIX C API の h_errno を利用する関数のために利用されます。例外に付随する (h_errno, string) ペアはライブラリの呼び出しによって返されたエラーを表します。 h_errno は数値で、 string は、 hstrerror() C関数によって返される h_errno を説明する文字列です。
exception socket.gaierror|OSError のサブクラスです。この例外は getaddrinfo() と getnameinfo() でアドレス関連のエラーが発生した場合に送出されます。例外の値は (error, string) のペアで、ライブラリの呼び出し結果を返します。 string はC関数 gai_strerror() で取得した、 error の意味を示す文字列です。 error の値は、このモジュールで定義される EAI_* 定数のどれかとなります。
exception socket.timeout|OSError のサブクラスです。この例外は、あらかじめ settimeout() を呼び出して (あるいは setdefaulttimeout() を利用して暗黙に) タイムアウトを有効にしてあるソケットでタイムアウトが生じた際に送出されます。 例外に付属する値は文字列で、その内容は現状では常に "timed out" となります。

### [18.1.2.2. 定数](https://docs.python.jp/3/library/socket.html#constants)

> AF_* 定数と SOCK_* 定数は、 AddressFamily と SocketKind IntEnum collection になりました。

属性|概要
----|----
socket.AF_UNIX, socket.AF_INET, socket.AF_INET6|アドレス (およびプロトコル) ファミリーを示す定数で、 socket() の 最初の引数に指定することができます。 AF_UNIX ファミリーをサポート しないプラットフォームでは、 AF_UNIX は未定義となります。システムによってはこれら以外の定数が定義されているかもしれません。
socket.SOCK_STREAM, socket.SOCK_DGRAM, socket.SOCK_RAW, socket.SOCK_RDM, socket.SOCK_SEQPACKET|ソケットタイプを示す定数で、 socket() の2番目の引数に指定することができます。システムによってはこれら以外の定数が定義されているかもしれません。 (ほとんどの場合、 SOCK_STREAM と SOCK_DGRAM 以外は必要ありません。)
socket.SOCK_CLOEXEC, socket.SOCK_NONBLOCK|この2つの定数が定義されていた場合、ソケットタイプと組み合わせていくつかの flags をアトミックに設定することができます (別の呼び出しを不要にして競合状態を避ける事ができます)。 より完全な説明は [Secure File Descriptor Handling](http://udrepper.livejournal.com/20407.html) を参照してください。
SO_*, socket.SOMAXCONN, MSG_*, SOL_*, SCM_*, IPPROTO_*, IPPORT_*, INADDR_*, IP_*, IPV6_*, EAI_*, AI_*, NI_*, TCP_*|Unixのソケット・IPプロトコルのドキュメントで定義されている各種定数。ソケットオブジェクトの setsockopt() や getsockopt() で使用します。ほとんどのシンボルはUnixのヘッダファイルに従っています。一部のシンボルには、デフォルト値を定義してあります。
socket.AF_CAN, socket.PF_CAN, SOL_CAN_*, CAN_*|Linux ドキュメントにあるこの形式の定数は socket モジュールでも定義されています。
socket.CAN_BCM, CAN_BCM_*|CANプロトコルファミリーのCAN_BCMは、ブロードキャストマネージャー(BCM)プロトコルです。Linuxドキュメントにあるこの形式の定数は、socketモジュールでも定義されています。
socket.CAN_RAW_FD_FRAMES|CAN_RAW ソケットで CAN FD をサポートします。これはデフォルトで無効になっています。これにより、アプリケーションが CAN フレームと CAN FD フレームを送信できるようになります。ただし、ソケットからの読み出し時に、CAN と CAN FD の両方のフレームを受け入れなければなりません。
socket.AF_RDS, socket.PF_RDS, socket.SOL_RDS, RDS_*|Linux ドキュメントにあるこの形式の定数は socket モジュールでも定義されています。
socket.SIO_RCVALL, socket.SIO_KEEPALIVE_VALS, socket.SIO_LOOPBACK_FAST_PATH, RCVALL_*|Windows の WSAIoctl() のための定数です。この定数はソケットオブジェクトの ioctl() メソッドに引数として渡されます。
TIPC_*|TIPC 関連の定数で、C のソケットAPIが公開しているものにマッチします。詳しい情報は TIPC のドキュメントを参照してください。
socket.AF_ALG, socket.SOL_ALG, ALG_*|Linux カーネル暗号用の定数です。
socket.AF_LINK|利用できる環境: BSD, OSX.
socket.has_ipv6|現在のプラットフォームでIPv6がサポートされているか否かを示す真偽値。
socket.BDADDR_ANY, socket.BDADDR_LOCAL|これらは、特別な意味を持つ Bluetooth アドレスを含む文字列定数です。例えば、BDADDR_ANY を使用すると、 BTPROTO_RFCOMM で束縛ソケットを指定する際に、任意のアドレスを指し示すことができます。
socket.HCI_FILTER, socket.HCI_TIME_STAMP, socket.HCI_DATA_DIR|BTPROTO_HCI で使用します。 HCI_FILTER は NetBSD または DragonFlyBSD では使用できません。 HCI_TIME_STAMP と HCI_DATA_DIR は FreeBSD, NetBSD, DragonFlyBSD では使用できません。

### [18.1.2.3. 関数](https://docs.python.jp/3/library/socket.html#functions)

#### [18.1.2.3.1. ソケットの作成](https://docs.python.jp/3/library/socket.html#creating-sockets)

以下の関数は全て socket object を生成します。

属性|概要
----|----
socket.socket(family=AF_INET, type=SOCK_STREAM, proto=0, fileno=None)|アドレスファミリー、ソケットタイプ、プロトコル番号を指定して新しいソケットを作成します。アドレスファミリーには AF_INET (デフォルト値)、 AF_INET6 、 AF_UNIX 、 AF_CAN 、または AF_RDS を指定します。ソケットタイプには SOCK_STREAM (デフォルト値)、 SOCK_DGRAM 、 SOCK_RAW 、または他の SOCK_ 定数を指定します。プロトコル番号は通常省略するか、または0を指定しますが、アドレスファミリーに AF_CAN を指定した場合は、プロトコル番号には CAN_RAW か CAN_BCM のいずれかを指定すべきです。fileno を指定した場合、別の引数が無視されるため、指定されたファイル記述子のソケットが返ります。fileno は、socket.fromfd() とは異なり、ソケットの複製ではなく、同一のソケットを返します。このことは、切り離されたソケットを socket.close() で閉じるのに役立つ場合があります。
socket.socketpair([family[, type[, proto]]])|指定されたアドレスファミリー、ソケットタイプ、プロトコル番号から、接続されたソケットオブジェクトのペアを作成します。アドレスファミリー、ソケットタイプ、プロトコル番号は socket() 関数と同様に指定します。デフォルトのアドレスファミリは、プラットフォームで定義されている場合 AF_UNIX 、そうでなければ AF_INET が使われます。
socket.create_connection(address[, timeout[, source_address]])|address ((host, port) ペア) で listen しているTCPサービスに接続し、ソケットオブジェクトを返します。これは socket.connect() を高級にした関数です。 host が数値でないホスト名の場合、 AF_INET と AF_INET6 の両方で名前解決を試み、得られた全てのアドレスに対して成功するまで接続を試みます。この関数を使って IPv4 と IPv6 に両対応したクライアントを簡単に書くことができます。
socket.fromfd(fd, family, type, proto=0)|ファイル記述子 (ファイルオブジェクトの fileno() メソッドが返す整数) fd を複製して、ソケットオブジェクトを構築します。アドレスファミリとプロトコル番号は socket() と同様に指定します。ファイル記述子 はソケットを指していなければなりませんが、実際にソケットであるかどうかのチェックは行っていません。このため、ソケット以外のファイル記述子 を指定するとその後の処理が失敗する場合があります。この関数が必要な事はあまりありませんが、 (Unixのinetデーモンに起動されるプログラムのように) ソケットを標準入力や標準出力として使用するプログラムでソケットオプションの取得や設定を行うために使われます。この関数で使用するソケットは、ブロッキングモードと想定しています。
socket.fromshare(data)|socket.share() メソッドから取得した data からソケットオブジェクトを生成します。ソケットはブロッキングモードだと仮定されます。
socket.SocketType|ソケットオブジェクトの型を示す型オブジェクト。 type(socket(...)) と同じです。

#### [18.1.2.3.2. その他の関数](https://docs.python.jp/3/library/socket.html#other-functions)

> socket モジュールはネットワーク関連のサービスを提供しています:

属性|概要
----|----
socket.getaddrinfo(host, port, family=0, type=0, proto=0, flags=0)|host / port 引数の指すアドレス情報を、そのサービスに接続されたソケットを作成するために必要な全ての引数が入った 5 要素のタプルに変換します。 host はドメイン名、IPv4/v6アドレスの文字列、または None です。 port は 'http' のようなサービス名文字列、ポート番号を表す数値、または None です。 host と port に None を指定すると C APIに NULL を渡せます。
socket.getfqdn([name])|name の完全修飾ドメイン名を返します。 name が空または省略された場合、ローカルホストを指定したとみなします。完全修飾ドメイン名の取得にはまず gethostbyaddr() でチェックし、次に可能であればエイリアスを調べ、名前にピリオドを含む最初の名前を値として返します。完全修飾ドメイン名を取得できない場合、 gethostname() で返されるホスト名を返します。
socket.gethostbyname(hostname)|ホスト名を '100.50.200.5' のようなIPv4形式のアドレスに変換します。ホスト名としてIPv4アドレスを指定した場合、その値は変換せずにそのまま返ります。 gethostbyname() APIへのより完全なインターフェイスが必要であれば、 gethostbyname_ex() を参照してください。 gethostbyname() は、IPv6名前解決をサポートしていません。IPv4/ v6のデュアルスタックをサポートする場合は getaddrinfo() を使用します。
socket.gethostbyname_ex(hostname)|ホスト名から、IPv4形式の各種アドレス情報を取得します。戻り値は (hostname, aliaslist, ipaddrlist) のタプルで、 hostname は ip_address で指定したホストの正式名、 aliaslist は同じアドレスの別名のリスト(空の場合もある)、 ipaddrlist は同じホスト上の同一インターフェイスのIPv4アドレスのリスト(ほとんどの場合は単一のアドレスのみ) を示します。 gethostbyname_ex() は、IPv6名前解決をサポートしていません。IPv4/v6のデュアルスタックをサポートする場合は getaddrinfo() を使用します。
socket.gethostname()|Pythonインタープリタを現在実行しているマシンのホスト名を含む文字列を返します。
socket.gethostbyaddr(ip_address)|(hostname, aliaslist, ipaddrlist) のタプルを返し、 hostname は ip_address で指定したホストの正式名、 aliaslist は同じアドレスの別名のリスト(空の場合もある)、 ipaddrlist は同じホスト上の同一インターフェイスのIPv4アドレスのリスト(ほとんどの場合は単一のアドレスのみ)を示します。完全修飾ドメイン名が必要であれば、 getfqdn() を使用してください。 gethostbyaddr() は、IPv4/IPv6の両方をサポートしています。
socket.getnameinfo(sockaddr, flags)|ソケットアドレス sockaddr から、 (host, port) のタプルを取得します。 flags の設定に従い、 host は完全修飾ドメイン名または数値形式アドレスとなります。同様に、 port は文字列のポート名または数値のポート番号となります。
socket.getprotobyname(protocolname)|('icmp' のような) インターネットプロトコル名を、 socket() の 第三引数として指定する事ができる定数に変換します。これは主にソケットを "raw" モード(SOCK_RAW)でオープンする場合には必要ですが、通常の ソケットモードでは第三引数に0を指定するか省略すれば正しいプロトコルが自動的に選択されます。
socket.getservbyname(servicename[, protocolname])|インターネットサービス名とプロトコルから、そのサービスのポート番号を取得します。省略可能なプロトコル名として、 'tcp' か 'udp' のどちらかを指定することができます。指定がなければどちらのプロトコルにもマッチします。
socket.getservbyport(port[, protocolname])|インターネットポート番号とプロトコル名から、サービス名を取得します。省略可能なプロトコル名として、 'tcp' か 'udp' のどちらかを指定することができます。指定がなければどちらのプロトコルにもマッチします。
socket.ntohl(x)|32ビットの正の整数のバイトオーダを、ネットワークバイトオーダからホストバイトオーダに変換します。ホストバイトオーダとネットワークバイトオーダが一致するマシンでは、この関数は何もしません。それ以外の場合は4バイトのスワップを行います。
socket.ntohs(x)|16ビットの正の整数のバイトオーダを、ネットワークバイトオーダからホストバイトオーダに変換します。ホストバイトオーダとネットワークバイトオーダが一致するマシンでは、この関数は何もしません。それ以外の場合は2バイトのスワップを行います。
socket.htonl(x)|32ビットの正の整数のバイトオーダを、ホストバイトオーダからネットワークバイトオーダに変換します。ホストバイトオーダとネットワークバイトオーダが一致するマシンでは、この関数は何もしません。それ以外の場合は4バイトのスワップを行います。
socket.htons(x)|16ビットの正の整数のバイトオーダを、ホストバイトオーダからネットワークバイトオーダに変換します。ホストバイトオーダとネットワークバイトオーダが一致するマシンでは、この関数は何もしません。それ以外の場合は2バイトのスワップを行います。
socket.inet_aton(ip_string)|ドット記法によるIPv4アドレス('123.45.67.89' など)を32ビットにパックしたバイナリ形式に変換し、長さ4のバイト列オブジェクトとして返します。この関数が返す値は、標準Cライブラリの struct in_addr 型を使用する関数に渡す事ができます。
socket.inet_ntoa(packed_ip)|32 ビットにパックされた IPv4 アドレス (長さ 4 バイトの bytes-like object) を、標準的なドット記法による 4 桁の文字列 ('123.45.67.89' など) に変換します。この関数は、struct in_addr 型を使用する標準 C ライブラリのプログラムとやりとりする場合に便利です。struct in_addr 型は、この関数が引数として受け取る 32 ビットにパックされたバイナリデータに対する C の型です。
socket.inet_pton(address_family, ip_string)|IPアドレスを、アドレスファミリ固有の文字列からパックしたバイナリ形式に変換します。 inet_pton() は、 struct in_addr 型 (inet_aton() と同様)や struct in6_addr を使用するライブラリやネットワークプロトコルを呼び出す際に使用することができます。
socket.inet_ntop(address_family, packed_ip)|パックしたIPアドレス (数バイトからなる bytes-like オブジェクト ) を、 '7.10.0.5' や '5aef:2b::8' などの標準的な、アドレスファミリ固有の文字列形式に変換します。 inet_ntop() は (inet_ntoa() と同様に)、 struct in_addr 型や struct in6_addr 型のオブジェクトを返すライブラリやネットワークプロトコル等で使用することができます。
socket.CMSG_LEN(length)|指定された length にある制御メッセージ（CMSG）から、末尾のパディングを除いた全体の長さを返します。この値は多くの場合、 recvmsg() が制御メッセージの一連の要素を受信するためのバッファサイズとして使用できますが、バッファの末尾が要素である場合であってもパディングは含まれるので、バッファサイズを取得するには RFC 3542 で求められているように、 CMSG_SPACE() を使用した移植可能なアプリケーションが必要です。通常 length は定数であり、許容範囲外の値が指定された場合は OverflowError 例外が送出されます。
socket.CMSG_SPACE(length)|指定された length の制御メッセージ（CMSG）の要素を recvmsg() が受信するために必要な、パディングを含めたバッファサイズを返します。複数の項目を受信するために必要なバッファスペースは、 CMSG_SPACE() が返すそれぞれの要素の長さの合計です。通常 length は定数であり、許容範囲外の値が指定された場合は OverflowError 例外が送出されます。
socket.getdefaulttimeout()|新規に生成されたソケットオブジェクトの、デフォルトのタイムアウト値を浮動小数点形式の秒数で返します。タイムアウトを使用しない場合には None を返します。最初に socket モジュールがインポートされた時の初期値は None です。
socket.setdefaulttimeout(timeout)|新規に生成されるソケットオブジェクトの、デフォルトのタイムアウト値を秒数 (float 型) で設定します。最初に socket モジュールがインポートされた時の初期値は None です。指定可能な値とその意味については settimeout() メソッドを参照してください。
socket.sethostname(name)|マシンのホスト名を name に設定します。必要な権限がない場合は OSError を送出します。
socket.if_nameindex()|ネットワークインターフェイス情報 (index int, name string)のタプルを返します。システムコールが失敗した場合、 OSError 例外を送出します。
socket.if_nametoindex(if_name)|インターフェイス名 if_name に対応するネットワークインターフェイスのインデックス番号を返します。対応するインターフェースが存在しない場合は OSError 例外を送出します。
socket.if_indextoname(if_index)|インターフェイスインデックス番号 if_index に対応するネットワークインターフェイス名を返します。対応するインターフェイスが存在しない場合は OSError 例外を送出します。

## [18.1.3. socket オブジェクト](https://docs.python.jp/3/library/socket.html#socket-objects)

> ソケットオブジェクトは以下のメソッドを持ちます。 makefile() 以外のメソッドは、Unixのソケット用システムコールに対応しています。

> バージョン 3.2 で変更: context manager プロトコルのサポートが追加されました。コンテキストマネージャを終了することは、 close() を呼ぶことと同一です。

属性|概要
----|----
socket.accept()|接続を受け付けます。ソケットはアドレスにbind済みで、listen中である必要があります。戻り値は (conn, address) のペアで、 conn は接続を通じてデータの送受信を行うための 新しい ソケットオブジェクト、 address は接続先でソケットにbindしているアドレスを示します。
socket.bind(address)|ソケットを address にbindします。bind済みのソケットを再バインドする事はできません。(address のフォーマットはアドレスファミリによって異なります – 前述。)
socket.close()|ソケットを閉じられたものとしてマークします。 makefile() が返したファイルオブジェクトを閉じる時、対応する下層のシステムリソース（例：ファイル記述子）もすべて閉じます。一度この操作をすると、その後、このソケットオブジェクトに対するすべての操作が失敗します。キューに溜まったデータがフラッシュされた後は、リモート側の端点ではそれ以上のデータを受信しません。
socket.connect(address)|address で示されるリモートソケットに接続します。(address のフォーマットはアドレスファミリによって異なります — 前述。)
socket.connect_ex(address)|connect(address) と同様ですが、C言語の connect() 関数の呼び出しでエラーが発生した場合には例外を送出せずにエラーを戻り値として返します。(これ以外の、"host not found,"等のエラーの場合には例外が発生します。)処理が正常に終了した場合には 0 を返し、エラー時には errno の値を返します。この関数は、非同期接続をサポートする場合などに使用することができます。
socket.detach()|実際にファイル記述子を閉じることなく、ソケットオブジェクトを閉じた状態にします。ファイル記述子は返却され、他の目的に再利用することができます。
socket.dup()|ソケットを複製します。
socket.fileno()|ソケットのファイル記述子を短い整数型で返します。失敗時には、-1 を返します。ファイル記述子は、 select.select() などで使用します。
socket.get_inheritable()|ソケットのファイル記述子またはソケットのハンドルの 継承可能フラグ を取得します。ソケットが子プロセスへ継承可能なら True 、継承不可なら False を返します。
socket.getpeername()|ソケットが接続しているリモートアドレスを返します。この関数は、リモート IPv4/v6ソケットのポート番号を調べる場合などに使用します。 address のフォーマットはアドレスファミリによって異なります(前述)。この関数をサポートしていないシステムも存在します。
socket.getsockname()|ソケット自身のアドレスを返します。この関数は、IPv4/v6ソケットのポート番号を調べる場合などに使用します。(address のフォーマットはアドレスファミリによって異なります — 前述。)
socket.getsockopt(level, optname[, buflen])|ソケットに指定されたオプションを返します(Unixのマニュアルページ getsockopt(2) を参照)。 SO_* 等のシンボルは、このモジュールで定義しています。 buflen を省略した場合、取得するオブションは整数とみなし、整数型の値を戻り値とします。 buflen を指定した場合、長さ buflen のバッファでオプションを受け取り、このバッファをバイト列オブジェクトとして返します。このバッファは、呼び出し元プログラムで struct モジュール等を利用して内容を読み取ることができます。
socket.gettimeout()|ソケットに指定されたタイムアウト値を取得します。タイムアウト値が設定されている場合には浮動小数点型で秒数が、設定されていなければ None が返ります。この値は、最後に呼び出された setblocking() または settimeout() によって設定されます。

socket.ioctl(control, option)|プラットフォーム:	Windows  ioctl() メソッドは WSAIoctl システムインタフェースへの制限されたインタフェースです。詳しい情報については、 Win32 documentation を参照してください。
socket.listen([backlog])|サーバーを有効にして、接続を受け付けるようにします。backlog が指定されている場合、少なくとも 0 以上でなければなりません (それより低い場合、0 に設定されます)。システムが新しい接続を拒否するまでに許可する未受付の接続の数を指定します。指定しない場合、デフォルトの妥当な値が選択されます。
socket.makefile(mode='r', buffering=None, *, encoding=None, errors=None, newline=None)|ソケットに関連付けられた ファイルオブジェクト を返します。戻り値の正確な型は、 makefile() に指定した引数によります。これらの引数は、組み込み関数 open() の引数と同様に解釈されます。ただし、mode の値は 'r' (デフォルト), 'w', 'b' のみがサポートされています。
socket.recv(bufsize[, flags])|ソケットからデータを受信し、結果を bytes オブジェクトで返します。一度に受信するデータは、最大でも bufsize で指定した量です。オプション引数 flags に指定するフラグの意味については、 Unix のマニュアルページ recv(2) を参照してください。 flags のデフォルトは 0 です。
socket.recvfrom(bufsize[, flags])|ソケットからデータを受信し、結果をタプル (bytes, address) として返します。 bytes は受信データの bytes オブジェクトで、 address は送信元のアドレスを示します。オプション引数 flags については、 Unix のマニュアルページ recv(2) を参照してください。デフォルトは0です。 (address のフォーマットはアドレスファミリによって異なります(前述))
socket.recvmsg(bufsize[, ancbufsize[, flags]])|ソケットから通常のデータ (最大 bufsize バイト) と補助的なデータを受信します。ancbufsize 引数により、補助的なデータの受信に使用される内部バッファのバイト数として、サイズが設定されます。このデフォルトは 0 で、補助的なデータを受信しないことを意味します。CMSG_SPACE() または CMSG_LEN() を使用して、補助的なデータの適切なサイズを計算することができ、バッファ内に収まらないアイテムは、短縮されるか破棄されます。flags 引数はデフォルトでは 0 で、recv() での意味と同じ意味を持ちます。
socket.recvmsg_into(buffers[, ancbufsize[, flags]])|recvmsg() と同様に動作してソケットから通常のデータと付属的なデータを受信しますが、非付属的データは新しいバイトオブジェクトとして返すのではなく、一連のバッファとして返します。buffers 引数は書き込み可能なバッファをエクスポートするオブジェクトのイテラブルでなければなりません (例: bytearray オブジェクト)。これらは、全てに書き込まれるか、残りバッファがなくなるまで、非付属的データの連続チャンクで埋められます。オペレーティングシステムによって、使用できるバッファの数が制限 (sysconf() 値 SC_IOV_MAX) されている場合があります。ancbufsize 引数と flags 引数は、recvmsg() での意味と同じ意味を持ちます。
socket.recvfrom_into(buffer[, nbytes[, flags]])|ソケットからデータを受信し、そのデータを新しいバイト文字列として返す代わりに buffer に書きます。戻り値は (nbytes, address) のペアで、 nbytes は受信したデータのバイト数を、 address はデータを送信したソケットのアドレスです。オプション引数 flags (デフォルト:0) の意味については、 Unix マニュアルページ recv(2) を参照してください。(address のフォーマットは前述のとおりアドレスファミリーに依存します。)
socket.recv_into(buffer[, nbytes[, flags]])|nbytes バイトまでのデータをソケットから受信して、そのデータを新しいバイト文字列にするのではなく buffer に保存します。 nbytes が指定されない(あるいは0が指定された)場合、 buffer の利用可能なサイズまで受信します。受信したバイト数を返り値として返します。オプション引数 flags (デフォルト:0) の意味については、 Unix マニュアルページ recv(2) を参照してください。
socket.send(bytes[, flags])|ソケットにデータを送信します。ソケットはリモートソケットに接続済みでなければなりません。オプション引数 flags の意味は、上記 recv() と同じです。戻り値として、送信したバイト数を返します。アプリケーションでは、必ず戻り値をチェックし、全てのデータが送られた事を確認する必要があります。データの一部だけが送信された場合、アプリケーションで残りのデータを再送信してください。 ソケットプログラミング HOWTO に、さらに詳しい情報があります。
socket.sendall(bytes[, flags])|ソケットにデータを送信します。ソケットはリモートソケットに接続済みでなければなりません。オプション引数 flags の意味は、上記 recv() と同じです。 send() と異なり、このメソッドは bytes の全データを送信するか、エラーが発生するまで処理を継続します。正常終了の場合は None を返し、エラー発生時には例外が発生します。エラー発生時、送信されたバイト数を調べる事はできません。
socket.sendto(bytes, address), socket.sendto(bytes, flags, address)|ソケットにデータを送信します。このメソッドでは接続先を address で指定するので、接続済みではいけません。オプション引数 flags の意味は、上記 recv() と同じです。戻り値として、送信したバイト数を返します。(address のフォーマットはアドレスファミリによって異なります — 前述。)
socket.sendmsg(buffers[, ancdata[, flags[, address]]])|非付属的なデータを一連のバッファから集め、単一のメッセージにまとめることで、通常のデータと付属的なデータをソケットに送信します。buffers 引数は、非付属的なデータを bytes-like objects (例: bytes オブジェクト) のイテラブルとして指定します。オペレーティングシステムによって、使用できるバッファの数が制限 (sysconf() 値 SC_IOV_MAX) されている場合があります。ancdata 引数は付属的なデータ (制御メッセージ) をゼロ以上のタプル (cmsg_level, cmsg_type, cmsg_data) のイテラブルとして指定します。ここで、cmsg_level と cmsg_type はそれぞれプロトコルレベルとプロトコル固有のタイプを指定する整数で、cmsg_data は関連データを保持するバイトライクオブジェクトです。一部のシステム (特に CMSG_SPACE() を持たないシステム) では、一度の呼び出しで一つの制御メッセージの送信しかサポートされていない場合があります。flags 引数のデフォルトは 0 であり、send() での意味と同じ意味を持ちます。None 以外の address が渡された場合、メッセージの目的地のアドレスを設定します。戻り値は、送信された非付属的データのバイト数です。
socket.sendmsg_afalg([msg, ]*, op[, iv[, assoclen[, flags]]])|sendmsg() の AF_ALG ソケット用に特化したバージョンです。AF_ALG ソケットの、モード、IV、AEAD に関連づけられたデータ長、フラグを設定します。
socket.sendfile(file, offset=0, count=None)|高性能の os.sendfile を使用して、ファイルを EOF まで送信し、送信されたバイトの総数を返します。file は、バイナリモードで開かれた標準的なファイルオブジェクトです。os.sendfile が使用できない場合 (例: Windows)、または file が標準的なファイルでない場合、代わりに send() が使用されます。offset は、ファイルの読み出し開始位置を指定します。count が指定されている場合、ファイルを EOF まで送信するのではなく、転送するバイトの総数を指定します。ファイルの位置は、返る時に更新されます。あるいは、エラー時には file.tell()  を使用して送信されたバイトの数を確認することができます。ソケットは SOCK_STREAM タイプでなければなりません。非ブロックソケットはサポートされていません。
socket.set_inheritable(inheritable)|ソケットのファイル記述子、またはソケットのハンドルの、 継承可能フラグ を立てます。
socket.setblocking(flag)|ソケットをブロッキングモード、または非ブロッキングモードに設定します。flag が False の場合にはソケットは非ブロッキングモードになり、True の場合にはブロッキングモードになります。
socket.settimeout(value)|ブロッキングソケットの処理のタイムアウト値を指定します。 value には float 型で非負の秒数を指定するか、 None を指定します。ゼロ以外の値を指定した場合、ソケットの処理が完了する前に value で指定した秒数が経過すれば timeout 例外を送出します。ゼロを指定した場合、ソケットは非ブロッキングモード状態に置かれます。 None を指定した場合、ソケットのタイムアウトを無効にします。
socket.setsockopt(level, optname, value: int), socket.setsockopt(level, optname, value: buffer), socket.setsockopt(level, optname, None, optlen: int)|指定されたソケットオプションの値を設定します (Unix のマニュアルページ setsockopt(2) を参照)。必要なシンボリック定数は、socket モジュール (SO_* など) で定義されています。この値は、整数、None、またはバッファを表す bytes-like object のいずれかです。バイトライクオブジェクトの場合、バイト文字列に適切なビットが含まれていることを確認するのは呼び出し元の仕事です (C 構造をバイト文字列としてエンコードする方法については、オプションの組み込みモジュール struct を参照)。値が None に設定されている場合、optlen 引数が必須です。これは、optval=NULL と optlen=optlen で setsockopt C 関数を呼び出すのと同一です。
socket.shutdown(how)|接続の片方向、または両方向を切断します。 how が SHUT_RD の場合、以降は受信を行えません。 how が SHUT_WR の場合、以降は送信を行えません。 how が SHUT_RDWR の場合、以降は送受信を行えません。
socket.share(process_id)|ソケットを複製し、対象のプロセスと共有するための bytes オブジェクトを返します。対象のプロセスを process_id で指定しなければなりません。戻り値の bytes オブジェクトは、何らかのプロセス間通信を使って対象のプロセスに伝えます。対象のプロセス側では、 fromshare() を使って複製されたソケットをとらえます。オペレーティング・システムは対象のプロセスに対してソケットを複製するため、このメソッドを呼び出した後であれば、元のソケットをクローズしても、対象のプロセスに渡ったソケットには影響がありません。
socket.family|ソケットファミリー。
socket.type|ソケットタイプ。
socket.proto|ソケットプロトコル。

## [18.1.4. ソケットタイムアウトの注意事項](https://docs.python.jp/3/library/socket.html#notes-on-socket-timeouts)

> ソケットオブジェクトは、ブロッキングモード、非ブロッキングモード、タイムアウトモードのうち、いずれか1つのモードをとります。デフォルトでは、ソケットは常にブロッキングモードで作成されますが、 setdefaulttimeout() で標準のモードを変更することができます。

* ブロッキングモード での操作は、完了するか、または（接続がタイムアウトするなどして）システムがエラーを返すまで、ブロックされます。
* 非ブロッキングモード での操作は、ただちに完了できない場合、例外を送出して失敗します。この場合の例外の種類は、システムに依存するため、ここに記すことができません。 select モジュールの関数を使って、ソケットの読み書きが利用可能かどうか、可能な場合はいつ利用できるかを調べることができます。 タイムアウトモード での操作は、指定されたタイムアウトの時間内に完了しなければ、 timeout 例外を送出します。タイムアウトの時間内にシステムがエラーを返した場合は、そのエラーを返します。

### 注釈

オペレーティング・システムのレベルでは、 タイムアウトモード のソケットには、内部的に非ブロッキングモードが設定されています。またブロッキングモードとタイムアウトモードの指定は、ファイル記述子と、「そのファイル記述子と同じネットワーク端点を参照するソケットオブジェクト」との間で共有されます。このことは、例えばソケットの fileno() を使うことにした場合に、明らかな影響を与えます。

### [18.1.4.1. タイムアウトと connect メソッド](https://docs.python.jp/3/library/socket.html#timeouts-and-the-connect-method)

connect() もタイムアウト設定に従います。一般的に、 settimeout() を connect() の前に呼ぶか、 create_connection() にタイムアウト引数を渡すことが推奨されます。ただし、システムのネットワークスタックが Python のソケットタイムアウトの設定を無視して、自身の接続タイムアウトエラーを返すこともあります。

### [18.1.4.2. タイムアウトと accept メソッド](https://docs.python.jp/3/library/socket.html#timeouts-and-the-accept-method)

getdefaulttimeout() が None でない場合、 accept() メソッドが返すソケットでは、そのタイムアウトが継承されます。 None である場合、待機中のソケットの設定によって動作は異なります。

* 待機中のソケットが ブロッキングモード または タイムアウトモード である場合、accept() が返すソケットは、ブロッキングモード になります。
* 待機中のソケットが 非ブロッキングモード である場合、accept() が返すソケットは、オペレーティングシステムによってブロッキングモードまたは非ブロッキングモードになります。クロスプラットフォームの動作を確保したい場合、この設定を手動でオーバーライドすることをお勧めします。

## [18.1.5. 使用例](https://docs.python.jp/3/library/socket.html#example)

> 以下は TCP/IP プロトコルの簡単なサンプルとして、受信したデータをクライアントにそのまま返送するサーバ (接続可能なクライアントは一件のみ) と、サーバに接続するクライアントの例を示します。サーバでは、 socket() ・ bind() ・ listen() ・ accept() を実行し (複数のクライアントからの接続を受け付ける場合、 accept() を複数回呼び出します)、クライアントでは socket() と connect() だけを呼び出しています。サーバでは sendall() / recv() メソッドは listen 中のソケットで実行するのではなく、 accept() で取得したソケットに対して実行している点にも注意してください。

> 次のクライアントとサーバは、IPv4 のみをサポートしています。

```python
# Echo server program
import socket

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data: break
            conn.sendall(data)
```

```python
# Echo client program
import socket

HOST = 'daring.cwi.nl'    # The remote host
PORT = 50007              # The same port as used by the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b'Hello, world')
    data = s.recv(1024)
print('Received', repr(data))
```

> 次のサンプルは上記のサンプルとほとんど同じですが、IPv4 と IPv6 の両方をサポートしています。サーバでは、IPv4/v6 の両方ではなく、利用可能な最初のアドレスファミリだけを listen しています。ほとんどの IPv6 対応システムでは IPv6 が先に現れるため、サーバは IPv4 には応答しません。クライアントでは名前解決の結果として取得したアドレスに順次接続を試み、最初に接続に成功したソケットにデータを送信しています。

```python
# Echo server program
import socket
import sys

HOST = None               # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC,
                              socket.SOCK_STREAM, 0, socket.AI_PASSIVE):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.bind(sa)
        s.listen(1)
    except OSError as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
conn, addr = s.accept()
with conn:
    print('Connected by', addr)
    while True:
        data = conn.recv(1024)
        if not data: break
        conn.send(data)
```

```python
# Echo client program
import socket
import sys

HOST = 'daring.cwi.nl'    # The remote host
PORT = 50007              # The same port as used by the server
s = None
for res in socket.getaddrinfo(HOST, PORT, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        s = socket.socket(af, socktype, proto)
    except OSError as msg:
        s = None
        continue
    try:
        s.connect(sa)
    except OSError as msg:
        s.close()
        s = None
        continue
    break
if s is None:
    print('could not open socket')
    sys.exit(1)
with s:
    s.sendall(b'Hello, world')
    data = s.recv(1024)
print('Received', repr(data))
```

> 次の例は、Windowsで raw socket を利用して非常にシンプルなネットワークスニファーを書きます。このサンプルを実行するには、インタフェースを操作するための管理者権限が必要です:

```python
import socket

# the public network interface
HOST = socket.gethostbyname(socket.gethostname())

# create a raw socket and bind it to the public interface
s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
s.bind((HOST, 0))

# Include IP headers
s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

# receive all packages
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

# receive a package
print(s.recvfrom(65565))

# disabled promiscuous mode
s.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
```

> 最後の例では、ソケットインターフェイスを使用してローソケットプロトコルを使用する CAN ネットワークと通信する方法を説明します。ブロードキャストマネージャプロトコロルで CAN を使用するには、以下でソケットを開きます。

```python
socket.socket(socket.AF_CAN, socket.SOCK_DGRAM, socket.CAN_BCM)
```

> ソケットの束縛 (CAN_RAW) または (CAN_BCM) 接続を行ったあと、ソケットオブジェクトで socket.send() と socket.recv() 操作 (とそのカウンターパート) を通常通りに使用することができます。

> 次の例では、特権が必要になるかもしれません:

```python
import socket
import struct


# CAN frame packing/unpacking (see 'struct can_frame' in <linux/can.h>)

can_frame_fmt = "=IB3x8s"
can_frame_size = struct.calcsize(can_frame_fmt)

def build_can_frame(can_id, data):
    can_dlc = len(data)
    data = data.ljust(8, b'\x00')
    return struct.pack(can_frame_fmt, can_id, can_dlc, data)

def dissect_can_frame(frame):
    can_id, can_dlc, data = struct.unpack(can_frame_fmt, frame)
    return (can_id, can_dlc, data[:can_dlc])


# create a raw socket and bind it to the 'vcan0' interface
s = socket.socket(socket.AF_CAN, socket.SOCK_RAW, socket.CAN_RAW)
s.bind(('vcan0',))

while True:
    cf, addr = s.recvfrom(can_frame_size)

    print('Received: can_id=%x, can_dlc=%x, data=%s' % dissect_can_frame(cf))

    try:
        s.send(cf)
    except OSError:
        print('Error sending CAN frame')

    try:
        s.send(build_can_frame(0x01, b'\x01\x02\x03'))
    except OSError:
        print('Error sending CAN frame')
```

> この例を、ほとんど間を空けずに複数回実行すると、以下のエラーが発生する場合があります:

```sh
OSError: [Errno 98] Address already in use
```

> これは以前の実行がソケットを TIME_WAIT 状態のままにし、すぐには再利用できないことで起こります。

> これを防ぐのに、 socket フラグの socket.SO_REUSEADDR があります:

```python
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
```

> SO_REUSEADDR フラグは、 TIME_WAIT 状態にあるローカルソケットをそのタイムアウト期限が自然に切れるのを待つことなく再利用することをカーネルに伝えます。

#### 参考

> C 言語によるソケットプログラミングの基礎については、以下の資料を参照してください。

* An Introductory 4.3BSD Interprocess Communication Tutorial, by Stuart Sechrest
* An Advanced 4.3BSD Interprocess Communication Tutorial, by Samuel J. Leffler et al,

> 両書とも UNIX Programmer’s Manual, Supplementary Documents 1 (PS1:7章 PS1:8章)。ソケットの詳細については、各プラットフォームのソケット関連システムコールに関するドキュメントも参照してください。Unix ではマニュアルページ、WindowsではWinSock (または WinSock2) 仕様書をご覧ください。IPv6 対応の API については、 RFC 3493 "Basic Socket Interface Extensions for IPv6" を参照してください。

