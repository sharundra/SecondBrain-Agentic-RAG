import asyncio
from app.db.checkpointer import get_checkpointer
from app.db.vector_store import get_vector_store

async def main():
    print("Testing Infrastructure...")
    
    # Test 1: Postgres
    try:
        cp = await get_checkpointer()
    except Exception as e:
        print(f"❌ Postgres Error: {e}")

    # Test 2: Pinecone
    try:
        vs = get_vector_store()
    except Exception as e:
        print(f"❌ Pinecone Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())