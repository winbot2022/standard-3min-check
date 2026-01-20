# 1. Python 3.11を使用
FROM python:3.11-slim

# 2. OSの最小限のツールをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 3. 作業ディレクトリ
WORKDIR /app

# 4. ライブラリのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. プログラムのコピー
COPY . .

# 6. AWS App Runnerの標準ポート 8080 を開放
EXPOSE 8080

# 7. 起動コマンド（ここが最重要！）
# 環境変数ではなく、コマンド引数として「最強の設定」を叩き込みます
CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=8080", \
     "--server.address=0.0.0.0", \
     "--server.enableCORS=false", \
     "--server.enableXsrfProtection=false", \
     "--server.headless=true", \
     "--browser.serverPort=443", \
     "--server.enableWebsocketCompression=false", \
     "--global.developmentMode=false"]
