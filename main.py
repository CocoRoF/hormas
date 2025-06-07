import pandas as pd
from model.model import HotelReviewTool

df = pd.read_excel('./data/Hotel_Reviews.xlsx')
Tool = HotelReviewTool(df)

analyzed_df = HotelReviewTool.Analysis(method='prompt', analyzer_prompt_number=0, analyzer_temperature=0.1, save_path='./data/Hotel_Reviews_Analyzed.xlsx')
responded_df = HotelReviewTool.Respond(method='prompt', responder_prompt_number=0, responder_temperature=0.1, save_path='./data/Hotel_Reviews_Responded.xlsx')