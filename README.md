# JecNavi API

このプロジェクトは、JecNavi公式サイトのニュースと重要なお知らせを取得するためのAPIを提供します。Flaskを使用して構築されており、Pythonで実装されています。

## 概要

このAPIは、学校の公式サイトからニュースや重要なお知らせをスクレイピングし、JSON形式で提供します。これにより、他のアプリケーションやサービスで簡単に情報を利用することができます。
## エンドポイント

### 重要なお知らせ (`/api/important`)

重要なお知らせを取得します。

- **メソッド**: GET
- **レスポンス**: JSON形式の重要なお知らせのリスト

レスポンスの例:
```json
[
    {
        "title": "Example Title",
        "link": "https://www.jec.ac.jp/urgent-news/12345",
        "date": "2024-07-01"
    },
    ...
]
```

### 学科ニュース (`/api/news`)

学科ニュースなどを取得します。

- **メソッド**: GET
- **クエリパラメータ**
 - `page`(オプション, デフォルト値: 1) - ニュースページの番号
- **レスポンス**: JSON形式のニュースのリスト

レスポンスの例:
```json
[
    {
        "title": "Example News Title",
        "link": "https://www.jec.ac.jp/collegenews/cm/12345/",
        "date": "2024-07-01",
        "image": "https://www.jec.ac.jp/images/example.jpg"
    },
    ...
]
```
## インストールと実行

### 1.このリポジトリをクローン
```sh
git clone https://github.com/dlxsmd/JecAPI.git
```
### 2.必要なパッケージをインストール
```sh
pip install -r requirements.txt
```
### 3.アプリケーションを実行
```sh
python app.py
```

## キャッシュ
このAPIでは、データ取得の効率を高めるためにキャッシュを使用しています。重要なお知らせは300秒（5分）間キャッシュされます。

## 工夫した点
- **スクレイピングの安定性**: BeautifulSoupを使用してHTMLをパースし、必要な情報を効率よく抽出
- **キャッシュ機能**: キャッシュを導入することで、頻繁なリクエストによるサーバー負荷を軽減

## 貢献
バグ報告や新機能の提案は、Issuesセクションで行ってください。プルリクエストもお待ちしています。




