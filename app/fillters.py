from models import Filter,FilterList

import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_best_filters():
    filter_list = []
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
    driver.get("https://www.kurly.com/collection-groups/market-best?page=1&collection=market-best&filters=")
    
    
    time.sleep(2)


    li = driver.find_elements(By.CSS_SELECTOR,".e1isxf3i1")
    
    for item in li:
        title = item.find_element(By.CSS_SELECTOR,".ee933652").text
        num = item.find_element(By.CSS_SELECTOR,".ee933651").text
        url = item.find_element(By.CSS_SELECTOR,".e1isxf3i0").get_attribute("href")
        filter_list.append(Filter(num=num,title=title,url=url))
        
        
    return FilterList(
        filter_list=filter_list
    )
    
    