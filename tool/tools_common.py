import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# 올림 함수
def up_ten(n):
    return math.ceil(n / 10.0) * 10

# Input Text 속에 Search_text가 있는 경우, insert_text를 삽입 후 반환
def insert_text_after(target_string, search_text, insert_text):
    index = target_string.find(search_text)
    
    if index == -1:
        return target_string

    return target_string[:index + len(search_text)] + insert_text + target_string[index + len(search_text):]


# List 형태로 str 데이터를 입력받아, 해당 데이터의 tfidf 값을 기준으로 코사인 유사도를 계산하여 반환
def tfidf_cos_similarity(list_data:list):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform(list_data)

    cosine_similarities = cosine_similarity(tfidf)
    avg_similarity = cosine_similarities.sum() / (cosine_similarities.shape[0] * cosine_similarities.shape[1] - cosine_similarities.shape[0])
    
    return avg_similarity

# List 형태로 str 데이터를 입력받은 뒤, 해당 데이터를 임베딩하여 코사인 유사도를 계산하여 반환. 이 때 임베딩 모델은 model에서 사용
# 이 때 model은 sentence_transformer의 모델을 사용하게 됨
def embd_cos_similarity(list_data:list, model_name:str = 'all-MiniLM-L12-v2'):
    """
    You can choose Sentence Transformer models below.
    ['all-mpnet-base-v2', 'all-distilroberta-v1', 'all-MiniLM-L12-v2', 'all-MiniLM-L6-v2', 'paraphrase-albert-small-v2']

    Default Model is 'all-MiniLM-L12-v2'.
    """
    model = SentenceTransformer(model_name)
    embeddings = model.encode(list_data, convert_to_tensor=True)
    cosine_similarities = cosine_similarity(embeddings)

    # 모든 유사도의 평균을 계산하기
    avg_similarity = cosine_similarities.sum() / (cosine_similarities.shape[0] * cosine_similarities.shape[1] - cosine_similarities.shape[0])
    return avg_similarity