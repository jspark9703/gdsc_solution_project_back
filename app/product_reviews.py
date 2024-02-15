
from typing import List

from models import Review, ReviewList

import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from models import Item, ProductDetail

from bs4 import BeautifulSoup

def make_review_data_structure(review_length: int):
    review_list = [
        dict(
            name=None,
            url=None,
        ) for _ in range(review_length)
    ]
    return review_list

def get_review(driver):
    
    class_name = '.css-ek0k8o'
    target = driver.find_elements(by=By.CSS_SELECTOR, value=class_name)
    page_html = target[0].get_attribute('outerHTML')

    soup = BeautifulSoup(page_html, 'html.parser')

    review_length = len(soup.select('.css-y49dcn'))

    data = make_review_data_structure(review_length)

    for i in range(review_length):
        
        review_list = soup.select('.css-169773r')
        name = review_list[i].select_one('.css-f3vz0n').text
        data[i]['name'] = name

        review = review_list[i].select_one('.css-y49dcn').text
        data[i]['review'] = review
        
    return data

def get_reviews(url:str):
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

    url = url
    driver.get(url)
    driver.implicitly_wait(10)

    # 리뷰 더보기 버튼이 없을 수 있으므로 예외 처리 필요
    try:
        button_class = '#review > section > div:nth-child(3) > div.css-jz9m4p.ebs5rpx3 > button.css-1orps7k.ebs5rpx0'
        button = driver.find_element(by=By.CSS_SELECTOR, value=button_class)
    except NoSuchElementException:
        button = None

    review_list = get_review(driver)

    max_reviews = 20  # 최대 리뷰 수
    iteration_num = 2
    for _ in range(iteration_num):
        # 현재 리뷰 수가 최대 리뷰 수에 도달하면 루프 종료
        if len(review_list) >= max_reviews:
            break
        if button:
            button.click()
            time.sleep(2)
            temp = get_review(driver)
            for review in temp:
                # 리뷰 추가 중 최대 리뷰 수를 초과하지 않도록 확인
                if len(review_list) < max_reviews:
                    review_list.append(review)
                else:
                    break

    driver.quit()  # 드라이버 사용 종료
    return ReviewList(review_list=review_list[:max_reviews])  # 최대 15개 리뷰만 반환