import os
from pathlib import Path
from operator import itemgetter
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage

from .util_prompt import (
    analysis_prompt_selector,
    response_prompt_selector,
    Response_output_selector,
    output_function,
)

NLP_BASE_DIR = Path(__file__).resolve().parent.parent
API_KEY_PATH = str(NLP_BASE_DIR / "Openai_API_Key.txt")
GOOGLE_API_PATH = str(NLP_BASE_DIR / "Google_API_Key.txt")

# API Load
with open(API_KEY_PATH, "r") as api:
    os.environ["OPENAI_API_KEY"] = api.read()

with open(GOOGLE_API_PATH, "r") as google_api:
    os.environ["GOOGLE_API_KEY"] = google_api.read()


# 리뷰 분석을 수행하는 모듈
# Input: User_Review, Analysis_Prompt, Basic_System_Message ========> Output: Analysis_Result (Parsed by Analysis_Prompt)
# 기본적으로 system message가 Template으로 제시되며, analysis_prompt를 통해 Output parsing에 대한 설명을 추가적으로 제공함. 현재 analysis prompt는 0번 하나만 존재함.
# 기본 답변 모듈을 제외한 대부분의 답변에서 사용되고 있음.
# 따라서 analyzer_prompt의 작성에 따라서 어떤 방식으로 output을 산출할지 결정하게 됨.
def review_analyzer(
    user_review: str,
    analyzer_prompt_number: int = 0,
    analyzer_temperature: float = 0,
    model_name: str = "gpt-4-0125-preview",
):
    function_prompt = analysis_prompt_selector(prompt_num=analyzer_prompt_number)
    analyzer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "As an online hotel manager, analyze customer reviews."),
            ("human", "{analysis}"),
        ]
    )

    analyzer_model = ChatOpenAI(
        model=model_name, temperature=analyzer_temperature
    ).bind(function_call={"name": "Describer"}, functions=function_prompt)
    runnable = (
        {"analysis": RunnablePassthrough()}
        | analyzer_prompt
        | analyzer_model
        | JsonOutputFunctionsParser()
    )
    result = runnable.invoke(user_review)
    return result


def google_review_analyzer(user_review: str, model_name: str = "gemini-pro"):
    analyzer_model = ChatGoogleGenerativeAI(
        model=model_name, convert_system_message_to_human=True
    )
    result = analyzer_model.invoke(
        [
            SystemMessage(
                content="Analyze Text. Answer only 'Poristive', 'Neutral', 'Negative'"
            ),
            HumanMessage(content=user_review),
        ]
    )
    return result


# 기본 답변모듈
# Input: User_Review =========> Output: Response
# 아무런 프롬프트도 제공하지 않으며, Respond를 수행하라는 명령만 제공됨
def norm_responder(
    user_review: str,
    responder_temperature: float = 0,
    model_name: str = "gpt-4-0125-preview",
):
    responder_model = ChatOpenAI(model=model_name, temperature=responder_temperature)
    norm_prompt = ChatPromptTemplate.from_messages(
        [("system", "Respond to review"), ("human", "{review}")]
    )

    try:
        responder_chain = norm_prompt | responder_model
        response = responder_chain.invoke({"review": user_review})
        return response.content

    except:
        print("Responding Error.")
        response = "Responding Error"
        return response


# Chain Of Thought를 사용하지 않는 답변 모듈.
# Input: User_Review =========> Output: Response
# 감정, 감성, 의도를 이용하기는 하나, COT 방식으로 답변을 작성하지 않음.
def responder_nocot(
    user_review: str,
    responder_temperature: float = 0,
    User_Sentiment: str = None,
    User_Emotion: str = None,
    User_Intention: str = None,
    model_name: str = "gpt-4-0125-preview",
):
    responder_prompt = response_prompt_selector(4)
    responder_model = ChatOpenAI(model=model_name, temperature=responder_temperature)
    responder_function = Response_output_selector(prompt_num=4)

    try:
        response_chain = (
            responder_prompt
            | responder_model.bind(
                function_call={"name": "Responder"}, functions=responder_function
            )
            | JsonOutputFunctionsParser()
        )
        response = response_chain.invoke(
            {
                "customer_sentiment": User_Sentiment,
                "customer_emotion": User_Emotion,
                "customer_intention": User_Intention,
                "review": user_review,
            }
        )
    except:
        print("Responding Error.")
        response = "Responding Error"
    return response


