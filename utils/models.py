from typing import List

from pydantic import BaseModel


class User(BaseModel):
    user_name:str
    user_class:int
    user_info:str
    
class UserUrl(BaseModel):
    user:User
    url:str

class Prod(BaseModel):
    name : str
    price : str
    coupon_price :str
    rating: int
    rating_num :int
    link: str
    
class ProdList(BaseModel):
    prods: List[Prod]
    


class ProductDetail(BaseModel):
    prod_img_url:str
    brand: str
    title: str
    seller: str
    prod_sale_price: str
    prod_coupon_price: str
    # prod_option_item: str
    prod_description: str
    
class Review(BaseModel):
    user_name: str
    rating: str
    headline: str
    review_content: str
    

class ReviewList(BaseModel):
    review_list: List[Review]

class FilterContent(BaseModel):
    value:str
    id:str
    
class Filter(BaseModel):
    title: str
    classname: str
    content: List[FilterContent]
    

    
class FilterList(BaseModel):
    filter_list:List[Filter]


