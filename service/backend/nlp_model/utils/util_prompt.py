from langchain.prompts import ChatPromptTemplate


def response_prompt_selector(prompt_num: int, rag: bool = False):
    if prompt_num == 0:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """As a marketing manager managing online customer reviews, write a response to the following 'Review'.\n\nWhen composing your reply, it is important to keep 'Customer Sentiment', 'Customer Emotion' and 'Customer Intention' in mind.\n\nYour answer must follow this 'Format' below.\nFormat:\n(Responding to Customer Sentiment) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Emotion) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Intention) + "(The sentence in the customer review that is the reason for generating that response.)"\n\nThe Final Generated Response to that Customer Review = Your Final Response""",
                ),
                (
                    "human",
                    "Customer Sentiment:\n{customer_sentiment}\n\nCustomer Emotion:\n{customer_emotion}\n\nCustomer Intention:\n{customer_intention}\n\nReview:\n{review}",
                ),
            ]
        )
    if prompt_num == 0 and rag:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """As a marketing manager managing online customer reviews, write a response to the following 'Review'.\n\nWhen composing your reply, it is important to keep 'Customer Sentiment', 'Customer Emotion' and 'Customer Intention' in mind.\n\nUse the following pieces of retrieved context to answer the question.\n\nContext: {context}\n\nYour answer must follow this 'Format' below.\nFormat:\n(Responding to Customer Sentiment) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Emotion) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Intention) + "(The sentence in the customer review that is the reason for generating that response.)"\n\nThe Final Generated Response to that Customer Review = Your Final Response""",
                ),
                (
                    "human",
                    "Customer Sentiment:\n{customer_sentiment}\n\nCustomer Emotion:\n{customer_emotion}\n\nCustomer Intention:\n{customer_intention}\n\nReview:\n{review}",
                ),
            ]
        )
    if prompt_num == 1:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """As a marketing manager managing online customer reviews, write a response to the following 'Review'.\n\nWhen composing your reply, it is important to keep 'Customer Sentiment', 'Customer Emotion' and 'Customer Intention' in mind.\n\nYour answer must follow this 'Format' below.\nFormat:\n"(Greetings including company name)"\n(Responding to Customer Sentiment) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Emotion) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Intention) + "(The sentence in the customer review that is the reason for generating that response.)"\n\nThe Final Generated Response to that Customer Review = Your Final Response""",
                ),
                (
                    "human",
                    "Company name:\n{company_name}\n\nCustomer Sentiment:\n{customer_sentiment}\n\nCustomer Emotion:\n{customer_emotion}\n\nCustomer Intention:\n{customer_intention}\n\nReview:\n{review}",
                ),
            ]
        )
    if prompt_num == 1 and rag:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """As a marketing manager managing online customer reviews, write a response to the following 'Review'.\n\nWhen composing your reply, it is important to keep 'Customer Sentiment', 'Customer Emotion' and 'Customer Intention' in mind.\n\nUse the following pieces of retrieved context to answer the question.\n\nContext: {context}\n\nYour answer must follow this 'Format' below.\nFormat:\n"(Greetings including company name)"\n(Responding to Customer Sentiment) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Emotion) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Intention) + "(The sentence in the customer review that is the reason for generating that response.)"\n\nThe Final Generated Response to that Customer Review = Your Final Response""",
                ),
                (
                    "human",
                    "Company name:\n{company_name}\n\nCustomer Sentiment:\n{customer_sentiment}\n\nCustomer Emotion:\n{customer_emotion}\n\nCustomer Intention:\n{customer_intention}\n\nReview:\n{review}",
                ),
            ]
        )
    if prompt_num == 2:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """As a marketing manager managing online customer reviews, write a response to the following 'Review'.\n\nWhen composing your reply, it is important to keep 'Customer Sentiment', 'Customer Emotion' and 'Customer Intention' in mind.\n\nThe given 'Greeting' and 'Contact Information' message must be included.\n\nThe Final Response must be generated.\n\nYour answer must follow this 'Format' below.\nFormat:\nGreeting = (Greetings message)\n(Responding to Customer Sentiment) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Emotion) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Intention) + "(The sentence in the customer review that is the reason for generating that response.)"\nContact Information = (Contact Information message)\n\nThe Final Generated Response to that Customer Review = Your Final Response""",
                ),
                (
                    "human",
                    "Greeting:\n{greeting}\n\nContact Information:\n{contactinfo}\n\nCustomer Sentiment:\n{customer_sentiment}\n\nCustomer Emotion:\n{customer_emotion}\n\nCustomer Intention:\n{customer_intention}\n\nReview:\n{review}",
                ),
            ]
        )
    if prompt_num == 3:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """As a marketing manager managing online customer reviews, write a response to the following 'Review'.\n\nWhen composing your reply, it is important to keep 'Customer Sentiment', 'Customer Emotion' and 'Customer Intention' in mind. Consider the contacts information.\n\nYour answer must follow this 'Format' below.\nFormat:\n"(Greetings including company name)"\n(Responding to Customer Sentiment) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Emotion) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Intention) + "(The sentence in the customer review that is the reason for generating that response.)"\n\nThe Final Generated Response to that Customer Review = Your Final Response""",
                ),
                (
                    "human",
                    "Company name:\n{company_name}\n\nContact:\n{contact}\n\nCustomer Sentiment:\n{customer_sentiment}\n\nCustomer Emotion:\n{customer_emotion}\n\nCustomer Intention:\n{customer_intention}\n\nReview:\n{review}",
                ),
            ]
        )
    if prompt_num == 3 and rag:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """As a marketing manager managing online customer reviews, write a response to the following 'Review'.\n\nWhen composing your reply, it is important to keep 'Customer Sentiment', 'Customer Emotion' and 'Customer Intention' in mind.\n\nConsider the contacts information.\n\nUse the following pieces of retrieved context to answer the question.\n\nContext: {context}\n\nYour answer must follow this 'Format' below.\nFormat:\n"(Greetings including company name)"\n(Responding to Customer Sentiment) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Emotion) + "(The sentence in the customer review that is the reason for generating that response.)"\n(Responding to Customer Intention) + "(The sentence in the customer review that is the reason for generating that response.)"\n\nThe Final Generated Response to that Customer Review = Your Final Response""",
                ),
                (
                    "human",
                    "Company name:\n{company_name}\n\nContact:\n{contact}\n\nCustomer Sentiment:\n{customer_sentiment}\n\nCustomer Emotion:\n{customer_emotion}\n\nCustomer Intention:\n{customer_intention}\n\nReview:\n{review}",
                ),
            ]
        )
    # prompt number 4
    # COT를 사용하지 않는 prompt를 작성.
    if prompt_num == 4:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """As a marketing manager managing online customer reviews, write a response to the following 'Review'.\n\nWhen composing your reply, it is important to keep 'Customer Sentiment', 'Customer Emotion' and 'Customer Intention' in mind. Consider the contacts information.""",
                ),
                (
                    "human",
                    "Customer Sentiment:\n{customer_sentiment}\n\nCustomer Emotion:\n{customer_emotion}\n\nCustomer Intention:\n{customer_intention}\n\nReview:\n{review}",
                ),
            ]
        )

    return prompt


