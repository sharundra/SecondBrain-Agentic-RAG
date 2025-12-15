from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
import os
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv('SUPABASE_DB_URL')

async def get_checkpointer():
    """
    Creates and returns PostGres Checkpointer for LangGraph.
    This allows the agent to remember conversations across restarts.
    """
    if not DB_URI:
        raise ValueError("SUPABASE_DB_URL is not set in .env file")
    
    connection_kwargs = {
        "autocommit": True,
        "prepare_threshold" : 0,
        "keepalives": 1,
        "keepalives_idle": 5,
        "keepalives_interval": 2,
        "keepalives_count": 5
    }

    pool = AsyncConnectionPool(conninfo = DB_URI, max_size = 20, kwargs = connection_kwargs)

    checkpointer = AsyncPostgresSaver(pool)

    await checkpointer.setup()
    print("--- 📝 Database (Diary) Connected Successfully ---")
    return checkpointer