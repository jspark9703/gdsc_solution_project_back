import warnings

import requests
from bs4 import BeautifulSoup
from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.chromium.remote_connection import \
    ChromiumRemoteConnection
from selenium.webdriver.common.by import By

warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)


host = "brd.superproxy.io:22225"
user_name = "brd-customer-hl_3250c65a-zone-unblocker"
password = "keckdpm31tj0"

proxy_url = f"https://{user_name}:{password}@{host}"

proxies = {"http":proxy_url,"https":proxy_url}



#TODO url review page 정보 포함하여 재설정
def get_product_list(kwds:str):
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
            link = item.a['href']

            rating = item.select_one(".rating-star")
            if not rating:
                continue
            rating_num = rating.select_one(".rating-total-count").text
            rating_num =''.join(filter(str.isdigit, rating_num))

            if int(rating_num) < 30:
                continue

            rating = rating.select_one(".rating").text
            
            data_list.append({
                "name": name,
                "price": price,
                "rating": rating,
                "rating_num": rating_num,
                "link": link
            })

    return {"data": data_list}
