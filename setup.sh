#!/bin/bash

# 必要なパッケージをインストール
pip install -r requirements.txt

# ディレクトリ構造を作成
mkdir -p logs backups

# アプリケーションを起動
python main.py
