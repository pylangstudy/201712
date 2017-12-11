# [17.8. dummy_threading — threading の代替モジュール](https://docs.python.jp/3/library/dummy_threading.html)

< [17. 並行実行](https://docs.python.jp/3/library/concurrency.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

ソースコード: [Lib/dummy_threading.py](https://github.com/python/cpython/tree/3.6/Lib/dummy_threading.py)

> このモジュールは threading モジュールのインターフェースをそっくりまねるものです。 _thread モジュールがサポートされていないプラットフォームで import することを意図して作られたものです。

> おすすめの使い道は:

```python
try:
    import threading
except ImportError:
    import dummy_threading as threading
```

> 生成するスレッドが、他のブロックしたスレッドを待ち、デッドロック発生の可能性がある場合には、このモジュールを使わないようにしてください。ブロッキング I/O を使っている場合によく起きます。

