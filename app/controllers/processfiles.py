import pinecone
import os
from dotenv import load_dotenv
from fastapi import UploadFile, File, HTTPException
from app.utility.process import save_file, process_pdf
from app.models.file import files_collection
from uuid import uuid4
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_API_KEY)
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)
index = pinecone.Index("resume-index")

async def upload_and_process(file: UploadFile = File(...)):
    upload_dir = "uploads"
    file_path = save_file(file, upload_dir)
    file_id = str(uuid4())
    
    try:
        chunks = process_pdf(file_path)
        
        document = {
            "file_id": file_id,
            "content": chunks
        }
        result = await files_collection.replace_one(
            {"file_id": file_id},  
            document,
            upsert=True
        )
        
        if result.upserted_id is None and result.modified_count == 0:
            raise HTTPException(status_code=500, detail="Failed to store the document in MongoDB")
        
        vectors = []
        for i, chunk in enumerate(chunks):
            vector = embeddings.embed_query(chunk)
            vectors.append((f"{file_id}_{i}", vector))
        
        index.upsert(vectors=vectors)
        
        if not vectors:
            raise HTTPException(status_code=500, detail="Failed to upsert embeddings to Pinecone")
        
        return {"message": "Upload, storage, and embedding successful", "file_id": file_id}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

async def get_chunks():
    try:
        # Retrieve the single document from the collection
        document = await files_collection.find_one() 
        if not document:
            raise HTTPException(status_code=404, detail="No document found")
        chunks = document.get("content", [])
        return {"chunks": chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
