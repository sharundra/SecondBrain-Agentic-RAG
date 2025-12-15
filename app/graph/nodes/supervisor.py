from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

class PlanningOutput(BaseModel):
    sub_queries : List[str] = Field("List of distinct search queries.")
class RouteDecision(BaseModel):
    """Decide the next worker based on the user question."""

    next : Literal['web_searcher', 'rag_agent', 'FINISH'] = Field(
        description="The worker to handle the CURRENT task."
    )

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
structured_llm = llm.with_structured_output(RouteDecision)

def supervisor_node(state : Dict[str, Any]):
    """
    Decides which route to take.
    """
    print("--- Supervisor: Managing task ---")
    messages = state['messages']
    current_sub_queries = state.get('sub_queries', [])

    if state.get('original_query'):
        original_query = state['original_query']
    else:
        original_query = ""


    last_message = messages[-1]
    if not current_sub_queries and isinstance(last_message, HumanMessage):
        print("--- Planning Phase: Breaking down query ---")

        original_query = last_message.content
        planner_prompt = SystemMessage(content="""
        You are the Planner for 'SecondBrain AI'.
        Break down the user's request into distinct, independent search queries.
        
        Example: "Weather in Delhi and Upanishads info"
        Output: ["Current weather in Delhi", "What are the 13 Upanishads?"]
        
        If it's a simple greeting ("Hi"), output: [] (Empty list).
        """)

        planner_llm = llm.with_structured_output(PlanningOutput)
        plan = planner_llm.invoke([planner_prompt] + messages)
        current_sub_queries = plan.sub_queries
        print(f"--- Plan Created: {current_sub_queries} ---")

        if not current_sub_queries:
            print("--- 🗣️ Conversational Response ---")
            response = llm.invoke(messages)
            return {"next": "FINISH", "messages": [response], "sub_queries": [], "original_query": original_query}
        
    if current_sub_queries:
        current_task = current_sub_queries[0]
        remaining_tasks = current_sub_queries[1:]
        print(f"--- Processing Task: '{current_task}' ---")
        router_prompt = SystemMessage(content="""
        You are the Router. Pick the best worker for the CURRENT TASK:
        1. 'rag_agent': Indian Ancient History of religions and philosophy (Upanishads, Vedas) OR AI (LangGraph) OR question about some fictional scifi story.
        2. 'web_searcher': Movies, Weather, News, current affairs, Everything else.
        
        Task: {task}
        """)

        router_llm = llm.with_structured_output(RouteDecision)
        decision = router_llm.invoke([router_prompt, HumanMessage(content=current_task)])
        print(f"--- Assigned to: {decision.next} ---")
        return {
            "next": decision.next, 
            "current_task": current_task,
            "sub_queries": remaining_tasks,
            "original_query": original_query
                }

    print("--- All tasks done. Synthesizing Final Answer. ---")

    final_prompt = SystemMessage(content=f"""
    You are the 'Research Compiler' for SecondBrain AI.
    
    YOUR MISSION: 
    Construct a final answer based ONLY on the conversation history below.
    
    CRITICAL INSTRUCTION:
    The user's ORIGINAL QUERY was: "{original_query}"
    
    1. Break down the Original Query into its sub-parts (e.g., Part A and Part B).
    2. Scan the conversation history specifically for the answer to Part A (likely found earlier in the chat).
    3. Scan the conversation history specifically for the answer to Part B (likely found later in the chat).
    4. You MUST include answers for BOTH parts. Do not ignore the first part just because it is older.
    
    FORMAT:
    - Start with a direct answer.
    - Use bullet points if there were multiple questions.
    - If one part was "NOT FOUND" by workers, explicitly state that.
    
    WARNING:
    - Do not hallucinate. Use only the info provided by 'web_searcher' and 'rag_agent'.
    - If the history contains a "Web Search Result" for Part A, USE IT. Do not skip it.
    """)
    
    response = llm.invoke([final_prompt] + messages)
    return {"next": "FINISH", "messages": [response], "current_task": None, "sub_queries": [], "original_query": None }