
from apis.review_sum import get_review_sum, review_sum
from fastapi import FastAPI, HTTPException
from product_detail import get_product_detail
from product_list import get_product_list
from product_reviews import get_reviews
from utils.models import FilterList, UserUrl

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

# @app.get("/filters")
# async def filter_list(kwds:str):
#     return {
#   "filter_list": [
#     {
#       "title": "종류",
#       "classname": "search-attr_13100-filter",
#       "content": [
#         {
#           "value": "소",
#           "id": "attr26615"
#         },
#         {
#           "value": "돼지",
#           "id": "attr26616"
#         }
#       ]
#     },
#     {
#       "title": "총 중량",
#       "classname": "search-attr_7943-filter",
#       "content": [
#         {
#           "value": "300g 이하",
#           "id": "attr25132"
#         },
#         {
#           "value": "300~500g",
#           "id": "attr25133"
#         },
# 				{
#           "value": "500~700g",
#           "id": "attr25134"
#         },
# 				{
#           "value": "700~1kg",
#           "id": "attr25135"
#         },
# 				{
#           "value": "1kg~3kg",
#           "id": "attr25136"
#         },
# 				{
#           "value": "3kg 이상",
#           "id": "attr25137"
#         }
#       ]
#     }
#   ]
# }

#TODO FILTER 리스트 받고 카테고리 URL에 전달
@app.get("/prods")
async def search_prod(kwds:str):
    return {"data":get_product_list(kwds)}

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
        review_sum =  get_review_sum(user_url)
        return {"review_list":review_list,"review_sum":review_sum}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



