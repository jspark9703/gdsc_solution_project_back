# Python 이미지를 기반으로 시작
FROM python:3.11

# 필요한 도구 설치
RUN apt-get update && apt-get install -y wget unzip

# Chrome 다운로드 및 설치
RUN wget https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/linux64/chrome-linux64.zip -P /root/ && \
    unzip /root/chrome-linux64.zip -d /opt/chrome && \
    ln -s /opt/chrome/chrome /usr/bin/google-chrome && \
    rm /root/chrome-linux64.zip

# ChromeDriver 다운로드 및 설치
RUN wget -N https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/121.0.6167.85/linux64/chromedriver-linux64.zip -P /root/ && \
    unzip /root/chromedriver-linux64.zip -d /usr/local/bin/ && \
    ls -l /usr/local/bin/&&\
    chmod 0755 /usr/local/bin/chromedriver-linux64/chromedriver && \
    rm /root/chromedriver-linux64.zip


# 작업 디렉토리 설정
WORKDIR /app

# 애플리케이션 파일 복사
COPY . /app

# 필요한 Python 패키지 설치
RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
