
from typing import Optional
from fastapi import FastAPI, HTTPException,Response
from models import Review, ReviewList, UserUrl
from fillters import get_best_filters
from product_list import get_product_list
from product_detail import get_product_detail
from product_reviews import get_reviews
from review_sum import get_review_sum
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/search_prod")
async def search_prod(kwds:Optional[str] = None, is_best_url :Optional[str] = None):
    
    print(kwds)
    print(is_best_url)
    try:
        result = get_product_list(kwds,is_best_url)
        return {"data" :result}
    except  Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/prod_detail")
async def prod_detail(produrl:str):
    try:
        result = get_product_detail(produrl)
        return {"data":result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


#TODO 리뷰 전처리과정 추가
@app.get("/prod_reviews")
async def prod_reviews(url:str):
    try:
        review_list = get_reviews(url)
        return {"data":review_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



@app.post("/review_sum")
async def prod_review_sum(user_info:str ,review_list: ReviewList):
    try:
        review_sum = get_review_sum(user_info, review_list)
        return {"data":review_sum}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

   