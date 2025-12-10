from pydantic import BaseModel, Field
from typing import Literal, Dict, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage

class RouteDecision(BaseModel):
    """Decide the next worker based on the user question."""

    next : Literal['web_searcher', 'rag_agent', 'FINISH'] = Field(
        description="Choose 'rag_agent' for technical/saved knowledge. Choose 'web_searcher' for current events/general info. Choose 'FINISH' if it's just a greeting."
    )

llm = ChatOpenAI()
structured_llm = llm.with_structured_output(RouteDecision)

def supervisor_node(state : Dict[str, Any]):
    """
    Decides which route to take.
    """
    print("--- Supervisor: Routing the task ---")
    messages = state['messages']

    system_prompt = SystemMessage(content="""
    You are the Supervisor of 'SecondBrain AI'.
    You have two workers:
    1. 'rag_agent': Has access to saved videos and PDFs. Use this for technical concepts, tutorials, or specific documents.
    2. 'web_searcher': Has access to the internet. Use this for news, weather, or current events.
    
    Decide which worker should act next. If the user just says 'Hi' or 'Thanks', choose 'FINISH'.
    """)

    decision = structured_llm.invoke([system_prompt] + messages)
    print(f"--- Decision: {decision.next} ---")

    return {'next' : decision.next}