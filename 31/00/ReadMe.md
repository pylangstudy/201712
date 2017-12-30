# [18.9. mmap — メモリマップファイル](https://docs.python.jp/3/library/mmap.html)

< [18. プロセス間通信とネットワーク](https://docs.python.jp/3/library/ipc.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

> メモリにマップされたファイルオブジェクトは、 bytearray と ファイルオブジェクト の両方のように振舞います。しかし通常の文字列オブジェクトとは異なり、これらは可変です。 bytearray が期待されるほとんどの場所で mmap オブジェクトを利用できます。例えば、メモリマップファイルを探索するために re モジュールを使うことができます。それらは可変なので、 obj[index] = 97 のように文字を変換できますし、スライスを使うことで obj[i1:i2] = b'...' のように部分文字列を変換することができます。現在のファイル位置をデータの始めとする読込みや書込み、ファイルの異なる位置へ seek() することもできます。

> メモリマップドファイルは Unix と Windows で異なる mmap コンストラクタで生成されます。どちらの場合も、更新用に開かれたファイルディスクリプタを渡さなければなりません。既存の Python ファイルオブジェクトをマップしたければ、 fileno() メソッドを使って fileno パラメータの正しい値を取得してください。そうでなければ、 os.open() 関数を使ってファイルを開けます。この関数はファイルディスクリプタを直接返します(処理が終わったら、やはりファイルを閉じる必要があります)。

> 注釈

> 書き込み可能でバッファされたファイルへのメモリマップファイルを作りたいのであれば、まず最初にファイルの flush() を呼び出すべきです。これはバッファへのローカルな修正がマッピングで実際に利用可能になることを保障するために必要です。

> Unix バージョンと Windows バージョンのどちらのコンストラクタについても、オプションのキーワード・パラメータとして access を指定することになるかもしれません。 access は3つの値の内の1つを受け入れます。 ACCESS_READ は読み出し専用、 ACCESS_WRITE は書き込み可能、 ACCESS_COPY はコピーした上での書き込みです。 access は Unix と Windows の両方で使用することができます。 access が指定されない場合、 Windows の mmap は書き込み可能マップを返します。 3つのアクセス型すべてに対する初期メモリ値は、指定されたファイルから得られます。 ACCESS_READ 型のメモリマップに対して書き込むと TypeError 例外を送出します。 ACCESS_WRITE 型のメモリマップへの書き込みはメモリと元のファイルの両方に影響を与えます。 ACCESS_COPY 型のメモリマップへの書き込みはメモリに影響を与えますが、元のファイルを更新することはありません。

> 無名メモリ(anonymous memory)にマップするためには fileno として -1 を渡し、length を与えてください。

属性|概要
----|----
class mmap.mmap(fileno, length, tagname=None, access=ACCESS_DEFAULT[, offset])|(Windows バージョン) ファイルハンドル fileno によって指定されたファイルから length バイトをマップして、 mmap オブジェクトを生成します。 length が現在のファイルサイズより大きな場合、ファイルサイズは length を含む大きさにまで拡張されます。 length が 0 の場合、マップの最大の長さは現在のファイルサイズになります。ただし、ファイル自体が空のときは Windows が例外を送出します (Windows では空のマップを作成することができません)。
class mmap.mmap(fileno, length, flags=MAP_SHARED, prot=PROT_WRITE|PROT_READ, access=ACCESS_DEFAULT[, offset])|(Unix バージョン) ファイルディスクリプタ fileno で指定されたファイルから length バイトをマップし、mmap オブジェクトを返します。length が 0 の場合、マップの最大の長さは mmap が呼ばれた時点でのファイルサイズになります。
close()|メモリマップファイルを閉じます。この呼出しの後にオブジェクトの他のメソッドの呼出すことは、 ValueError 例外の送出を引き起こします。このメソッドは開いたファイルのクローズはしません。
closed|ファイルが閉じている場合 True となります。
find(sub[, start[, end]])|オブジェクト内の [start, end] の範囲に含まれている部分シーケンス sub が見つかった場所の最も小さいインデックスを返します。オプションの引数 start と end はスライスに使われるときのように解釈されます。失敗したときには -1 を返します。
flush([offset[, size]])|ファイルのメモリコピー内での変更をディスクへフラッシュします。この呼出しを使わなかった場合、オブジェクトが破壊される前に変更が書き込まれる保証はありません。もし offset と size が指定された場合、与えられたバイトの範囲の変更だけがディスクにフラッシュされます。指定されない場合、マップ全体がフラッシュされます。
move(dest, src, count)|オフセット src から始まる count バイトをインデックス dest の位置へコピーします。もし mmap が ACCESS_READ で作成されていた場合、 TypeError 例外を発生させます。
read([n])|現在のファイル位置からの最大 n バイトを含む bytes を返します。引数が省略されるか、 None もしくは負の値が指定された場合、現在のファイル位置からマップ終端までの全てのバイト列を返します。ファイル位置は返されたバイト列の直後を指すように更新されます。
read_byte()|現在のファイル位置のバイトを整数値として返し、ファイル位置を 1 進めます。
readline()|現在のファイル位置から次の改行までの、1行を返します。
resize(newsize)|マップと元ファイル(がもしあれば)のサイズを変更します。もし mmap が ACCESS_READ または ACCESS_COPY で作成されたならば、マップサイズの変更は TypeError 例外を発生させます。
rfind(sub[, start[, end]])|オブジェクト内の [start, end] の範囲に含まれている部分シーケンス sub が見つかった場所の最も大きいインデックスを返します。オプションの引数 start と end はスライスに使われるときのように解釈されます。失敗したときには -1 を返します。
seek(pos[, whence])|ファイルの現在位置をセットします。 whence 引数はオプションであり、デフォルトは os.SEEK_SET つまり 0 (絶対位置)です。その他の値として、 os.SEEK_CUR つまり 1 (現在位置からの相対位置)と os.SEEK_END つまり 2 (ファイルの終わりからの相対位置)があります。
size()|ファイルの長さを返します。メモリマップ領域のサイズより大きいかもしれません。
tell()|ファイルポインタの現在位置を返します。
write(bytes)|メモリ内のファイルポイントの現在位置に bytes のバイト列を書き込み、書き込まれたバイト数を返します(もし書き込みが失敗したら ValueError が送出されるため、len(bytes) より少なくなりません)。ファイル位置はバイト列が書き込まれた位置に更新されます。もしmmapが:const:ACCESS_READ とともに作成されていた場合は、書き込みは TypeError 例外を送出するでしょう。
write_byte(byte)|メモリ内のファイル・ポインタの現在位置に整数 byte を書き込みます。ファイル位置は 1 だけ進みます。もし mmap が ACCESS_READ で作成されていた場合、書き込み時に TypeError 例外を発生させるでしょう。

> この例は mmap の簡潔な使い方を示すものです:

```python
import mmap

# write a simple example file
with open("hello.txt", "wb") as f:
    f.write(b"Hello Python!\n")

with open("hello.txt", "r+b") as f:
    # memory-map the file, size 0 means whole file
    mm = mmap.mmap(f.fileno(), 0)
    # read content via standard file methods
    print(mm.readline())  # prints b"Hello Python!\n"
    # read content via slice notation
    print(mm[:5])  # prints b"Hello"
    # update content using slice notation;
    # note that new content must have same size
    mm[6:] = b" world!\n"
    # ... and read again using standard file methods
    mm.seek(0)
    print(mm.readline())  # prints b"Hello  world!\n"
    # close the map
    mm.close()
```

> mmap は with 文の中でコンテキストマネージャとしても使えます:

```python
import mmap

with mmap.mmap(-1, 13) as mm:
    mm.write(b"Hello world!")
```

バージョン 3.2 で追加: コンテキストマネージャのサポート。

次の例では無名マップを作り親プロセスと子プロセスの間でデータのやりとりをしてみせます:

```python
import mmap
import os

mm = mmap.mmap(-1, 13)
mm.write(b"Hello world!")

pid = os.fork()

if pid == 0:  # In a child process
    mm.seek(0)
    print(mm.readline())

    mm.close()
```

