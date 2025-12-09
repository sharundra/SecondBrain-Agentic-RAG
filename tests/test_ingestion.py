from app.graph.ingestion import ingest_youtube_video, ingest_pdf
import os

# Koi bhi educational video ka link dalo (jisme subtitles hon)
VIDEO_URL = "https://www.youtube.com/watch?v=NYSWn1ipbgg" # Example: LangChain Video

if __name__ == "__main__":
    # result = ingest_youtube_video(VIDEO_URL)
    # print(result)

    # 2. PDF Test
    PDF_PATH = "Religion of India in 6th century BC (Part 1).pdf" 

    if __name__ == "__main__":
        if os.path.exists(PDF_PATH):
            result = ingest_pdf(PDF_PATH)
            print(result)
        else:
            print(f"Error: {PDF_PATH} not found. Please add a PDF file.")