# 기본적인 Basic Responder. RAG기능을 사용할지 아닐지를 결정할 수 있음.
def responder_basic(
    user_review: str,
    responder_temperature: float = 0,
    User_Sentiment: str = None,
    User_Emotion: str = None,
    User_Intention: str = None,
    rag: bool = False,
    vectorstore_retriever=None,
    model_name: str = "gpt-4-0125-preview",
):
    responder_prompt = response_prompt_selector(0, rag=rag)
    responder_model = ChatOpenAI(model=model_name, temperature=responder_temperature)
    responder_function = Response_output_selector(prompt_num=0)

    if rag:
        print("resp_basic_rag")
        try:
            response_chain = (
                {
                    "context": itemgetter("review") | vectorstore_retriever,
                    "customer_sentiment": itemgetter("customer_sentiment"),
                    "customer_emotion": itemgetter("customer_emotion"),
                    "customer_intention": itemgetter("customer_intention"),
                    "review": itemgetter("review"),
                }
                | responder_prompt
                | responder_model.bind(
                    function_call={"name": "Responder"}, functions=responder_function
                )
                | JsonOutputFunctionsParser()
            )
            response = response_chain.invoke(
                {
                    "customer_sentiment": User_Sentiment,
                    "customer_emotion": User_Emotion,
                    "customer_intention": User_Intention,
                    "review": user_review,
                }
            )
        except:
            print("Responding Error.")
            response = "Responding Error"

    else:
        try:
            response_chain = (
                responder_prompt
                | responder_model.bind(
                    function_call={"name": "Responder"}, functions=responder_function
                )
                | JsonOutputFunctionsParser()
            )
            response = response_chain.invoke(
                {
                    "customer_sentiment": User_Sentiment,
                    "customer_emotion": User_Emotion,
                    "customer_intention": User_Intention,
                    "review": user_review,
                }
            )
        except:
            print("Responding Error.")
            response = "Responding Error"

    return response


# 사용자의 정보(회사 이름 정도)를 입력할 수 있는 모듈. RAG 기능 사용 가능. 간단한 인사말을 넣도록 설정함.
def responder_com_name(
    user_review: str,
    responder_temperature: float = 0,
    User_Sentiment: str = None,
    User_Emotion: str = None,
    User_Intention: str = None,
    Company_Name: str = None,
    rag: bool = False,
    vectorstore_retriever=None,
    model_name: str = "gpt-4-0125-preview",
):
    responder_prompt = response_prompt_selector(1, rag=rag)
    responder_model = ChatOpenAI(model=model_name, temperature=responder_temperature)
    responder_function = Response_output_selector(prompt_num=1)

    if rag:
        try:
            response_chain = (
                {
                    "context": itemgetter("review") | vectorstore_retriever,
                    "company_name": itemgetter("company_name"),
                    "customer_sentiment": itemgetter("customer_sentiment"),
                    "customer_emotion": itemgetter("customer_emotion"),
                    "customer_intention": itemgetter("customer_intention"),
                    "review": itemgetter("review"),
                }
                | responder_prompt
                | responder_model.bind(
                    function_call={"name": "Responder"}, functions=responder_function
                )
                | JsonOutputFunctionsParser()
            )
            response = response_chain.invoke(
                {
                    "company_name": Company_Name,
                    "customer_sentiment": User_Sentiment,
                    "customer_emotion": User_Emotion,
                    "customer_intention": User_Intention,
                    "review": user_review,
                }
            )

        except:
            print("Responding Error.")
            response = "Responding Error"

    else:
        try:
            response_chain = (
                responder_prompt
                | responder_model.bind(
                    function_call={"name": "Responder"}, functions=responder_function
                )
                | JsonOutputFunctionsParser()
            )
            response = response_chain.invoke(
                {
                    "company_name": Company_Name,
                    "customer_sentiment": User_Sentiment,
                    "customer_emotion": User_Emotion,
                    "customer_intention": User_Intention,
                    "review": user_review,
                }
            )
        except:
            print("Responding Error.")
            response = "Responding Error"

    return response