def analysis_prompt_selector(prompt_num: int):
    function_list = [
        [
            {
                "name": "Describer",
                "description": "Analyze the following Review",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "User_Sentiment": {
                            "type": "string",
                            "enum": ["Positive", "Neutral", "Negative"],
                            "description": "Sentiment Analysis of the 'Review'",
                        },
                        "User_Emotion": {
                            "type": "string",
                            "enum": [
                                "Anger",
                                "Disgust",
                                "Fear",
                                "Happiness",
                                "Contempt",
                                "Sadness",
                                "Surprise",
                            ],
                            "description": "Emotion Analysis of the 'Review'",
                        },
                        "User_Intention": {
                            "type": "string",
                            "enum": [
                                "Complaint",
                                "Expressing Dissatisfaction",
                                "Warning Others",
                                "Feedback",
                                "Sharing Experience",
                                "Expressing Satisfaction",
                                "Praise",
                                "Recommendation",
                            ],
                            "description": "Intention Analysis of the 'Review'",
                        },
                    },
                    "required": ["User_Sentiment", "User_Emotion", "User_Intention"],
                },
            }
        ],
    ]

    return function_list[prompt_num]

def Response_output_selector(prompt_num: int):
    function_list = [
        [
            {
                "name": "Responder",
                "description": "Respond appropriately to the following customer 'Reviews'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Responding_to_Customer_Sentiment": {
                            "type": "string",
                            "description": "Responding to Customer Sentiment",
                        },
                        "Sentiment_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Sentiment'",
                        },
                        "Responding_to_Customer_Emotion": {
                            "type": "string",
                            "description": "Responding to Customer Emotion",
                        },
                        "Emotion_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Emotion'",
                        },
                        "Responding_to_Customer_Intention": {
                            "type": "string",
                            "description": "Emotion Analysis of the 'Review'",
                        },
                        "Intention_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Intention'",
                        },
                        "Final_Response": {
                            "type": "string",
                            "description": "The Final Generated Response to Customer Review",
                        },
                    },
                    "required": [
                        "Responding_to_Customer_Sentiment",
                        "Sentiment_Reason",
                        "Responding_to_Customer_Emotion",
                        "Emotion_Reason",
                        "Responding_to_Customer_Intention",
                        "Intention_Reason",
                        "Final_Response",
                    ],
                },
            }
        ],
        [
            {
                "name": "Responder",
                "description": "Respond appropriately to the following customer 'Reviews'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Greeting": {
                            "type": "string",
                            "description": "Greeting Message",
                        },
                        "Responding_to_Customer_Sentiment": {
                            "type": "string",
                            "description": "Responding to Customer Sentiment",
                        },
                        "Sentiment_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Sentiment'",
                        },
                        "Responding_to_Customer_Emotion": {
                            "type": "string",
                            "description": "Responding to Customer Emotion",
                        },
                        "Emotion_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Emotion'",
                        },
                        "Responding_to_Customer_Intention": {
                            "type": "string",
                            "description": "Emotion Analysis of the 'Review'",
                        },
                        "Intention_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Intention'",
                        },
                        "Final_Response": {
                            "type": "string",
                            "description": "The Final Generated Response to Customer Review",
                        },
                    },
                    "required": [
                        "Greeting",
                        "Responding_to_Customer_Sentiment",
                        "Sentiment_Reason",
                        "Responding_to_Customer_Emotion",
                        "Emotion_Reason",
                        "Responding_to_Customer_Intention",
                        "Intention_Reason",
                        "Final_Response",
                    ],
                },
            }
        ],
        [
            {
                "name": "Responder",
                "description": "Respond appropriately to the following customer 'Reviews'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Greeting": {
                            "type": "string",
                            "description": "Generate Greeting Message",
                        },
                        "Responding_to_Customer_Sentiment": {
                            "type": "string",
                            "description": "Responding to Customer Sentiment",
                        },
                        "Sentiment_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Sentiment'",
                        },
                        "Responding_to_Customer_Emotion": {
                            "type": "string",
                            "description": "Responding to Customer Emotion",
                        },
                        "Emotion_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Emotion'",
                        },
                        "Responding_to_Customer_Intention": {
                            "type": "string",
                            "description": "Emotion Analysis of the 'Review'",
                        },
                        "Intention_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Intention'",
                        },
                        "Contact_Information": {
                            "type": "string",
                            "description": "Generate Contact_Information",
                        },
                        "Final_Response": {
                            "type": "string",
                            "description": "The Final Generated Response to Customer Review",
                        },
                    },
                    "required": [
                        "Greeting",
                        "Responding_to_Customer_Sentiment",
                        "Sentiment_Reason",
                        "Responding_to_Customer_Emotion",
                        "Emotion_Reason",
                        "Responding_to_Customer_Intention",
                        "Intention_Reason",
                        "Contact_Information",
                        "Final_Response",
                    ],
                },
            }
        ],
        # num 3. COT를 사용하지 않는 경우. 최종 답변만 생성하도록 함.
        [
            {
                "name": "Responder",
                "description": "Respond appropriately to the following customer 'Reviews'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Greeting": {
                            "type": "string",
                            "description": "Generate Greeting Message",
                        },
                        "Responding_to_Customer_Sentiment": {
                            "type": "string",
                            "description": "Responding to Customer Sentiment",
                        },
                        "Sentiment_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Sentiment'",
                        },
                        "Responding_to_Customer_Emotion": {
                            "type": "string",
                            "description": "Responding to Customer Emotion",
                        },
                        "Emotion_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Emotion'",
                        },
                        "Responding_to_Customer_Intention": {
                            "type": "string",
                            "description": "Emotion Analysis of the 'Review'",
                        },
                        "Intention_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Intention'",
                        },
                        "Final_Response": {
                            "type": "string",
                            "description": "The Final Generated Response to Customer Review",
                        },
                    },
                    "required": [
                        "Greeting",
                        "Responding_to_Customer_Sentiment",
                        "Sentiment_Reason",
                        "Responding_to_Customer_Emotion",
                        "Emotion_Reason",
                        "Responding_to_Customer_Intention",
                        "Intention_Reason",
                        "Final_Response",
                    ],
                },
            }
        ],
        # num 4. COT를 사용하지 않는 경우. 최종 답변만 생성하도록 함.
        [
            {
                "name": "Responder",
                "description": "Respond appropriately to the following customer 'Reviews'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Response": {
                            "type": "string",
                            "description": "Response to Customer Review",
                        },
                    },
                    "required": ["Response"],
                },
            }
        ],
    ]
    return function_list[prompt_num]

