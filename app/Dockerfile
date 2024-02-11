# Python 이미지를 기반으로 시작
FROM python:3.11

# Chrome 설치
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get update && apt-get install -y google-chrome-stable

# ChromeDriver 설치
RUN CHROME_VERSION=$(google-chrome --version | grep -oE "[0-9.]+" | head -1) && \
    DRIVER_VERSION=$(wget -qO- "https://chromedriver.storage.googleapis.com/114.0.5735.90") && \
    wget -N http://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip -P ~/ && \
    unzip ~/chromedriver_linux64.zip -d ~/ && \
    mv -f ~/chromedriver /usr/local/bin/chromedriver && \
    chown root:root /usr/local/bin/chromedriver && \
    chmod 0755 /usr/local/bin/chromedriver && \
    rm ~/chromedriver_linux64.zip

# 작업 디렉토리 설정
WORKDIR /app

# 애플리케이션 파일 복사
COPY . /app

# 필요한 Python 패키지 설치
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
