from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from langchain_core.messages import HumanMessage
# from app.graph.workflow import main_app
from contextlib import asynccontextmanager
from app.graph.workflow import main_graph
from app.db.checkpointer import get_checkpointer

graph_app = None

# setup required for AsyncPostgresSaver -- AsyncPostgresSaver + lifespan + thread_id

# T = 0, we gave command, "uvicorn app.api.server:app --reload" -- UVcorn server process starts
# T = 1, UVcorn asks python to bring FAST API app object and it returns app to UVcorn by scanning this entire script
# t = 2, UVcorn starts event loop and asks it to start lifspan as it is defined here
# At yield, lifespan pauses, and control goes back to event loop which starts taking requests
# Lifespan is the time duration between event loop starting and starting to take requests where it/process connects to AsyncPostGres database.

# Lifespan Manager (Startup/Shutdown logic)
@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    global graph_app
    print("--- Starting SecondBrain API & Connecting to DB ---")

    # Connect to Postgres
    checkpointer = await get_checkpointer()

    # Compile Graph WITH Memory
    graph_app = main_graph.compile(checkpointer)

    # lifespan will pause now by yield command so that server can take requests
    yield

    #Server has stopped taking requests and now lifespan is shutting down.
    print("--- Shutting down ---")


# defining input schema
class ChatRequest(BaseModel):
    message : str
    thread_id : str = 'default_user'

fastapi_app = FastAPI(
    title = 'SecondBrain-Agentic-RAG API',
    version = '1.0',
    lifespan = lifespan,
    description = "An Autonomous RAG Agent API"
)

# Define the chat Endpoint through POST(@fastapi_app.post) HTTP method
@fastapi_app.post("/chat")
async def chat_endpoint(request : ChatRequest):
    """
    Main endpoint to talk to the Supervisor Agent.
    """
    print(f"--- API Request: {request.message} (Thread: {request.thread_id}) ---")
    try:
        inputs = {'messages': [HumanMessage(content = request.message)]}
        #config with thread_id is mandatory for memory
        config = {'configurable' : {'thread_id' : request.thread_id}}

        final_response = ""
        
        async for event in graph_app.astream(inputs, config = config):
            for key, value in event.items():
                pass
        
        #get final state from memory
        snapshot = await graph_app.aget_state(config)
        last_msg = snapshot.values['messages'][-1]
        final_response = last_msg.content if hasattr(last_msg, 'content') else str(last_msg)

        return {'response': final_response}


    except Exception as e:
        print(f"API Error: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
    
@fastapi_app.get("/")
def home():
    return {"message": "Welcome to SecondBrain AI API. Go to /docs for Swagger UI."}

@fastapi_app.get("/health")
def health_check():
    return {"status": "active", "model": "SecondBrain v1"}