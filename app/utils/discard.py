import random
import time
from typing import List

from pydantic import BaseModel
from selenium import webdriver
from selenium.webdriver.common.by import By

# AUTH = 'brd-customer-hl_3250c65a-zone-scraping_browser:l6d2m4og6pqe'
# SBR_WEBDRIVER = f'https://{AUTH}@zproxy.lum-superproxy.io:9515'


class Review(BaseModel):
    rating: str
    title: str
    content: str
    
class ReviewList(BaseModel):
    review_list: List[Review]

def get_reviewsX(url:str):
    review_list = []

    print('Connecting to Scraping Browser...')
    # sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
    # with Remote(sbr_connection, options=ChromeOptions()) as driver:
    driver= webdriver.Chrome()
    print('Connected! Navigating...')
    driver.implicitly_wait(1)
    driver.get(f'https://www.coupang.com{url}')
    print('Navigated! Scraping page content...')
    time.sleep(random.uniform(0.5,1))
    
    driver.find_element(By.XPATH,'//*[@id="btfTab"]/ul[1]/li[2]').click()
    
    data_page_num =1
    while True:
        
        
        reviews = driver.find_elements(By.CSS_SELECTOR,".sdp-review__article__list.js_reviewArticleReviewList")
        
        review_btns = driver.find_elements(By.CSS_SELECTOR,f".sdp-review__article__page__num.js_reviewArticlePageBtn")
        
        print(len(review_btns))
        if not reviews:
            print("없음")
            
        for i, review in enumerate(reviews, 1):
            try:
                review_rating = review.find_element(By.CSS_SELECTOR, ".sdp-review__article__list__info__product-info__star-orange.js_reviewArticleRatingValue").get_attribute("data-rating")
            except:
                review_rating = "값 없음"
            try:
                review_title = review.find_element(By.CSS_SELECTOR, ".sdp-review__article__list__headline").text
            except:
                review_title = "없음"
            try:
                review_content = review.find_element(By.CSS_SELECTOR, ".sdp-review__article__list__review__content.js_reviewArticleContent").text
            except:
                review_content = "없음"

            review_list.append(Review(rating=review_rating, title=review_title, content=review_content))
        data_page_num +=1
        
        if data_page_num > len(review_btns) or data_page_num > 3:
            break
        
        review_btn = driver.find_element(By.CSS_SELECTOR,f".sdp-review__article__page__num.js_reviewArticlePageBtn[data-page='{data_page_num}']")
        review_btn.click()
        
        time.sleep(random.uniform(0.6,1))
        
    driver.quit()
    return ReviewList(review_list=review_list).dict()





