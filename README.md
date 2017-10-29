# Ghostwriter
[![Ghostwriter](https://raw.github.com/GabLeRoux/WebMole/master/ressources/WebMole_Youtube_Video.png)](https://www.youtube.com/watch?v=uViALDC-OAw&feature=youtu.be)

## 製品概要
### 試験対策 Tech

### 背景（製品開発のきっかけ、課題等）
大学での講義では，前に映されているスライドをカメラで撮る人がよく見られます．シャッター音がうるさいですし，授業の妨げになる場合があります．しかも，撮ったスライドの画像はそこまで見直すわけでもありません．試験直前に少し見直して「あれ？これどんな内容だっけ？」と混乱してしまいます．

そこで私たちは，設置するだけでスライドの情報を保存して，かつその内容を解析し試験対策用の問題を生成する製品を開発しようと思いました．

決してその製品に任せて授業中に寝ようなんて思っていません．

### 製品説明（具体的な製品の説明）
授業中にスライドの内容を記録して，その情報から試験対策用問題を生成する．

### 特長

#### 1. スライドの認識と，そこに書かれているキーワードの抽出

#### 2. テスト対策用問題生成

#### 3. 講義ごとにキャプチャしたスライドを管理できるwebアプリ

### 解決出来ること
何から手をつけていいか分からない試験の対策となる．

### 今後の展望
- 黒板の記述も記録して問題生成できるようにしたい
- スライド部分に人が入ったり，カメラの位置やピントがブレた時にも対応
- webアプリの機能充実

## 開発内容・開発技術
### 活用した技術
#### API・データ
* 固有表現抽出API（NTTレゾナント様）
* キーワード抽出API（NTTレゾナント様）
* Google Cloud Vision API

#### フレームワーク・ライブラリ・モジュール
* OpenCV 3.3.0
* Django 1.11.6
* Pillow 4.3.0
* rabbitmq 0.2.0
* celery 3.2.1

#### デバイス
* Raspberry Pi 3
* Mac Book Pro

### 独自開発技術（Hack Dayで開発したもの）
#### 2日間に開発した独自の機能・技術
* webカメラでスライドを監視し，次のスライドに移ったタイミングで画像を取得する．前後のフレームの差分を平均二乗誤差法によって算出し，一定の差分が生まれたときにスライドが変わったと判断する．誤検知を防ぐために，自動でスライドの位置を検出している．[code](https://github.com/jphacks/KB_1708/blob/master/webapp/ghostwriter/capture_lib/slidecapture.py)
* gooAPI，Google Cloud Vision APIを駆使し，スライドの画像から試験問題を生成する．[code](https://github.com/jphacks/KB_1708/blob/master/webapp/ghostwriter/capture_lib/generate_questions_from_images.py)
