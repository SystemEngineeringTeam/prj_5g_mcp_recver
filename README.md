# mocopi のデータを直接&インターネット経由で送信する

## セットアップ
### venv を設定
```shell
python3 -m venv .venv
```

### 依存関係のインストール
```shell
pip3 install -r requirements.txt
```

### 環境変数の設定
```shell
cp .env.example .env
```


## 実行方法
```shell
dotenvx run -- python3 main.py
```
