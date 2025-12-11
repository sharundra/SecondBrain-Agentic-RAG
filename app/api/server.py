from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage
from app.graph.workflow import main_app

class ChatRequest(BaseModel):
    message : str
    thread_id : str = 'default_user'

app = FastAPI(
    title = 'SecondBrain-Agentic-RAG API',
    version = '1.0',
    description = "An Autonomous RAG Agent API"
)

# Define the chat Endpoint through POST(@app.post) HTTP method
@app.post("/chat")
async def chat_endpoint(request : ChatRequest):
    """
    Main endpoint to talk to the Supervisor Agent.
    """
    print(f"--- API Request: {request.message} (Thread: {request.thread_id}) ---")
    try:
        inputs = {'messages': [HumanMessage(content = request.message)]}
        result = await main_app.ainvoke(inputs)
        final_msg = result['messages'][-1]

        return {"response": final_msg}

    except Exception as e:
        print(f"API Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/")
def home():
    return {"message": "Welcome to SecondBrain AI API. Go to /docs for Swagger UI."}

@app.get("/health")
def health_check():
    return {"status": "active", "model": "SecondBrain v1"}