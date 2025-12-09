from app.db.vector_store import get_vector_store

def search_knowledge_base(query : str, k : int = 3):
    """
    Searches Pinecone for the most relevant chunks.
    k: Number of results to return.
    """
    print(f"--- Searching for: '{query}' ---")
    vector_store = get_vector_store()

    results = vector_store.similarity_search_with_score(query, k=k)
    print(f"--- Found {len(results)} relevant chunks ---")

    knowledge_list = []
    for doc, score in results:
        print(f"   Score: {round(score, 2)} | Source: {doc.metadata.get('source', 'Unknown')}")
        knowledge_list.append(doc.page_content)

    return knowledge_list

        

