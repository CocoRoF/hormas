from langchain.prompts import ChatPromptTemplate

def response_prompt_selector(prompt_num: int):
    if prompt_num == 0:
        system_prompt = """You are an expert Marketing Manager specializing in online reputation management. Your task is to craft a thoughtful and effective response to a customer review.

To ensure the highest quality response, you must follow this step-by-step reasoning process before writing the final reply.

**## Step-by-Step Analysis ##**

**Step 1: Analyze Customer Sentiment.**
- Based on the provided 'Customer Sentiment', briefly explain how the overall tone of your response (e.g., apologetic, grateful, neutral) should be shaped.

**Step 2: Analyze Customer Emotion.**
- Based on the 'Customer Emotion', identify the core feeling the customer is expressing (e.g., frustration, delight, disappointment). How will you validate this specific emotion in your response?

**Step 3: Analyze Customer Intention.**
- Based on the 'Customer Intention', determine what the customer hopes to achieve with their review (e.g., receive a solution, warn others, praise the service). What specific action or information must your response contain to address this intention?

**Step 4: Synthesize and Formulate a Strategy.**
- Based on your analysis in steps 1-3, outline a brief strategy for the final response. Mention the key points you will include.

**## Final Response Generation ##**

After completing the analysis above, write the final, polished response to the customer. This response should directly reflect the insights from your step-by-step analysis.

**Final Response to Customer:**
[Your final, well-crafted response goes here]"""

    elif prompt_num == 1:
        system_prompt = """You are a professional Marketing Manager responsible for handling customer feedback. Your goal is to write a personalized and appropriate response to the following customer review, taking into account the provided analysis of their sentiment, emotion, and intention.

Carefully review all the information provided below.

Your final output should be only the direct response to the customer.

Let's think step by step."""
        
    else:
        system_prompt = """As a customer-centric Marketing Manager, your task is to write a public response to a customer review.

**## Guiding Principles for Your Response: ##**
1.  **Acknowledge and Validate:** Your response must acknowledge the customer's experience and validate their feelings, using the provided 'Customer Sentiment' and 'Customer Emotion' as a guide.
2.  **Be Specific:** Directly reference key points from the original 'Review' to show you have read it carefully.
3.  **Address the Intention:** Ensure your reply directly addresses the 'Customer Intention'. If they are seeking a solution, offer one. If they are giving praise, show gratitude.
4.  **Maintain a Professional Tone:** The tone should be professional, empathetic, and aligned with our brand's voice.
5.  **Provide a Clear Call to Action (if necessary):** If follow-up is needed, provide clear instructions for the customer (e.g., "Please contact us at [email/phone]").

Your final output should be ONLY the complete, ready-to-publish response to the customer. Do not include any of your own analysis or notes."""
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                ("human", "Review:\n{review}")
            ]
        )
        
        return prompt
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "Customer Sentiment:\n{customer_sentiment}\n\nCustomer Emotion:\n{customer_emotion}\n\nCustomer Intention:\n{customer_intention}\n\nReview:\n{review}")
        ]
    )
    
    return prompt


def analysis_prompt_selector(prompt_num:int):
    if prompt_num == 0:
        function_prompt = [
            {
                "name": "Describer",
                "description": "Analyze the following 'Review'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "User_Sentiment": {
                            "type": "string",
                            "enum": ['Positive', 'Neutral', 'Negative'],
                            "description": "Sentiment Analysis of the 'Review'"
                        },
                        "User_Emotion": {
                            "type": "string",
                            "enum": ['Anger', 'Disgust', 'Fear', 'Happiness', 'Contempt', 'Sadness', 'Surprise'],
                            "description": "Emotion Analysis of the 'Review'"
                        },
                        "User_Intention": {
                            "type": "string",
                            "description": "Intention Analysis of the 'Review'"
                        },
                    },
                    "required": ["User_Sentiment", "User_Emotion", "User_Intention"]
                }
            }
        ]
    
    return function_prompt

def Response_output_selector(prompt_num:int):
    if prompt_num == 0:
        function_prompt = [
            {
                "name": "Responder",
                "description": "Respond appropriately to the following customer 'Reviews'",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "Responding_to_Customer_Sentiment": {
                            "type": "string",
                            "description": "Responding to Customer Sentiment"
                        },
                        "Sentiment_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Sentiment'"
                        },
                        "Responding_to_Customer_Emotion": {
                            "type": "string",
                            "description": "Responding to Customer Emotion"
                        },
                        "Emotion_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Emotion'"
                        },
                        "Responding_to_Customer_Intention": {
                            "type": "string",
                            "description": "Emotion Analysis of the 'Review'"
                        },
                        "Intention_Reason": {
                            "type": "string",
                            "description": "The sentence in the customer review that is the reason for generating that response to customer 'Intention'"
                        },
                        "Final_Response": {
                            "type": "string",
                            "description": "The Final Generated Response to Customer Review"
                        },
                    },
                    "required": ["Responding_to_Customer_Sentiment", "Sentiment_Reason", "Responding_to_Customer_Emotion", "Emotion_Reason", "Responding_to_Customer_Intention", "Intention_Reason", "Final_Response"]
                }
            }
        ]
    
    return function_prompt
        