# [17.10. _dummy_thread — _thread の代替モジュール](https://docs.python.jp/3/library/_dummy_thread.html)

< [17. 並行実行](https://docs.python.jp/3/library/concurrency.html) < [Python 標準ライブラリ](https://docs.python.jp/3/library/index.html#the-python-standard-library) < [ドキュメント](https://docs.python.jp/3/index.html)

ソースコード: [Lib/_dummy_thread.py](https://github.com/python/cpython/tree/3.6/Lib/_dummy_thread.py)

> このモジュールは _thread モジュールのインターフェースをそっくりまねるものです。 _thread モジュールがサポートされていないプラットフォームで import することを意図して作られたものです。

> おすすめの使い道は:

```python
try:
    import _thread
except ImportError:
    import _dummy_thread as _thread
```

> 生成するスレッドが、他のブロックしたスレッドを待ち、デッドロック発生の可能性がある場合には、このモジュールを使わないようにしてください。ブロッキング I/O を使っている場合によく起きます。

