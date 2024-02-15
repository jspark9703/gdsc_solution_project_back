
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from models import Item, ProductDetail


def get_product_detail(url:str):
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

    

    driver.get(url)

    time.sleep(2)

    
    section = driver.find_element(By.CSS_SELECTOR,".e17iylht3")
    title = section.find_element(By.CSS_SELECTOR,".ezpe9l11").text
    sub_title = section.find_element(By.CSS_SELECTOR,".ezpe9l10").text
    price = section.find_element(By.CSS_SELECTOR,".e1q8tigr4").text.replace("\n","")
    
    try:
        dimm_price = section.find_element(By.CSS_SELECTOR,".e1q8tigr0").text.replace("\n","")

    except NoSuchElementException:
        dimm_price =""
    
    
    detail_list = []
    details= section.find_elements(By.CSS_SELECTOR,".epzddad2")

    for detail in details:
        
        try:
            item_cate = detail.find_element(By.CSS_SELECTOR,".epzddad1").text

        except NoSuchElementException:
            item_cate = ""
        
        try:
            item_name = detail.find_element(By.CSS_SELECTOR,".e6qx2kx1").text
        except NoSuchElementException:
            item_name = ""
        try:
            item_content = detail.find_element(By.CSS_SELECTOR,".e6qx2kx0").text
        except NoSuchElementException:
            item_content = ""


        item = Item(
            item_cate=item_cate,
            item_content=item_content,
            item_name=item_name
        )
        detail_list.append(item)


    try:
        des = driver.find_element(By.CSS_SELECTOR,".context.last")
        des = des.find_element(By.CSS_SELECTOR,"p.words").text
    except NoSuchElementException:
        des = ""
    
    tips = []
    try:
        tip_box = driver.find_element(By.CSS_SELECTOR,".tip_box")
        tip_contents = tip_box.find_elements(By.CSS_SELECTOR,".words")
        
        for content in tip_contents:
            tips.append(content.text)
    except NoSuchElementException:
        tips = []
    
    

    try:
        img_link= driver.find_element(By.CSS_SELECTOR,".goods_intro")
        img_link = img_link.find_element(By.CSS_SELECTOR,"img").get_attribute("src")
        
        
    except NoSuchElementException:
        img_link = ""

    
    
    
    data = ProductDetail(
        details= detail_list,
        description=des,
        title=title,
        sub_title=sub_title,
        price=price,
        dimm_price=dimm_price,
        prod_img_url=img_link
    )
    return data

