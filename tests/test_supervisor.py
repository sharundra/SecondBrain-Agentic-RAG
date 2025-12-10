from app.graph.workflow import main_app
from langchain_core.messages import HumanMessage
import logging

# Want only CRITICAL errors to be displayed, not INFO/WARNING
logging.getLogger("ddgs").setLevel(logging.CRITICAL)
logging.getLogger("httpx").setLevel(logging.CRITICAL)

if __name__ == "__main__":
    # Test 1: RAG Query
    print("\n=== TEST 1: Technical Query (Should go to RAG) ===")
    inputs = {"messages": [HumanMessage(content="How was Aryan Society?")]}
    for event in main_app.stream(inputs):
        for key, value in event.items():
            print(f"Finished: {key}")
            if 'messages' in value:
                print(f"Output: {value['messages'][-1]}")

    print("\n" + "="*50 + "\n")

    # Test 2: Web Query
    print("=== TEST 2: General Query (Should go to Web) ===")
    inputs = {"messages": [HumanMessage(content="Who won the Cricket World Cup 2023?")]}
    for event in main_app.stream(inputs):
        for key, value in event.items():
            print(f"Finished: {key}")
            if 'messages' in value:
                print(f"Output: {value['messages'][-1]}")