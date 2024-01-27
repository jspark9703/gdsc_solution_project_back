
from fastapi import FastAPI, HTTPException

from models import FilterList, ReviewList, UserUrl
from product_detail import get_product_detail
from product_list import get_product_list
from product_reviewlist import get_reviews
from review_sum import review_sum

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

#TODO FILTER 리스트 받고 카테고리 URL에 전달
@app.get("/prods/")
async def search_prod(kwds:str,filter_list:FilterList):
    return get_product_list(kwds, filter_list)

@app.get("/prod_detail")
async def prod_detail(user_produrl:UserUrl):
    try:
        result = get_product_detail(user_produrl.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#TODO 리뷰 전처리과정 추가
@app.get("/prod_review")
async def prod_review(user_url:UserUrl):
    try:
        result = get_reviews(user_url.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/review_sum")
async def review_summury(userinfo:str,review_list:ReviewList ):
    return {"data":review_sum(userinfo,review_list)}


