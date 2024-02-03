from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import os
import time

def make_category_data_structure(category_length: int):
    category_list=[
        dict(
            title=None,
            link=None,
        ) for _ in range(category_length)
    ]
    return category_list

def make_review_data_structure(review_length: int):
    review_list = [
        dict(
            name=None,
            url=None,
        ) for _ in range(review_length)
    ]
    return review_list

def get_category_list(driver: webdriver.Chrome):
    """
    사용하기 전에 웹 브라우저, ChromeDriver 설치 필요
    """
    # 페이지 접근
    url = 'https://www.kurly.com/collection-groups/market-best?page=1&collection=market-best'
    driver.get(url)
    driver.implicitly_wait(10)

    # 카테고리 리스트
    class_name = '.css-1kscq9s'
    target = driver.find_elements(by=By.CSS_SELECTOR, value=class_name)
    page_html = target[0].get_attribute('outerHTML')

    soup = BeautifulSoup(page_html, 'html.parser')

    category_length = len(soup.select('nav > li'))

    data = make_category_data_structure(category_length)

    for i in range(category_length):
        category_list = soup.select('.css-x67gaa')
        category = category_list[i].select_one('.css-1buhy1h').text
        data[i]['title'] = category

        link = category_list[i].select_one('a').attrs['href']
        data[i]['link'] = link

    return {'review_list': data}

def input_review_url():
    while True:
        # Window
        # os.system('cls')
        # Mac
        os.system('clear')
        # Review URL
        review_url: str = input(
            '원하시는 상품의 URL 주소를 입력해주세요\n\nEx)\nhttps://www.kurly.com/goods/5031441:')
        if not review_url:
            # Window
            os.system('cls')
            # Mac
            # os.system('clear')
            print('URL 주소가 입력되지 않았습니다')
            continue
        return review_url
    
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

def get_all_review(driver=None):

    url = input_review_url()
    driver.get(url)
    driver.implicitly_wait(10)

    button_class = '#review > section > div:nth-child(3) > div.css-jz9m4p.ebs5rpx3 > button.css-1orps7k.ebs5rpx0'
    button = driver.find_element(by=By.CSS_SELECTOR, value=button_class)

    review_list = get_review(driver)

    iteration_num = 3
    for _ in range(iteration_num):
        button.click()
        time.sleep(2)
        temp = get_review(driver)
        for review in temp:
            review_list.append(review)

    return {'review_list': review_list}

if __name__ == '__main__':

    webdriver_options = webdriver.ChromeOptions()

    # 원하는 창 크기
    webdriver_options.add_argument('--window-size=1000, 500')

    # 내부 창을 띄울 수 없으므로 설정
    # webdriver_options.add_argument('--headless')

    # 리소스 제한, 안정성 높이는 부분
    # webdriver_options.add_argument('--no-sandbox')
    # webdriver_options.add_argument('--disable-dev-shm-usage')

    # ChromeDriver 경로 설정
    # chrome_driver_path = '/usr/bin/chromedriver'
    # linux_driver = webdriver.Chrome(executable_path=chrome_driver_path, options=options)

    driver = webdriver.Chrome(service=Service(
        ChromeDriverManager().install()), options=webdriver_options)
    
    data = get_category_list(driver)
    print(data)

    review = get_all_review(driver)
    print(review)
