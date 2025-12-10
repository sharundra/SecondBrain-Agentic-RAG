from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated,List
from langchain_core.messages import BaseMessage
import operator
from app.graph.nodes.rag_agent_node import call_rag_agent_node
from app.graph.nodes.supervisor import supervisor_node
from app.graph.nodes.web_search import web_search_node

class MainState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    next : str

main_graph = StateGraph(MainState)

main_graph.add_node('supervisor', supervisor_node)
main_graph.add_node('rag_agent', call_rag_agent_node)
main_graph.add_node('web_searcher', web_search_node)



def route_logic(state):
    return state['next']

main_graph.set_entry_point('supervisor')
main_graph.add_conditional_edges('supervisor', route_logic, {'web_searcher': 'web_searcher', 'rag_agent': 'rag_agent', 'FINISH':END})
main_graph.add_edge('rag_agent', END)
main_graph.add_edge('web_searcher', END)

main_app = main_graph.compile()



