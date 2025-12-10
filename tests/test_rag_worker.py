from app.graph.subgraphs.rag_graph import rag_graph

if __name__ == "__main__":
    # Question about something present in the DB (Video or PDF)
    # query = "What are 13 Upanishads?" 
    query = "What is general thoery of relativity?"
    
    print(f"Testing RAG Subgraph with query: {query}")
    
    inputs = {"question": query}
    
    # Run the subgraph
    for output in rag_graph.stream(inputs):
        for key, value in output.items():
            print(f"Finished Node: {key}")
            
    # Final Result
    # Note: After stream we dont get final state directly in the loop,
    # so let's run invoke() to see the final answer clearly for testing.
    final_state = rag_graph.invoke(inputs)
    
    print("\n" + "="*30)
    print("FINAL GENERATION")
    print("="*30)
    print(final_state["generated_ans"])