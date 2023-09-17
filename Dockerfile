# 使用官方 Python 映像作為基底映像
FROM python:3.11.3

# 將當前目錄下所有檔案複製到容器的 /app 目錄
COPY . /app

# 指定工作目錄為 /app
WORKDIR /app

# 安裝所需的套件
RUN pip3 install pyautogui
RUN pip3 install tk

# 定義程式的入口點
CMD ["python", "__main__.py"]
