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

# Fix for Windows event loop issue
if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Flask app setup
app = Flask(__name__)

# Database URI setup (make sure your PostgreSQL is running)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define database table structure
Base = declarative_base()

class ChunkEmbedding(Base):
    __tablename__ = 'chunk_embeddings'
    id = Column(Integer, primary_key=True)
    chunk = Column(String)
    embedding = Column(ARRAY(Float))  # Using ARRAY from postgresql dialect

# Initialize model and tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Create the async engine with the correct connection string
engine = create_async_engine('postgresql+asyncpg://postgres:mysecretpassword@localhost:5432/postgres', echo=True)

# Function to compute embedding for the prompt
def compute_embedding(text):
    inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
        cls_embedding = outputs.last_hidden_state[:, 0, :].squeeze().numpy()
    return cls_embedding

# Function to fetch all chunks and embeddings from the database
async def fetch_all_embeddings():
    async with AsyncSession(engine) as session:
        query = select(ChunkEmbedding)
        result = await session.execute(query)
        rows = result.scalars().all()
        
        if rows:
            print(f"Fetched {len(rows)} rows from the database.")  # Debug print
            print(f"Sample chunk: {rows[0].chunk}")  # Print the first chunk for verification
            print(f"Sample embedding: {rows[0].embedding[:5]}")  # Print first 5 values of the first embedding for verification
    return rows

# Function to find the most similar chunks to the prompt
async def find_similar_chunks(prompt, top_n=5):
    # Compute the embedding for the prompt
    prompt_embedding = compute_embedding(prompt)
    
    # Fetch all embeddings from the database
    rows = await fetch_all_embeddings()
    
    # Extract chunks and their embeddings
    chunks = [row.chunk for row in rows]
    embeddings = np.array([row.embedding for row in rows])
    
    # Compute cosine similarity between the prompt and all embeddings in the database
    distances = cdist([prompt_embedding], embeddings, metric="cosine")[0]
    
    # Get indices of the top-N most similar chunks (smallest distance)
    similarity_indices = distances.argsort()[:top_n]  # Get indices of top-N similar chunks
    
    # Return the most similar chunks and their similarity scores
    similar_chunks = [(chunks[i], 1 - distances[i]) for i in similarity_indices]  # Convert to similarity scores
    return similar_chunks

# Flask route for finding similar chunks
@app.route('/find_similar_chunks', methods=['POST'])
async def get_similar_chunks():
    # Get the JSON data from the request
    data = request.get_json()
    prompt = data.get('prompt')
    top_n = data.get('top_n', 5)  # Default to 5 if top_n is not provided

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    # Find similar chunks using the async function
    similar_chunks = await find_similar_chunks(prompt, top_n)
    
    # Prepare the response in a suitable format
    return jsonify({
        "similar_chunks": [{"chunk": chunk, "similarity": round(similarity, 4)} for chunk, similarity in similar_chunks]
    })

# Start the Flask app using Uvicorn (for async support)
if __name__ == '__main__':
    from asgiref.wsgi import WsgiToAsgi
    # Wrap Flask app to ASGI
    app_asgi = WsgiToAsgi(app)
    import uvicorn
    uvicorn.run(app_asgi, host="0.0.0.0", port=5000)
