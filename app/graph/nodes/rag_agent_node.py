from typing import Dict, Any
from app.graph.subgraphs.rag_graph import rag_graph

def call_rag_agent_node(state : Dict[str, Any]):
    last_message = state['messages'][-1].content
    
    response = rag_graph.invoke({'question': last_message})
    
    return {"messages": [f"RAG Agent Answer: {response['generated_ans']}"]}