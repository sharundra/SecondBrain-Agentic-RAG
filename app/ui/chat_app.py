import sys
import os

# Current file's parent's parent directory (Root) got added to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import chainlit as cl
from langchain_core.messages import HumanMessage
from app.graph.workflow import main_app as graph_app # Direct Graph Import

@cl.on_chat_start
async def start():
    """
    Called when the user opens the chat.
    """
    # Session ID set karte hain (Postgres Memory ke liye)
    cl.user_session.set("thread_id", "user_session_1")
    
    await cl.Message(
        content="👋 Welcome to **SecondBrain AI**. I am your Autonomous Research Assistant.\n\nAsk me anything like:\n- *What is RAG?*\n- *Search web for Tesla stock price.*",
        author="SecondBrain"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """
    Called when the user sends a message.
    """
    # 1. Get Thread ID
    thread_id = cl.user_session.get("thread_id")
    config = {"configurable": {"thread_id": thread_id}}
    
    # 2. Prepare Input
    inputs = {"messages": [HumanMessage(content=message.content)]}
    
    # 3. Stream the Graph (The "Wow" Factor)
    # Hum final answer ka wait nahi karenge, hum har step dikhayenge
    
    msg = cl.Message(content="") # Empty message jo dheere dheere bharega
    
    async for event in graph_app.astream(inputs, config=config):
        
        for node, values in event.items():
            
            # Case A: Supervisor Decision
            if node == "supervisor":
                decision = values['next']
                # UI mein chota notification dikhao
                await cl.Message(
                    content=f"👔 **Supervisor:** Routing task to `{decision}`...",
                    parent_id=message.id # Ye message user ke message ke niche aayega
                ).send()
            
            # Case B: Workers (Web or RAG)
            elif node in ["web_searcher", "rag_agent"]:
                # Worker ka output nikalo
                last_msg = values['messages'][-1]
                
                # Agar content hai to stream karo
                if isinstance(last_msg, str):
                    content = last_msg
                else:
                    content = last_msg.content
                
                # Final answer update karo
                await msg.stream_token(content)

    # 4. Send Final Message
    await msg.send()