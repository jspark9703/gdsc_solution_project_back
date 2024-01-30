import warnings
from typing import List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.chromium.remote_connection import \
    ChromiumRemoteConnection
from selenium.webdriver.common.by import By

from utils.models import FilterList, Prod, ProdList

warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)


host = "brd.superproxy.io:22225"
user_name = "brd-customer-hl_3250c65a-zone-unblocker"
password = "keckdpm31tj0"

proxy_url = f"https://{user_name}:{password}@{host}"

proxies = {"http":proxy_url,"https":proxy_url}
#TODO filterList 받아와서 셀레니얼로 조작

path="/driver/chromedriver"
driver = webdriver.Chrome(path)
#TODO 셀레니얼로 받아온 url 전달
def get_product_list(kwds:str, filter_list:FilterList):
    data_list = []
    
    for page_idx in range(1):
        url =  f"https://www.coupang.com/np/search?q={kwds}&page={page_idx}"
        response = requests.get(url, proxies=proxies, verify=False)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        items = soup.select("[class=search-product]")

        for item in items:
            name = item.select_one(".name").text
            price = item.select_one(".price-value").text
            if not price:
                continue
            coupon_price = item.select_one(".").text
            #TODO couponprice 추가
            link = item.a['href']

            rating = item.select_one(".rating-star")
            if not rating:
                continue
            rating_num = rating.select_one(".rating-total-count").text
            rating_num =''.join(filter(str.isdigit, rating_num))

            if int(rating_num) < 30:
                continue

            rating = rating.select_one(".rating").text
            
            data = Prod({
                "name": name,
                "price": price,
                "coupon_price":"",
                "rating": rating,
                "rating_num": rating_num,
                "link": link})
            data_list.append(data)
    

    return ProdList(prods=data_list)

