from langchain_community.tools import DuckDuckGoSearchRun
from typing import Dict, Any
from langchain_core.messages import AIMessage, HumanMessage
import time

search_tool = DuckDuckGoSearchRun()

def web_search_node(state : Dict[str, Any]):
    """
    The Web Researcher Agent.
    Searches the internet for live information.
    """
    print("--- Web Searcher: Searching Internet ---")
    
    question = ""
    messages = state['messages']
    question = state.get("current_task")
    
    # --- FIX: Find Last Human Message (Original Query) ---
    
    if not question:
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                question = msg.content
                break
                
        # Fallback
        if not question:
            question = messages[-1].content if hasattr(messages[-1], 'content') else str(messages[-1])
    
    print(f"--- Web Search Query: '{question}' ---")

    max_retries = 3
    results = None
    last_error = None

    for attempt in range(max_retries):
        try:
            print(f"--- Attempt {attempt + 1}/{max_retries} ---")
            raw_results = search_tool.invoke(question)
            if not raw_results or "No results found" in raw_results:
                raise ValueError("Received empty or invalid results from search tool.")
            results = raw_results
            break 
        except Exception as e:
            print(f"--- Attempt {attempt + 1} Failed: {str(e)} ---")
            last_error = e
            time.sleep(2) 

    # Result processing
    if results:
        print("--- Search Completed ---")
        return {"messages": [AIMessage(content=f"Web Search Result for '{question}':\n\n{results}")]}
    else:
        return {"messages": [AIMessage(content=f"Error: Could not connect to internet after {max_retries} attempts. Reason: {str(last_error)}")]}