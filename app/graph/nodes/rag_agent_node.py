from typing import Dict, Any
from app.graph.subgraphs.rag_graph import rag_graph
from langchain_core.messages import AIMessage, HumanMessage

def call_rag_agent_node(state : Dict[str, Any]):
    print("--- Handover to RAG Subgraph ---")
    
    # We are intereasted in last HumanMessage because last message could be web server's output also but that is not correct query.
    user_query = ""
    user_query = state.get("current_task")
    if isinstance(user_query, str):
        user_query = user_query
    else:
        user_query = user_query.content
    if not user_query:
        for msg in reversed(state['messages']):
            if isinstance(msg, HumanMessage):
                user_query = msg.content
                break
                
        # Fallback (though impossible)
        if not user_query:
            last_message = state['messages'][-1]
            if isinstance(last_message, str):
                user_query = last_message
            else:
                user_query = last_message.content

    print(f"--- RAG Query Extraction: '{user_query}' ---")

    response = rag_graph.invoke({"question": user_query})

    return {"messages": [AIMessage(content = f"RAG Agent Answer: {response['generated_ans']}")]}

