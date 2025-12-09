from app.graph.advanced_retrieval import advanced_search

if __name__ == "__main__":
    query = "Explain the architecture of LangGraph"
    
    # 1. Search without Filter
    print("=== TEST 1: General Search ===")
    results = advanced_search(query)
    for i, res in enumerate(results):
        print(f"\nResult {i+1}:\n{res[:150]}...")

    # 2. Search WITH Filter (Only PDFs)
    # Ye tabhi chalega agar aapne Session 2.5 mein PDF ingest kiya tha
    print("\n\n=== TEST 2: Filtered Search (PDF Only) ===")
    results_pdf = advanced_search(query, filter_dict={"type": "pdf"})
    for i, res in enumerate(results_pdf):
        print(f"\nResult {i+1}:\n{res[:150]}...")
