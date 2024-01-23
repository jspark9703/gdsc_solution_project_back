from typing import List

from langchain.prompts.chat import (ChatPromptTemplate,
                                    HumanMessagePromptTemplate,
                                    SystemMessagePromptTemplate)
from langchain.schema import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from pydantic import BaseModel

from credential.credential import OPENAI_API_KEY

chat = ChatOpenAI(temperature=0.5, openai_api_key=OPENAI_API_KEY,)


class Review(BaseModel):
    rating: str
    title: str
    content: str
    
class ReviewList(BaseModel):
    review_list: List[Review]


def review_sum(reviews:ReviewList):
    combined_content = "-------".join([review.content for review in reviews.review_list])
    
    prompt = ChatPromptTemplate.from_messages([
    ("system","""
        Answer the question using ONLY the following context. If you don't know the answer 
        just say you don't know. Don't make anything up.
        
        Context:{context}
    """),
    ("human"),"{question}"
    ])
    
