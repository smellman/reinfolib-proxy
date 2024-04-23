# 不動産情報ライブラリ　Proxy

## 概要

不動産情報ライブラリのProxyです。

## 使い方

### ライブラリのインストール

```bash
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### API Keyの設定

```bash
vim main.py
```

`API_KEY`にAPI Keyを設定してください。

### ライブラリの実行

```bash
uvicorn main:app --reload
```