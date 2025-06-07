import os

from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.output_parsers.openai_functions import JsonOutputFunctionsParser
from .prompt import analysis_prompt_selector, response_prompt_selector, Response_output_selector

# API Load
with open('./Openai_API_Key.txt', 'r') as api:
    os.environ["OPENAI_API_KEY"] = api.read()

# 기본 답변모듈
# Input: User_Review =========> Output: Response
# 아무런 프롬프트도 제공하지 않으며, Respond를 수행하라는 명령만 제공됨
def gpt_norm_responder(user_review:str, responder_temperature:float = 0, model:str = "gpt-4-1106-preview"):
    responder_model = ChatOpenAI(model=model, temperature=responder_temperature)
    norm_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "Respond to review"),
            ("human", "{review}")
        ]
    )
    
    try:
        responder_chain = norm_prompt | responder_model
        response = responder_chain.invoke({"review" : user_review})
        return response.content
    
    except:
        print("Responding Error.")
        response = 'Responding Error'
        return response



# 리뷰 분석을 수행하는 모듈
# Input: User_Review, Analysis_Prompt, Basic_System_Message ========> Output: Analysis_Result (Parsed by Analysis_Prompt)
# 기본적으로 system message가 Template으로 제시되며, analysis_prompt를 통해 Output parsing에 대한 설명을 추가적으로 제공함.
# 따라서 analyzer_prompt의 작성에 따라서 어떤 방식으로 output을 산출할지 결정하게 됨.
def gpt_review_analyzer(user_review:str, analyzer_prompt_number:int = 0, analyzer_temperature:float = 0):
    function_prompt = analysis_prompt_selector(prompt_num=analyzer_prompt_number)
    analyzer_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "As an online hotel manager, analyze customer reviews."),
            ("human", "{analysis}")
        ]
    )
    
    analyzer_model = ChatOpenAI(model="gpt-4-1106-preview", temperature=analyzer_temperature).bind(function_call={"name": "Describer"}, functions=function_prompt)
    runnable = (
        {"analysis": RunnablePassthrough()} 
        | analyzer_prompt 
        | analyzer_model
        | JsonOutputFunctionsParser()
    )
    result = runnable.invoke(user_review)
    return result
    
def gpt_responder(user_review:str, responder_prompt_number:int = 0, responder_temperature:float = 0, User_Sentiment:str = None, User_Emotion:str = None, User_Intention:str = None):
    responder_prompt = response_prompt_selector(responder_prompt_number)
    responder_model = ChatOpenAI(model="gpt-4-1106-preview", temperature=responder_temperature)
    responder_function = Response_output_selector(prompt_num=0)
    
    try:
        response_chain = responder_prompt | responder_model.bind(function_call={"name" : "Responder"}, functions=responder_function) | JsonOutputFunctionsParser()
        response = response_chain.invoke(
            {"customer_sentiment" : User_Sentiment, "customer_emotion" : User_Emotion, "customer_intention" : User_Intention, "review" : user_review})
    except:
        print("Responding Error.")
        response = 'Responding Error'
    return response

