# Dockerfile
FROM python:3.10-slim

WORKDIR /app

# 安裝必要系統套件
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
 && rm -rf /var/lib/apt/lists/*

# 複製專案到容器
COPY . /app

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 開放 Streamlit 端口
EXPOSE 8501

# 啟動 Streamlit 應用
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]
