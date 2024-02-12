import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def test_driver_location():
    # Chrome 실행 파일의 경로
    chrome_bin = "../opt/chrome/chrome-linux64/chrome"
    
    # ChromeDriver 실행 파일의 경로
    chromedriver_bin = "../usr/local/bin/chromedriver-linux64/chromedriver"
    
    # Chrome 옵션 설정
    options = webdriver.ChromeOptions()
    
    # Docker 컨테이너 내의 Chrome 경로 지정
    options.binary_location = chrome_bin
    options.add_argument("--headless")
    
    # ChromeDriver 서비스 설정
    service = Service(executable_path=chromedriver_bin)
    
    if os.path.exists(chrome_bin):
        print(f"Chrome 경로가 올바릅니다: {chrome_bin}")
    else:
        print(f"Chrome 경로가 잘못되었습니다: {chrome_bin}")

# ChromeDriver 실행 파일의 경로 확인
    if os.path.exists(chromedriver_bin):
        print(f"ChromeDriver 경로가 올바릅니다: {chromedriver_bin}")
    else:
        print(f"ChromeDriver 경로가 잘못되었습니다: {chromedriver_bin}")
    
    # WebDriver 초기화
    driver = webdriver.Chrome(service=service, options=options)
    
    # WebDriver 사용 예시: Google 페이지 열기
    driver.get("https://www.naver.com")
    
    # 페이지 제목 출력
    test = driver.title
    
    # WebDriver 종료
    driver.quit()

    return test

test = test_driver_location()
print(test)