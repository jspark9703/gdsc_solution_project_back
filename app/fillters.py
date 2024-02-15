from models import Filter,FilterList

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_best_filters():
    filter_list = []
    # Chrome 실행 파일의 경로
    chrome_bin = "../opt/chrome/chrome-linux64/chrome"
    
    # ChromeDriver 실행 파일의 경로
    chromedriver_bin = "../usr/local/bin/chromedriver-linux64/chromedriver"
    
    # Chrome 옵션 설정
    options = webdriver.ChromeOptions()
    
    # Docker 컨테이너 내의 Chrome 경로 지정
    options.binary_location = chrome_bin
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")  # Sandbox 모드 비활성화
    options.add_argument("--disable-dev-shm-usage")  # /dev/shm 파티션 사용 비활성화
    options.add_argument("--remote-debugging-port=9222") 
    
    # ChromeDriver 서비스 설정
    service = Service(executable_path=chromedriver_bin)
    
  
    # WebDriver 초기화
    driver = webdriver.Chrome(service=service, options=options)
    try:
        driver.get("https://www.kurly.com/collection-groups/market-best?page=1&collection=market-best&filters=")
        time.sleep(1)  # 페이지 로딩 대기

        # 필터 정보 스크래핑
        li = driver.find_elements(By.CSS_SELECTOR, ".e1isxf3i1")
        for index, item in enumerate(li):
            if index >= 10:  # 최대 10개의 필터만 처리
                break
            title = item.find_element(By.CSS_SELECTOR, ".ee933652").text
            num = item.find_element(By.CSS_SELECTOR, ".ee933651").text
            url = item.find_element(By.CSS_SELECTOR, ".e1isxf3i0").get_attribute("href")
            filter_list.append(Filter(num=num, title=title, url=url))

        return FilterList(filter_list=filter_list)
    finally:
        driver.quit()  # WebDriver 종료
    
    