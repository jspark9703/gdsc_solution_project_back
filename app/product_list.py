import time
from typing import Optional

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from models import Prod, ProdList

# warnings.filterwarnings("ignore", category=requests.packages.urllib3.exceptions.InsecureRequestWarning)
# host = "brd.superproxy.io:22225"
# user_name = "brd-customer-hl_3250c65a-zone-unblocker"
# password = "keckdpm31tj0"

# proxy_url = f"https://{user_name}:{password}@{host}"

# proxies = {"http":proxy_url,"https":proxy_url}





    
def get_product_list(kwds:Optional[str] = None, is_best_url:Optional[str] = None):
    
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
    if is_best_url :
        url= is_best_url
    else :
        url = f"https://www.kurly.com/search?sword={kwds}"
    driver.get(url)
    time.sleep(1)

    items= driver.find_elements(By.CSS_SELECTOR,".e1c07x487")
    detail_list = []
    for item in items:
        
        prod_link = item.get_attribute(name="href")
        name = item.find_element(By.CSS_SELECTOR,".e1c07x485").text
        price = item.find_element(By.CSS_SELECTOR,".sales-price").text
        
        try:
            dimmed_price =  item.find_element(By.CSS_SELECTOR,".dimmed-price").text
            
        except NoSuchElementException:
            dimmed_price = ""
        try:
            review_num= item.find_element(By.CSS_SELECTOR,".review-number").text

        except NoSuchElementException:
            review_num = ""
        
        
        
        data = Prod(
            link=prod_link,
            name=name,
            price=price,
            dimm=dimmed_price,
            rating_num=review_num
            )
        
        detail_list.append(data)
        
    driver.quit()
    return ProdList(prods=detail_list)
# div= driver.find_element(By.CSS_SELECTOR,".search-attr_7943-filter")

# item = div.find_element(By.CSS_SELECTOR,'#attr25617')
# item = item.find_element(By.XPATH,"..")
# item.click()

# time.sleep(5)
# prod = driver.find_element(By.CSS_SELECTOR,".search-product-link")
# link =prod.get_attribute(name="href")
# print(link)


    
    # response = requests.get(f"https://www.coupang.com{url}", proxies=proxies, verify=False)
    # print(f"https://www.coupang.com{url}")
    # print(response.status_code)
    # html = response.text
    # soup = BeautifulSoup(html,"html.parser")

    # prod_img_url = soup.select_one(".prod-image__detail")['src']
    # brand = soup.select_one(".prod-brand-name")
    # brand = "" if not brand else brand.text.strip()

    # title = soup.select_one(".prod-buy-header__title")
    # title = "" if not title else title.text.strip()


    # seller = soup.select_one(".prod-sale-vendor-name")
    # seller = "" if not seller else seller.text.strip()

    # prod_sale_price = soup.select_one(".prod-sale-price")
    # prod_coupon_price = soup.select_one(".prod-coupon-price")

    # if prod_sale_price:
    #     prod_sale_price = prod_sale_price.select_one(".total-price").text.strip()
    # else:
    #     prod_sale_price = "없음"
    # if prod_coupon_price:
    #     prod_coupon_price = prod_coupon_price.select_one(".total-price").text.strip()
    # else:
    #     prod_coupon_price= "없음"

    # # prod_option_item = soup.select(".prod-option__item")

    # # if prod_option_item:
    # #     option_list = []
        
    # #     for item in prod_option_item:
    # #         option_title = item.select_one(".title").string.strip()
    # #         option_value = item.select_one(".value").string.strip()
    # #         option_list.append(f"{option_title}: {option_value}")
    # #     prod_option_item = ", ".join(option_list)
    # # else:
    # #     prod_option_item = ""

    # prod_description = soup.select(".prod-description .prod-attr-item")  # 상세정보

    # if prod_description:
    #     description_list = []
    #     for description in prod_description:
    #         description_list.append(description.string.strip())
    #     prod_description = ", ".join(description_list)
    # else:
    #     prod_description = ""

    # product_detail = ProductDetail(
    #     prod_img_url= prod_img_url,
    #     brand=brand,
    #     title=title,
    #     seller=seller,
    #     prod_sale_price=prod_sale_price,
    #     prod_coupon_price=prod_coupon_price,
    #     # prod_option_item=prod_option_item,
    #     prod_description=prod_description
    # )

    


