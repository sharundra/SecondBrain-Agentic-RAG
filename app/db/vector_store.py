import os
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore

load_dotenv()

def get_vector_store():
    """
    Connects to Pinecone and returns a LangChain VectorStore object.
    This is where we will store and search for knowledge.
    """

    pinecone_api_key = os.getenv('PINECONE_API_KEY')
    pinecone_index_name = os.getenv('PINECONE_INDEX_NAME')

    if not pinecone_api_key or not pinecone_index_name:
        raise ValueError("Pinecone credentials missing in .env")


    pc = Pinecone(api_key = pinecone_api_key)

    existing_indexes = [index.name for index in pc.list_indexes()]

    if pinecone_index_name not in existing_indexes:
        print(f"--- Creating new Pinecone Index: {pinecone_index_name} ---")
        pc.create_index(
            name=pinecone_index_name,
            dimension=1536, 
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )

    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vector_store = PineconeVectorStore(index_name = pinecone_index_name, embedding = embeddings)
    print("--- Vector Store (Library) Connected Successfully ---")
    return vector_store