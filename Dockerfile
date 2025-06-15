# ベースイメージとしてPython 3.9を選択
FROM python:3.9-slim

# Tkinterを動作させるために必要なライブラリをインストール
RUN apt-get update && apt-get install -y tk

# 作業ディレクトリを作成
WORKDIR /app

# カレントディレクトリのファイルをコンテナの/appにコピー
COPY . /app

# コンテナからホストOSのディスプレイに接続するための設定
# Macの場合、'host.docker.internal'がホストマシンを指す特別なDNS名
ENV DISPLAY=host.docker.internal:0

# アプリケーションを実行
CMD ["python", "brain_sim.py"]
