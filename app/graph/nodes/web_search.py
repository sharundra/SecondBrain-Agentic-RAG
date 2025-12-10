from langchain_community.tools import DuckDuckGoSearchRun
from typing import Dict, Any

search_tool = DuckDuckGoSearchRun()

def web_search_node(state : Dict[str, Any]):
    """
    The Web Researcher Agent.
    Searches the internet for live information.
    """
    print("--- Web Searcher: Searching Internet ---")

    question = state['messages'][-1].content
    try:
        results = search_tool.invoke(question)
        print("--- Search Completed ---")

        return {"messages": [f"Web Search Result for '{question}':\n\n{results}"]}
    except Exception as e:
        return {"messages": [f"Error searching web: {str(e)}"]}
