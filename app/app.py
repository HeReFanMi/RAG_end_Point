import asyncio
import numpy as np
import torch
from transformers import BertTokenizer, BertModel
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import ARRAY  # Import ARRAY
from scipy.spatial.distance import cdist
from asgiref.wsgi import WsgiToAsgi
import requests
from sentence_transformers import SentenceTransformer  # Import SentenceTransformer for embeddings

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+asyncpg://postgres:mysecretpassword@postgres-container:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Base = declarative_base()

class ChunkEmbedding(Base):
    __tablename__ = 'chunk_embeddings'
    id = Column(Integer, primary_key=True)
    chunk = Column(String)
    embedding = Column(ARRAY(Float))  

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
embedding_model = embedding_model.to(device)  

engine = create_async_engine('postgresql+asyncpg://postgres:mysecretpassword@postgres-container:5432/postgres', echo=True)

def compute_embedding(text):
    embedding = embedding_model.encode(text, convert_to_tensor=True)  
    return embedding.cpu().numpy()  
async def fetch_all_embeddings():
    async with AsyncSession(engine) as session:
        query = select(ChunkEmbedding)
        result = await session.execute(query)
        rows = result.scalars().all()
        
        if rows:
            print(f"Fetched {len(rows)} rows from the database.") 
            print(f"Sample chunk: {rows[0].chunk}")  
            print(f"Sample embedding: {rows[0].embedding[:5]}") 
    return rows

async def find_similar_chunks(prompt, top_n=5):
    prompt_embedding = compute_embedding(prompt)
    
    rows = await fetch_all_embeddings()
    
    chunks = [row.chunk for row in rows]
    embeddings = np.array([row.embedding for row in rows])
    
    distances = cdist([prompt_embedding], embeddings, metric="cosine")[0]
    
    similarity_indices = distances.argsort()[:top_n] 
    
    similar_chunks = [(chunks[i], 1 - distances[i]) for i in similarity_indices] 
    return similar_chunks

@app.route('/')
def home():
    return "App is running 🚀"

@app.route('/find_similar_chunks', methods=['POST'])
async def get_similar_chunks():
    data = request.get_json()
    prompt = data.get('prompt')
    top_n = data.get('top_n', 5) 

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    similar_chunks = await find_similar_chunks(prompt, top_n)
    
    chunks = [chunk for chunk, _ in similar_chunks]


    payload = {
        "chunks": chunks,
        "question": prompt
    }

    try:
        response = requests.post("http://127.0.0.1:5002/predict", json=payload)
        if response.status_code == 200:
            print(f"Successfully sent to /predict API with status 200.")
        else:
            print(f"Failed to send to /predict API. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error while sending to /predict API: {e}")
    
    return jsonify({"status": "200 OK"}), 200

if __name__ == '__main__':
    from asgiref.wsgi import WsgiToAsgi
    app_asgi = WsgiToAsgi(app)
    import uvicorn
    print("App is running on http://0.0.0.0:5000 🚀")  
    uvicorn.run(app_asgi, host="0.0.0.0", port=5000)
