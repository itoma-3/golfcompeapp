# Pythonのベースイメージを使用
FROM python:3.9

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# 環境変数を設定
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 依存関係のインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# プロジェクトのファイルをコピー
COPY . .