def responder_cc(
    user_review: str,
    responder_temperature: float = 0,
    User_Sentiment: str = None,
    User_Emotion: str = None,
    User_Intention: str = None,
    Company_Name: str = None,
    Contact: str = None,
    rag: bool = False,
    vectorstore_retriever=None,
    model_name: str = "gpt-4-0125-preview",
):
    responder_prompt = response_prompt_selector(3, rag=rag)
    responder_model = ChatOpenAI(model=model_name, temperature=responder_temperature)
    responder_function = Response_output_selector(prompt_num=3)
    if rag:
        try:
            response_chain = (
                {
                    "context": itemgetter("review") | vectorstore_retriever,
                    "company_name": itemgetter("company_name"),
                    "contact": itemgetter("contact"),
                    "customer_sentiment": itemgetter("customer_sentiment"),
                    "customer_emotion": itemgetter("customer_emotion"),
                    "customer_intention": itemgetter("customer_intention"),
                    "review": itemgetter("review"),
                }
                | responder_prompt
                | responder_model.bind(
                    function_call={"name": "Responder"}, functions=responder_function
                )
                | JsonOutputFunctionsParser()
            )
            response = response_chain.invoke(
                {
                    "company_name": Company_Name,
                    "contact": Contact,
                    "customer_sentiment": User_Sentiment,
                    "customer_emotion": User_Emotion,
                    "customer_intention": User_Intention,
                    "review": user_review,
                }
            )

        except:
            print("Responding Error.")
            response = "Responding Error"

    else:
        try:
            response_chain = (
                responder_prompt
                | responder_model.bind(
                    function_call={"name": "Responder"}, functions=responder_function
                )
                | JsonOutputFunctionsParser()
            )
            response = response_chain.invoke(
                {
                    "company_name": Company_Name,
                    "contact": Contact,
                    "customer_sentiment": User_Sentiment,
                    "customer_emotion": User_Emotion,
                    "customer_intention": User_Intention,
                    "review": user_review,
                }
            )
        except:
            print("Responding Error.")
            response = "Responding Error"
    return response


def responder_cgc(
    user_review: str,
    responder_temperature: float = 0,
    User_Sentiment: str = None,
    User_Emotion: str = None,
    User_Intention: str = None,
    Head: str = None,
    Foot: str = None,
    model_name: str = "gpt-4-0125-preview",
    ):
    responder_prompt = response_prompt_selector(2)
    responder_model = ChatOpenAI(model=model_name, temperature=responder_temperature)
    responder_function = Response_output_selector(prompt_num=2)

    try:
        response_chain = (
            responder_prompt
            | responder_model.bind(
                function_call={"name": "Responder"}, functions=responder_function
            )
            | JsonOutputFunctionsParser()
        )
        response = response_chain.invoke(
            {
                "greeting": Head,
                "contactinfo": Foot,
                "customer_sentiment": User_Sentiment,
                "customer_emotion": User_Emotion,
                "customer_intention": User_Intention,
                "review": user_review,
            }
        )
    except:
        print("Responding Error.")
        response = "Responding Error"
    return response

# 제로샷 cot를 활용해 감성, 감정, 의도를 순차적으로 추출하도록 요청하는 경우.

