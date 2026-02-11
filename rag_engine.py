from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def build_vector_store(text_chunks):
    # Check if text_chunks is empty
    if not text_chunks or len(text_chunks) == 0:
        raise ValueError("text_chunks cannot be empty")
    
    # Encode the text chunks
    embeddings = model.encode(text_chunks)
    
    # Convert to float32 numpy array (CRITICAL for FAISS)
    embeddings = np.array(embeddings, dtype=np.float32)
    
    # Ensure it's 2D array
    if embeddings.ndim == 1:
        embeddings = embeddings.reshape(1, -1)
    
    print(f"Embeddings shape: {embeddings.shape}")
    print(f"Embeddings dtype: {embeddings.dtype}")
    
    # Create FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    
    # Ensure embeddings are contiguous float32 (required by FAISS) then add
    embeddings = np.ascontiguousarray(embeddings, dtype=np.float32)
    index.add(embeddings) #ignore

    
    print(f"Index size: {index.ntotal}")  # Should show number of vectors added
    
    return index, embeddings

def retrieve(query, text_chunks, index, k=5):
    q_embedding = model.encode([query])
    q_embedding = np.array(q_embedding, dtype=np.float32)
    
    # Ensure 2D shape
    if q_embedding.ndim == 1:
        q_embedding = q_embedding.reshape(1, -1)
    
    # Make contiguous
    q_embedding = np.ascontiguousarray(q_embedding, dtype=np.float32)
    
    _, indices = index.search(q_embedding, k)
    return [text_chunks[i] for i in indices[0]]

# TEST IT
if __name__ == "__main__":
    texts = ["Hello world", "FAISS vector search", "Python programming"]
    
    try:
        index, emb = build_vector_store(texts)
        results = retrieve("coding", texts, index, k=2)
        print(f"Results: {results}")
    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")