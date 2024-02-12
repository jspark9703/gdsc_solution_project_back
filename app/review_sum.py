from typing import List
from credential.credential import OPENAI_API_KEY
from langchain.chat_models import ChatOpenAI
from langchain.prompts.chat import (ChatPromptTemplate
                                    )
from langchain.schema import  HumanMessage, SystemMessage
from models import  ReviewList, UserUrl

#CONTEXT 지정하여 제공
context = "맛, 조리방법, 양과 실용성, 제품의 신선도"


def get_review_sum(user_info:str , review_list:ReviewList):
    
    
    user_info=user_info
   
    review_list_soup = '||'.join(review.review for review in review_list.review_list)

    
    #TODO USERINFO JOIN, CONTEXT 결정, REVIEWLIST 크기 제한
    llm = ChatOpenAI(temperature=0.9, openai_api_key=OPENAI_API_KEY)


    # userinfo = "매운 걸 안좋아함, 시각 장애인"
    # review_list ="저랑 와이프가 팔당 오징어볶음 무척 좋아합니다.\n쿠팡에 이런 상품이 있는걸 발견해서 일단 바로 주문했습니다.\n금요일 주문해서 수요일 도착한다는거 화요일 퇴근하고오니 도착해있었습니다. 역시 배송 착합니다.\n\n● 맛평가\n첫번째. 우선 가장 중요한 맵기 정도는 원조 대비 비슷하거나 다소 약합니다. 그러나 집에서 먹기 나쁘지 않은 수준이라 판단 됨.\n저 같은 경우 매운음식에 취약해서(맵찔이) 땀 엄청 흘리며 먹음.\n\n두번째. 다른 분들 리뷰를 보니 니맛도 내맛도 아니다라는 평이 있는데 감칠맛?이 부족해서 매운맛만 느껴져 2% 부족함.\n다행히도 저희는 원조 팔당오징어 경험이 있어 농심 멸치칼국수 라면을 같이 먹었는데\n라면국물을 몇 숟갈 소스에 첨가하였더니 감칠맛이 살아서 제법 맛있게 즐길수 있었습니다.\n\n세번째. 조리법이 간단해 중불에 5분간 볶아서 먹으라고 되어있는데 개인차가 있겠지만 시간이 좀 더 걸리더라도 몸통, 다리 가능한 제대로 익혀서 드시는게 더 맛있게 느껴지는것 같네요. 통 오징어라서 몸통만 신경썼더니 다리는 덜 익어서 좀 별로였어요.\n\n최종적으로는 너무 맛있게 잘 먹었습니다. 왠만하면 이런 리뷰 안쓰는데 조금만 개선하면 좋은 상품이 될 수 있을것 같아서 리뷰를 남깁니다. 조금 만 더 신경써주시면 많은 분들이 요즘 같은 시대에 집에서 외식하는 느낌으로 즐길 수 있겠어요!! 읽어주셔서 감사합니다.||너무 맛있어요!\n먹어보고 주위에 영업성공만 세 곳\n그 중 두곳이 재주문!!!\n맵긴한데 콩나물 팽이버섯 양파 파 떡국떡까지 넣고 먹다가\n차돌박이 추가!!\n남은거엔 밥+김가루+참기름으로 진짜 남기는거 없이 싸악 다 먹었어요..\n왜 이제 알았나 후회ㅠㅠ\n오징어도 통으로 들어가있어서 일단 뜯으면서부터 감탄!!\n거기다 보들보들해서 질기지도않고 최고네요!||첨 시켜 봤는데~ 맛있네여 딱~ 제 입맛..\n요즘 오징어도 비싼데 두마리 정도 들어있구여 통으로 들어있네여~ 저는 야채 넣고 볶아서 먹었는데 맵고 맛있어여~~ 저도 한 매움 하는데. 먹으면서 쓰읍~~ 소리 계속 냈습니다~~ 또 시킬께여~^||진짜 핵매움. 근데 맛있음. 맛있는 매운맛임. 야채넣고 먹으니깐 진짜 맛있음. 또 구매의사있음"


    chat_template = ChatPromptTemplate.from_messages( [
        SystemMessage(
            content = '''
            당신은 식품 관련 상품 리뷰 요약 프로그램입니다. 
            아래의 user ,context를 참고하세요
            
            user: {userinfo}
            context: {context}

            user은 구매자의 희망 사항 입니다.
            context은 구매자가 생각하는 상품의 중요사항 입니다.
            
            아래 규칙에 맞추어 user와 context를 반영한 리뷰 요약을 해주세요.
            
            1.  pros에는 긍정적인 의견,
                cons에는 부정적인 의견,
                final에는 장점과 단점을 잘 요약하고 review들의 다수의 의견을 언급하고 상품을 살 때 주의사항도 언급하여 주세요.
                
                
            2. 아래와 같이 json 형식으로 리뷰 결과를 작성해주세요.
                {{
                    "pros": "",
                    "cons": "",
                    "final": ""
                }}
    
            3. 한국말(korean)로 번역해주세요.
            
            4. 결과를 1500자 이내로 답해주세요.
            
            5. reviewlist에 대한 언급은 하지마세요.
            
            6. 의견 반영 여부를 언급하지 말고 바로 본론을 작성하세요. 
            
            7. pros와 cons는 구체적인 예시도 들어주세요.
            
            '''
        ),
        HumanMessage(
            content=" review list:{review_list}"),
    ])



    chain =  chat_template  |llm

    result= chain.invoke({"userinfo":user_info,"context":context, "review_list":review_list_soup})
    
    
    return result.content