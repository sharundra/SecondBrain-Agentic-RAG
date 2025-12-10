from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from youtube_transcript_api import YouTubeTranscriptApi
from app.db.vector_store import get_vector_store
from langchain_community.document_loaders import PyMuPDFLoader

text_splitter = RecursiveCharacterTextSplitter(
                                                            chunk_size = 500,
                                                            chunk_overlap = 200
                                                        )


def ingest_youtube_video(video_url : str):
    """
    Downloads transcript, chunks it, and saves to Pinecone.
    """
    print(f"--- Ingesting Video: {video_url} ---")
    
    try:
        
        if 'v=' in video_url:
            video_id = video_url.split('v=')[1].split('&')[0]
        elif 'youtu.be' in video_url:
            video_id = video_url.split('/')[-1]
        else:
            return "Error: Invalid URL"
        
        transcript_list_of_obj = YouTubeTranscriptApi().fetch(video_id, languages=['en', 'en-US', 'en-GB', 'en-IN'])

        full_text_string =  " ".join(text_obj.text for text_obj in transcript_list_of_obj)

        full_doc_string = Document(page_content = full_text_string, metadata = {'source': video_url, 'type': 'youtube'})

        chunks = text_splitter.split_documents([full_doc_string])
        print(f"--- Split into {len(chunks)} Chunks ---")

        vector_store = get_vector_store()
        vector_store.add_documents(chunks)
        print("--- Saved to Pinecone Successfully! ---")
        return "Success"

    except Exception as e:
        print(f"Error: {e}")
        return f"Failed: {str(e)}"
    
def ingest_pdf(file_path : str):
    """
    Reads a PDF file, chunks it, and saves to Pinecone.
    """
    try:
        print(f"--- Ingesting PDF: {file_path} ---")
        loader_obj = PyMuPDFLoader(file_path)
        docs = loader_obj.load()

        for doc in docs:
            doc.metadata['source'] = file_path
            doc.metadata['type'] = 'pdf'
        
        chunks = text_splitter.split_documents(docs)
        print(f"--- Split into {len(chunks)} Chunks ---")

        vector_store = get_vector_store()
        vector_store.add_documents(docs)
        print("--- Saved to Pinecone Successfully! ---")
        return "Success"
    except Exception as e:
        print(f"Error: {e}")
        return f"Failed: {str(e)}"



