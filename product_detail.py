import warnings

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from selenium.webdriver import ChromeOptions, Remote
from selenium.webdriver.common.by import By

warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)
host = "brd.superproxy.io:22225"
user_name = "brd-customer-hl_3250c65a-zone-unblocker"
password = "keckdpm31tj0"

proxy_url = f"https://{user_name}:{password}@{host}"

proxies = {"http":proxy_url,"https":proxy_url}





class ProductDetail(BaseModel):
    brand: str
    title: str
    seller: str
    prod_sale_price: str
    prod_coupon_price: str
    # prod_option_item: str
    prod_description: str
    
    
def get_product_detail(url: str):
    
    response = requests.get(f"https://www.coupang.com{url}", proxies=proxies, verify=False)
    print(f"https://www.coupang.com{url}")
    print(response.status_code)
    html = response.text
    soup = BeautifulSoup(html,"html.parser")

    brand = soup.select_one(".prod-brand-name")
    brand = "" if not brand else brand.text.strip()

    title = soup.select_one(".prod-buy-header__title")
    title = "" if not title else title.text.strip()


    seller = soup.select_one(".prod-sale-vendor-name")
    seller = "" if not seller else seller.text.strip()

    prod_sale_price = soup.select_one(".prod-sale-price")
    prod_coupon_price = soup.select_one(".prod-coupon-price")

    if prod_sale_price:
        prod_sale_price = prod_sale_price.select_one(".total-price").text.strip()
    else:
        prod_sale_price = "없음"
    if prod_coupon_price:
        prod_coupon_price = prod_coupon_price.select_one(".total-price").text.strip()
    else:
        prod_coupon_price= "없음"

    # prod_option_item = soup.select(".prod-option__item")

    # if prod_option_item:
    #     option_list = []
        
    #     for item in prod_option_item:
    #         option_title = item.select_one(".title").string.strip()
    #         option_value = item.select_one(".value").string.strip()
    #         option_list.append(f"{option_title}: {option_value}")
    #     prod_option_item = ", ".join(option_list)
    # else:
    #     prod_option_item = ""

    prod_description = soup.select(".prod-description .prod-attr-item")  # 상세정보

    if prod_description:
        description_list = []
        for description in prod_description:
            description_list.append(description.string.strip())
        prod_description = ", ".join(description_list)
    else:
        prod_description = ""

    product_detail = ProductDetail(
        brand=brand,
        title=title,
        seller=seller,
        prod_sale_price=prod_sale_price,
        prod_coupon_price=prod_coupon_price,
        # prod_option_item=prod_option_item,
        prod_description=prod_description
    )

    return product_detail.dict()

