from typing import TypedDict
from app.graph.advanced_retrieval import advanced_search
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END

class RAGState(TypedDict):
    question: str
    retrieved_docs : str
    generated_ans : str 

def retrieve_node(state : RAGState):
    """
    Uses the Advanced RAG (Vector + Re-ranker) to find data.
    """
    print(f"--- RAG Worker: Retrieving data for '{state['question']}' ---")
    question = state['question']
    retrieved_docs = advanced_search(question)
    return {'retrieved_docs' : retrieved_docs}

def generation_node(state:RAGState):
    """
    Synthesizes an answer using the retrieved documents.
    """
    print("--- RAG Worker: Generating Answer ---")
    question = state['question']
    context_list = state['retrieved_docs']
    context = "/n/n".join(context_list)

    prompt  = ChatPromptTemplate.from_template(
        """You are a helpful assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Keep the answer concise.

        Question: {question} 

        Context: 
        {context} 

        Answer:"""
    )
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    chain = prompt | llm | StrOutputParser()

    result = chain.invoke({'question' : question, 'context' : context})

    return {'generated_ans' : result}

rag_graph_builder = StateGraph(RAGState)

rag_graph_builder.add_node("retriever", retrieve_node)
rag_graph_builder.add_node("generator", generation_node)

rag_graph_builder.set_entry_point("retriever")
rag_graph_builder.add_edge("retriever", "generator")
rag_graph_builder.add_edge("generator", END)

rag_graph = rag_graph_builder.compile()

