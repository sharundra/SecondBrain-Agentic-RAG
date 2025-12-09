from app.graph.retrieval import search_knowledge_base

if __name__ == "__main__":
    # Aisa sawal pucho jo video mein tha
    # query = "What is a recursive splitter?" 
    query = 'What are the principal Upanishads?'
    results = search_knowledge_base(query)
    
    print("\n--- Retrieved Content ---")
    for chunk in results:
        print(chunk[:200] + "...\n")