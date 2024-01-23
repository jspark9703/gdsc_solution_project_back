from bs4 import BeautifulSoup
from typing import Optional, Union, Dict, List
import time
import os
import re
import requests as req
import json
import pandas as pd


def get_headers(
        key: str,
        default_value: Optional[str] = None
) -> Union[dict[str, str], str]:
    """ Get Headers """
    JSON_FILE: str = 'json/headers.json'

    with open(JSON_FILE, 'r', encoding='UTF-8') as file:
        headers: Dict[str, Dict[str, str]] = json.loads(file.read())

    try:
        return headers[key]
    except:
        if default_value:
            return default_value
        raise EnvironmentError(f'Set the {key}')


class Coupang:
    @staticmethod
    def get_product_code(url: str) -> str:
        """ 입력받은 URL 주소의 PRODUCT CODE 추출하는 메소드 """
        prod_code: str = url.split('products/')[-1].split('?')[0]
        return prod_code

    def __init__(self) -> None:
        self.__headers: Dict[str, str] = get_headers(key='headers')
        # MAX_REVIEWS_PER_URL = 

    def main(self) -> List[List[Dict[str, Union[str, int]]]]:
        
        # To do: for문 안에 넣고 url 리스트를 사용하여 한 번에 입력 받아 다수의 리뷰 추출
        # URL 주소
        URL: str = self.input_review_url()

        # URL의 Product Code 추출
        prod_code: str = self.get_product_code(url=URL)

        # URL 주소 재가공
        URLS: List[str] = [
            f'https://www.coupang.com/vp/product/reviews?productId={prod_code}&page={page}&size=5&sortBy=ORDER_SCORE_ASC&ratings=&q=&viRoleCode=3&ratingSummary=true'
            for page in range(1, self.input_page_count() + 1)]

        # __headers에 referer 키 추가
        self.__headers['referer'] = URL

        with req.Session() as session:
            return [self.fetch(url=url, session=session) for url in URLS]

    def fetch(self, url: str, session) -> List[Dict[str, Union[str, int]]]:
        save_data: List[Dict[str, Union[str, int]]] = list()

        with session.get(url=url, headers=self.__headers) as response:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            # Article Boxes
            article_length = len(soup.select(
                'article.sdp-review__article__list'))

            for idx in range(article_length):
                dict_data: Dict[str, Union[str, int]] = dict()
                articles = soup.select('article.sdp-review__article__list')

                # 구매자 이름
                user_name = articles[idx].select_one(
                    'span.sdp-review__article__list__info__user__name')
                if user_name == None or user_name.text == '':
                    user_name = '-'
                else:
                    user_name = user_name.text.strip()

                # To do: TOP 10 구매자 여부 데이터 추출
                    
                # 평점
                rating = articles[idx].select_one(
                    'div.sdp-review__article__list__info__product-info__star-orange')
                if rating == None:
                    rating = 0
                else:
                    rating = int(rating.attrs['data-rating'])

                # 구매자 상품명
                prod_name = articles[idx].select_one(
                    'div.sdp-review__article__list__info__product-info__name')
                if prod_name == None or prod_name.text == '':
                    prod_name = '-'
                else:
                    prod_name = prod_name.text.strip()

                # 헤드라인(타이틀)
                headline = articles[idx].select_one(
                    'div.sdp-review__article__list__headline')
                if headline == None or headline.text == '':
                    headline = '등록된 헤드라인이 없습니다'
                else:
                    headline = headline.text.strip()

                # 리뷰 내용
                review_content = articles[idx].select_one(
                    'div.sdp-review__article__list__review > div')
                if review_content is None:
                    review_content = '등록된 리뷰내용이 없습니다'
                else:
                    # To do : 리뷰 내용에 포함된 \n, \t 제거 -> 특수문자, 문제를 일으킬 수 있는 문자 제거
                    review_content = re.sub(
                        '[\n\t]', '', review_content.text.strip())

                # 맛 만족도 등의 지표 -> 품목마다 다름
                answer = articles[idx].select_one(
                    'span.sdp-review__article__list__survey__row__answer')
                if answer == None or answer.text == '':
                    answer = '맛 평가 없음'
                else:
                    answer = answer.text.strip()

                # To do: 도움이 됨 데이터 추출

                # 원본 URL 
                dict_data['prod_name'] = prod_name
                dict_data['user_name'] = user_name
                dict_data['rating'] = rating
                dict_data['headline'] = headline
                dict_data['review_content'] = review_content
                dict_data['answer'] = answer

                save_data.append(dict_data)

                # print(dict_data, '\n')
            
            # Add delay
            time.sleep(1)

            return save_data

    # @staticmethod
    # def clear_console() -> None:
    #     command: str = 'clear'
    #     if os.name in ('nt', 'dos'):
    #         command = 'cls'
    #     os.system(command)

    def input_review_url(self) -> str:
        while True:
            # Window
            # os.system('cls')
            # Mac
            os.system('clear')
            # Review URL
            review_url: str = input(
                '원하시는 상품의 URL 주소를 입력해주세요\n\nEx)\nhttps://www.coupang.com/vp/products/7204995821?itemId=18219837571&vendorItemId=85367581774&q=%EB%8B%AD%EA%B0%95%EC%A0%95&itemsCount=27&searchId=ebdff800c5af4600b18c5bc440f3d50e&rank=3&isAddedCart=\n\n:')
            if not review_url:
                # Window
                os.system('cls')
                # Mac
                # os.system('clear')
                print('URL 주소가 입력되지 않았습니다')
                continue
            return review_url

    def input_page_count(self) -> int:
        # Window
        # os.system('cls')
        # Mac
        os.system('clear')

        while True:
            page_count: str = input('페이지 수를 입력하세요\n\n:')
            if not page_count:
                print('페이지 수가 입력되지 않았습니다\n')
                continue

            return int(page_count)


class SaveFile:
    @staticmethod
    def save_file() -> None:
        # scrap result
        results: List[List[Dict[str, Union[str, int]]]] = Coupang().main()

        # pandas를 사용하지 않고 csv 파일을 작성하는 방법은 없을까?
        # DataFrame
        df = pd.DataFrame(columns=[
                          'prod_name', 'user_name', 'rating', 'headline', 'review_content', 'answer'])

        # results를 데이터프레임에 넣어주는 코드
        for result in results:
            for data in result:
                df.loc[len(df)] = data

        savePath: str = os.path.abspath('coupang-review')

        if not os.path.exists(savePath):
            os.mkdir(savePath)

        df.to_csv('./coupang-review/data.csv',
                  index=False, encoding='utf-8-sig')

        print('저장완료')

if __name__ == '__main__':
    SaveFile.save_file()