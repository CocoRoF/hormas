from sentence_transformers import SentenceTransformer
model = SentenceTransformer("Qwen/Qwen3-Embedding-0.6B")

def encode_text(text, pair):
    query_embeddings = model.encode(text, prompt_name="query")
    document_embeddings = model.encode(pair)
    similarity = model.similarity(query_embeddings, document_embeddings)

    return similarity.tolist()[0][0]

if __name__ == "__main__":
    text = "This is a sample text."
    pair = "This is the second pair."
    similarity_scores = encode_text(text, pair)
    print(similarity_scores)  # Output similarity scores for the pairs