def review_analyzer_zerocot(
    user_review: str, 
    responder_temperature: float = 0, 
    analyzer_temperature: float = 0, 
    response_model_name: str = "gpt-4o-2024-05-13", 
    analysis_model_name: str = "gpt-4o-2024-05-13",
    Company_Name: str = None,
    Contact: str = None,
    rag: bool = False,
    vectorstore_retriever=None,
):
    print("Analysis Start")
    analyzer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Analyze the sentiment, emotion, and intention in the user's review. Step by step."),
            ("human", "{review}"),
        ]
    )

    analyzer_model = ChatOpenAI(model=analysis_model_name, temperature=analyzer_temperature).bind(function_call={"name": "Describer"}, functions=[output_function(prompt_name="total_extraction")])
    analyzer_chain = {"review": RunnablePassthrough()} | analyzer_prompt | analyzer_model | JsonOutputFunctionsParser()

    analyzer_result = analyzer_chain.invoke({"review": user_review})
    
    print("Analize Lvl of Urgency")
    urgency_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "As a review manager, assess how urgent it is to respond to a given customer's review."),
            ("human", "{review}"),
        ]
    )

    urgency_model = ChatOpenAI(model=analysis_model_name, temperature=analyzer_temperature).bind(function_call={"name": "Describer"}, functions=[output_function(prompt_name="urgency_level")])
    urgency_chain = {"review": RunnablePassthrough()} | urgency_prompt | urgency_model | JsonOutputFunctionsParser()

    urgency_result = urgency_chain.invoke({"review": user_review})
    
    if rag:
        print("Response: RAG MODE")
        response_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "As a marketing manager managing online customer reviews, write a response to the following 'Review'.\n\nWhen composing your reply, consider 'Customer Sentiment', 'Customer Emotion' and 'Customer Intention'. The given 'Responder Name' and 'Contact Information' must be included. Additionally, use the following pieces of retrieved context to answer the question \nContext: {context}"),
                ("human", "Responder Name:\n{company_name}\n\nContact:\n{contact}\n\nCustomer Sentiment:\n{sentiment}\n\nCustomer Emotion:\n{emotion}\n\nCustomer Intention:\n{intention}\n\nReview:\n{review}")
            ]
        )
        
        response_model = ChatOpenAI(model=response_model_name, temperature=responder_temperature).bind(function_call={"name": "Describer"}, functions=[output_function(prompt_name="zero_response")])
        
        response_chain = (
            {
                "context": itemgetter("review") | vectorstore_retriever,
                "company_name": itemgetter("company_name"),
                "contact": itemgetter("contact"),
                "sentiment": itemgetter("sentiment"),
                "emotion": itemgetter("emotion"),
                "intention": itemgetter("intention"),
                "review": itemgetter("review"),
            }
            | response_prompt
            | response_model
            | JsonOutputFunctionsParser()
        )
        
        result = response_chain.invoke(
            {
                "company_name": Company_Name,
                "contact": Contact,
                "sentiment": analyzer_result['User_Sentiment'],
                "emotion": analyzer_result['User_Emotion'],
                "intention": analyzer_result['User_Intention'],
                "review": user_review,
            }
        )
        
    else:
        print("Response: NON-RAG MODE")

        response_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", "As a marketing manager managing online customer reviews, write a response to the following 'Review'.\n\nWhen composing your reply, consider 'Customer Sentiment', 'Customer Emotion' and 'Customer Intention'."),
                ("human", "Customer Sentiment:\n{sentiment}\n\nCustomer Emotion:\n{emotion}\n\nCustomer Intention:\n{intention}\n\nReview:\n{review}")
            ]
        )

        response_model = ChatOpenAI(model=response_model_name, temperature=responder_temperature).bind(function_call={"name": "Describer"}, functions=[output_function(prompt_name="zero_response")])
        response_chain = {"sentiment": RunnablePassthrough(), "emotion": RunnablePassthrough(), "intention": RunnablePassthrough(), "review": RunnablePassthrough()} | response_prompt | response_model | JsonOutputFunctionsParser()

        result = response_chain.invoke({"sentiment": analyzer_result['User_Sentiment'], "emotion": analyzer_result['User_Emotion'], "intention": analyzer_result['User_Intention'], "review": user_review})
        
    sentiment_mapping = {
        "Positive": "긍정",
        "Neutral": "중립",
        "Negative": "부정",
    }
    emotion_mapping = {
        "Anger": "화남",
        "Disgust": "역겨움",
        "Fear": "공포",
        "Happiness": "행복",
        "Contempt": "조소",
        "Sadness": "슬픔",
        "Surprise": "놀람",
        "Neutral": "중립"
    }
    intention_mapping = {
        "Complaint": "항의",
        "Expressing Dissatisfaction": "불만족 표출",
        "Warning Others": "타인에게 경고",
        "Feedback": "피드백",
        "Sharing Experience": "경험 공유",
        "Expressing Satisfaction": "만족감 표출",
        "Praise": "칭찬",
        "Recommendation": "추천"
    }
    urgency_mapping = {
        "Urgent": "긴급함",
        "Medium": "중간",
        "Not Urgent": "긴급하지않음",
    }
    
    trans_analyzer_result = {
        'User_Sentiment' : sentiment_mapping[analyzer_result['User_Sentiment']], 
        'User_Emotion' : emotion_mapping[analyzer_result['User_Emotion']], 
        'User_Intention' : intention_mapping[analyzer_result['User_Intention']],
        'Review_Urgency' : urgency_mapping[urgency_result['Urgency_Level']],
    }
    
    print(trans_analyzer_result)

    return trans_analyzer_result, result