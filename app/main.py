

from fastapi import FastAPI, HTTPException
from models import UserUrl
from fillters import get_best_filters
from product_list import get_product_list
from product_detail import get_product_detail
from product_reviews import get_reviews
from review_sum import get_review_sum


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/best_filter")
async def get_filters():
    try:
        result = get_best_filters()
        return {"data": result}
    except  Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/prods")
async def search_prod(kwds:str,is_best_url :str|None):
    try:
        
        if is_best_url =="" or not "https" in is_best_url:
            is_best_url = None
        result = get_product_list(kwds,is_best_url=is_best_url)
        return {"data" :result}
    except  Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/prod_detail")
async def prod_detail(user_produrl:UserUrl):
    try:
        result = get_product_detail(user_produrl.url)
        return {"data":result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#TODO 리뷰 전처리과정 추가
@app.get("/prod_review")
async def prod_review(user_url:UserUrl):
    try:
        review_list = get_reviews(user_url.url)
        review_sum =  get_review_sum(user_url,review_list=review_list)
        return {"review_list":review_list,"review_sum":review_sum}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



