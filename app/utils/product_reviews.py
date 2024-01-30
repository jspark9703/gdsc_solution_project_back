
from typing import List

from utils.models import Review
from utils.scrap import Coupang


def get_reviews(url):

    coupang_reviews = list(Coupang().main(url)[0])
    
    return coupang_reviews
