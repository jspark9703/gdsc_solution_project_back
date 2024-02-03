from typing import List

from pydantic import BaseModel


class User(BaseModel):
    user_name:str
    user_class:str
    user_info:str
    
class UserUrl(BaseModel):
    user:User
    url:str

class Prod(BaseModel):
    link: str
    name : str
    price : str
    dimm :str
    rating_num :str
    
    
class ProdList(BaseModel):
    prods: List[Prod]
    
class Item(BaseModel):
    item_cate:str
    item_name:str
    item_content:str

class ProductDetail(BaseModel):
    prod_img_url:str
    title: str
    sub_title: str
    price: str
    dimm_price:str
    description:str    # prod_option_item: str
    details:List[Item]
    
    
class Review(BaseModel):
    name: str
    url:str | None = None
    review: str
    

class ReviewList(BaseModel):
    review_list: List[Review]

    
class Filter(BaseModel):
    title: str
    num:str
    url:str
    

    
class FilterList(BaseModel):
    filter_list:List[Filter]


