# API活用サンプル
適当にAPI Keyをまとめたファイルを作って読み込んでください．

作成例 config.ini
```
[gooAPI]
id=xxxxxxxxxxxxxxxxxx

[googleAPI]
key=123456789bbbbbbbbb
```


## GooAPI
### 環境構築
[ここ](https://labs.goo.ne.jp/apiusage/)を参考に
GitHubを用いてのアカウント登録してIDを発行する．

有志がpythonのライブラリを作っているのでインストール
```
pip install goolabs
```
[goolabsのリファレンス](https://pypi.python.org/pypi/goolabs)

### 利用について
gooAPIを使用したwebサイトを公開する場合，クレジット表示が必要

クレジット表示例（[サイト](https://labs.goo.ne.jp/apiusage/)より）
```
<a href="http://www.goo.ne.jp/">
<img src="//u.xgoo.jp/img/sgoo.png" alt="supported by goo"
title="supported by goo">
</a>
```
その他にも商用利用する場合は連絡が必要．

## Google Cloud Vision API
[公式](https://cloud.google.com/vision/)
### 環境構築
[ここ](https://apps-gcp-tokyo.appspot.com/gcp-startup/)を参考にAPI Keyを発行する．

### 使用方法
一応ライブラリとサンプルプログラム作ったので見てなんとなく使い方察して．

ライブラリは[ここ](https://gist.github.com/dannguyen/a0b69c84ebc00c54c94d#file-cloudvisreq-py-L62)
を~~パクリ~~参考にして作りました．