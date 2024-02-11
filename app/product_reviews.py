
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
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    # 추가적인 options 설정은 생략합니다.
    options.add_argument("authority=" + "www.kurly.com")
    options.add_argument("method=" + "GET")
    options.add_argument("accept=" + "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
    options.add_argument("accept-encoding=" + "gzip, deflate, br")
    options.add_argument("user-agent=" + "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36")
    options.add_argument("sec-ch-ua-platform=" + "macOS")
    options.add_argument("cookie=" + "PCID=31489593180081104183684; _fbp=fb.1.1644931520418.1544640325; gd1=Y; X-CP-PT-locale=ko_KR; MARKETID=31489593180081104183684; sid=03ae1c0ed61946c19e760cf1a3d9317d808aca8b; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; x-coupang-accept-language=ko_KR;")
    driver = webdriver.Chrome(service=Service("/usr/local/bin/chromedriver"), options=options)

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

    max_reviews = 15  # 최대 리뷰 수
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