
import time

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from models import Item, ProductDetail


def get_product_detail(url:str):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("authority=" + "www.coupang.com")
    options.add_argument("method=" + "GET")
    options.add_argument("accept=" + "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9")
    options.add_argument("accept-encoding=" + "gzip, deflate, br")
    options.add_argument("user-agent=" + "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.104 Whale/3.13.131.36 Safari/537.36")
    options.add_argument("sec-ch-ua-platform=" + "macOS")
    options.add_argument("cookie=" + "PCID=31489593180081104183684; _fbp=fb.1.1644931520418.1544640325; gd1=Y; X-CP-PT-locale=ko_KR; MARKETID=31489593180081104183684; sid=03ae1c0ed61946c19e760cf1a3d9317d808aca8b; x-coupang-origin-region=KOREA; x-coupang-target-market=KR; x-coupang-accept-language=ko_KR;")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)   

    

    driver.get(url)

    time.sleep(2)

    section = driver.find_element(By.CSS_SELECTOR,".e17iylht3")
    details= section.find_elements(By.CSS_SELECTOR,".epzddad2")
    
    title = section.find_element(By.CSS_SELECTOR,".ezpe9l11").text
    sub_title = section.find_element(By.CSS_SELECTOR,".ezpe9l10").text
    price = section.find_element(By.CSS_SELECTOR,".e1q8tigr4").text.replace("\n","")
    dimm_price = section.find_element(By.CSS_SELECTOR,".e1q8tigr0").text.replace("\n","")
    detail_list = []

    for detail in details:
        
        try:
            item_cate = detail.find_element(By.CSS_SELECTOR,".epzddad1").text

        except NoSuchElementException:
            item_cate = None
        
        try:
            item_name = detail.find_element(By.CSS_SELECTOR,".e6qx2kx1").text
        except NoSuchElementException:
            item_name = None
        try:
            item_content = detail.find_element(By.CSS_SELECTOR,".e6qx2kx0").text
        except NoSuchElementException:
            item_content = None


        item = Item(
            item_cate=item_cate,
            item_content=item_content,
            item_name=item_name
        )
        detail_list.append(item)


    
    des = driver.find_element(By.CSS_SELECTOR,".context.last")
    des = des.find_element(By.CSS_SELECTOR,"p.words").text
    tip_box = driver.find_element(By.CSS_SELECTOR,".tip_box")

    tip_contents = tip_box.find_elements(By.CSS_SELECTOR,".words")

    tips = []
    for content in tip_contents:
        tips.append(content.text)

    img_link= driver.find_element(By.CSS_SELECTOR,".goods_intro")
    img_link = img_link.find_element(By.CSS_SELECTOR,"img").get_attribute("src")
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

