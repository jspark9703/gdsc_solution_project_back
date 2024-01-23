from typing import List

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from product_detail import get_product_detail
from product_list import get_product_list
from product_reviewlist import get_reviews

app = FastAPI()


class UserUrl(BaseModel):
    user:str
    url:str
    
class Review(BaseModel):
    rating: str
    title: str
    content: str

class ReviewList(BaseModel):
    review_list: List[Review]

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/prods/")
async def search_prod(kwds:str):
    return get_product_list(kwds)

@app.get("/prod_detail")
async def prod_detail(q:UserUrl):
    try:
        result = get_product_detail(q.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#TODO 리뷰 전처리과정 추가
@app.get("/prod_review")
async def prod_review(q:UserUrl):
    try:
        result = get_reviews(q.url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/review_sum")
async def review_sum(q:ReviewList):
    return q