def output_function(prompt_name:str = None):
    if prompt_name == "sentiment":
        output = {
            "name": "Describer",
            "description": "Analyze the following Review",
            "parameters": {
                "type": "object",
                "properties": {
                    "User_Sentiment": {
                        "type": "string",
                        "enum": ["Positive", "Neutral", "Negative"],
                    },
                },
                "required": ["User_Sentiment"],
            },
        }

    elif prompt_name == "emotion":
        output = {
            "name": "Describer",
            "description": "Analyze the following Review",
            "parameters": {
                "type": "object",
                "properties": {
                    "User_Emotion": {
                        "type": "string",
                        "enum": [
                            "Anger",
                            "Disgust",
                            "Fear",
                            "Happiness",
                            "Contempt",
                            "Sadness",
                            "Surprise",
                        ],
                    },
                },
                "required": ["User_Emotion"],
            },
        }

    elif prompt_name == "intention":
        output = {
            "name": "Describer",
            "description": "Analyze the following Review",
            "parameters": {
                "type": "object",
                "properties": {
                    "User_Intention": {
                        "type": "string",
                        "enum": [
                            "Complaint",
                            "Expressing Dissatisfaction",
                            "Warning Others",
                            "Feedback",
                            "Sharing Experience",
                            "Expressing Satisfaction",
                            "Praise",
                            "Recommendation",
                        ],
                    },
                },
                "required": ["User_Intention"],
            },
        }

    elif prompt_name == "response":
        output = {
            "name": "Describer",
            "description": "Respond appropriately to the following customer 'Reviews'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "Response": {
                        "type": "string",
                    },
                },
                "required": ["Response"],
            },
        }
        
    elif prompt_name == "urgency_level":
        output = {
            "name": "Describer",
            "description": "Determine how urgent a given customer's 'Review' is.",
            "parameters": {
                "type": "object",
                "properties": {
                    "Urgency_Level": {
                        "type": "string",
                        "enum": [
                            'Urgent',
                            'Medium',
                            'Not Urgent',
                        ]
                    },
                },
                "required": ["Urgency_Level"],
            },
        }
    
    elif prompt_name == "zero_response":
        output = {
            "name": "Describer",
            "description": "Respond appropriately to the following customer 'Reviews'",
            "parameters": {
                "type": "object",
                "properties": {
                    "Response": {
                        "type": "string",
                        "description": "Response to Customer Review",
                    },
                },
                "required": ["Response"],
            },
        }

    elif prompt_name == "zerocot":
        output = {
            "name": "Describer",
            "description": "Analyze the following Review",
            "parameters": {
                "type": "object",
                "properties": {
                    "User_Sentiment": {
                        "type": "string",
                        "enum": ["Positive", "Neutral", "Negative"],
                    },
                    "User_Emotion": {
                        "type": "string",
                        "enum": [
                            "Anger",
                            "Disgust",
                            "Fear",
                            "Happiness",
                            "Contempt",
                            "Sadness",
                            "Surprise",
                        ],
                    },
                    "User_Intention": {
                        "type": "string",
                        "enum": [
                            "Complaint",
                            "Expressing Dissatisfaction",
                            "Warning Others",
                            "Feedback",
                            "Sharing Experience",
                            "Expressing Satisfaction",
                            "Praise",
                            "Recommendation",
                        ],
                        "lang": "ko"
                    },
                    "Response": {
                        "type": "string",
                    },
                },
                "required": ["User_Sentiment", "User_Emotion", "User_Intention", "Response"],
            },
        }

    elif prompt_name == "total_extraction":
        output = {
            "name": "Describer",
            "description": "Analyze the following Review",
            "parameters": {
                "type": "object",
                "properties": {
                    "User_Sentiment": {
                        "type": "string",
                        "enum": ["Positive", "Neutral", "Negative"],
                    },
                    "User_Emotion": {
                        "type": "string",
                        "enum": [
                            "Anger",
                            "Disgust",
                            "Fear",
                            "Happiness",
                            "Contempt",
                            "Sadness",
                            "Surprise",
                            "Neutral",
                        ],
                    },
                    "User_Intention": {
                        "type": "string",
                        "enum": [
                            "Complaint",
                            "Expressing Dissatisfaction",
                            "Warning Others",
                            "Feedback",
                            "Sharing Experience",
                            "Expressing Satisfaction",
                            "Praise",
                            "Recommendation",
                        ],
                    },
                },
                "required": ["User_Sentiment", "User_Emotion", "User_Intention"],
            },
        }
    
    elif prompt_name == "zero_cot":
        output = {
            "name": "Describer",
            "description": "Analyze the following Review",
            "parameters": {
                "type": "object",
                "properties": {
                    "User_Sentiment": {
                        "type": "string",
                        "enum": ["Positive", "Neutral", "Negative"],
                    },
                    "User_Emotion": {
                        "type": "string",
                        "enum": [
                            "Anger",
                            "Disgust",
                            "Fear",
                            "Happiness",
                            "Contempt",
                            "Sadness",
                            "Surprise",
                        ],
                    },
                    "User_Intention": {
                        "type": "string",
                        "enum": [
                            "Complaint",
                            "Expressing Dissatisfaction",
                            "Warning Others",
                            "Feedback",
                            "Sharing Experience",
                            "Expressing Satisfaction",
                            "Praise",
                            "Recommendation",
                        ],
                    },
                },
                "required": ["User_Sentiment", "User_Emotion", "User_Intention"],
            },
        }

    else:
        raise Exception("Please Select Correct 'prompt_name' from ['sentiment', 'emotion', 'intention', 'response']")

    return output