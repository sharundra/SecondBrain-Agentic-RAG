from flashrank import Ranker, RerankRequest
from app.db.vector_store import get_vector_store

# Initialize the Re-ranker 
# 'ms-marco-TinyBERT-L-2-v2' is a famous model which searches for semantic and contexual similarity
ranker = Ranker(model_name="ms-marco-TinyBERT-L-2-v2", cache_dir="./opt")

def advanced_search(query : str, k : int = 5, filter_dict : dict = None, score_threshold : float = 0.6):
    """
    Performs Vector Search + Re-ranking.
    k: Number of final results to return.
    filter_dict: Metadata filters (e.g., {'type': 'pdf'})
    """
    print(f"--- Advanced Search for: '{query}' ---")

    vector_store = get_vector_store()
    initial_docs = vector_store.similarity_search(query, k*3, filter = filter_dict)
    print(f"--- Retrieved {len(initial_docs)} candidates from Pinecone ---")

    if not initial_docs:
        return []
    
    passages = [ {'id' : str(i), 'text' : doc.page_content, 'meta' : doc.metadata} for i, doc in enumerate(initial_docs) ]
    print("--- Re-ranking documents... ---")
    rerank_request = RerankRequest(query = query, passages = passages)
    results = ranker.rerank(rerank_request)

    final_results = []
    for res in results:
        # FlashRank score usually 0 to 1 hota hai
        if res['score'] >= score_threshold:
            final_results.append(res['text'])
        else:
            print(f" Dropped Low Score Result: {round(res['score'], 2)}")

    final_results = final_results[:k]

    if not final_results:
        print("--- No relevant documents found after thresholding ---")
        return []
    
    print(f"--- Selected Top {len(final_results)} most relevant chunks ---")
    return [res['text'] for res in final_results]