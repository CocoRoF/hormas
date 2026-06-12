import os
from ..utils.util_module import (
    review_analyzer,
    norm_responder,
    responder_nocot,
    responder_basic,
    responder_com_name,
    responder_cc,
    responder_cgc,
    review_analyzer_zerocot,
)
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


class ReviewResponder:
    def __init__(
        self,
        api_key: str,
        analyzer_prompt_number: int = 0,
        analyzer_temperature: float = 0,
        responder_temperature: float = 0,
        responder_name: str = None,
        header: str = None,
        footer: str = None,
        contact: str = None,
        rag: bool = False,
        memory: bool = False,
        rag_list: list[str] = None,
        analysis_model_name: str = "gpt-4-0125-preview",
        nocot: bool = False,
        model_name: str = "gpt-4-0125-preview",
    ):
        self.api_key = api_key
        self.analyzer_prompt_number = analyzer_prompt_number
        self.analyzer_temperature = analyzer_temperature
        self.responder_temperature = responder_temperature
        self.responder_name = responder_name
        self.header = header
        self.footer = footer
        self.rag = rag
        self.rag_list = rag_list
        self.retriever = None
        self.memory = memory
        self.contact = contact
        self.analysis_model_name = analysis_model_name
        self.nocot = nocot
        self.model_name = model_name

        os.environ["OPENAI_API_KEY"] = self.api_key
        if self.rag:
            self.vectorstore = FAISS.from_texts(
                self.rag_list, embedding=OpenAIEmbeddings()
            )
            self.retriever = self.vectorstore.as_retriever(
                search_type="similarity_score_threshold",
                search_kwargs={"k": 5, "score_threshold": 0.4},
            )

    def Analysis(self, review_text, value_return: bool = False):
        result = review_analyzer(
            review_text,
            self.analyzer_prompt_number,
            self.analyzer_temperature,
            self.analysis_model_name,
        )
        self.review_sentiment = result["User_Sentiment"]
        self.review_emotion = result["User_Emotion"]
        self.review_intention = result["User_Intention"]

        if value_return:
            return result

    def Response(
        self,
        review_text,
        method: str = "RAAM",
        review_sentiment: str = None,
        review_emotion: str = None,
        review_intention: str = None,
    ):
        if method == "normal":
            response = norm_responder(
                review_text, self.responder_temperature, model_name=self.model_name
            )

        elif method == "RAAM":
            if (
                review_sentiment == None
                or review_emotion == None
                or review_intention == None
            ):
                self.Analysis(review_text)
                review_sentiment = review_sentiment or self.review_sentiment
                review_emotion = review_emotion or self.review_emotion
                review_intention = review_intention or self.review_intention

            if self.responder_name:
                if (self.header) and (self.footer):
                    response = responder_cgc(
                        review_text,
                        self.responder_temperature,
                        review_sentiment,
                        review_emotion,
                        review_intention,
                        self.header,
                        self.footer,
                        model_name=self.model_name,
                    )["Final_Response"]
                    print("use cgc")
                    print(response)
                elif self.contact:
                    response = responder_cc(
                        review_text,
                        self.responder_temperature,
                        review_sentiment,
                        review_emotion,
                        review_intention,
                        self.responder_name,
                        self.contact,
                        self.rag,
                        self.retriever,
                        model_name=self.model_name,
                    )["Final_Response"]
                    print("use cc")
                    print(response)
                else:
                    response = responder_com_name(
                        review_text,
                        self.responder_temperature,
                        review_sentiment,
                        review_emotion,
                        review_intention,
                        self.responder_name,
                        self.rag,
                        self.retriever,
                        model_name=self.model_name,
                    )["Final_Response"]
                    print("use com")
                    print(response)
            else:
                if self.nocot:
                    response = responder_nocot(
                        review_text,
                        self.responder_temperature,
                        review_sentiment,
                        review_emotion,
                        review_intention,
                        model_name=self.model_name,
                    )["Response"]
                    print("use nocot")
                    print(response)
                else:
                    response = responder_basic(
                        review_text,
                        self.responder_temperature,
                        review_sentiment,
                        review_emotion,
                        review_intention,
                        self.rag,
                        self.retriever,
                        model_name=self.model_name,
                    )["Final_Response"]
                    print("use basic")
                    print(response)
                    
        elif method == "final":
            anal_result, result = review_analyzer_zerocot(
                review_text,
                self.responder_temperature,     
                self.analyzer_temperature,
                self.model_name,
                self.analysis_model_name,
                self.responder_name,
                self.contact,
                self.rag,
                self.retriever,
            )
            
            sentiment = anal_result["User_Sentiment"]
            emotion = anal_result["User_Emotion"]
            intention = anal_result["User_Intention"]
            result = result["Response"]
            urgency = anal_result["Review_Urgency"]
            response = [sentiment, emotion, intention, result, urgency]
            
        else:
            print("Error Occur. Please select correct method.")

        return response
