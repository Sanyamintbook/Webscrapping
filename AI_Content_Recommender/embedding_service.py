from sentence_transformers import SentenceTransformer
import streamlit as st
import numpy as np

import requests
import os

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://10.80.100.214:11434")
OLLAMA_EMBEDDING_MODEL = os.environ.get("OLLAMA_EMBEDDING_MODEL", "mxbai-embed-large:latest")

def get_embedding_from_ollama(text: str) -> np.ndarray:
    url = f"{OLLAMA_BASE_URL}/api/embeddings"
    payload = {
        "model": OLLAMA_EMBEDDING_MODEL,
        "prompt": text
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return np.array(response.json()["embedding"], dtype='float32')

def generate_embeddings(texts: list) -> np.ndarray:
    """Generate embeddings for a list of texts using Ollama in parallel."""
    import concurrent.futures
    embeddings = [None] * len(texts)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_index = {executor.submit(get_embedding_from_ollama, text): i for i, text in enumerate(texts)}
        for future in concurrent.futures.as_completed(future_to_index):
            i = future_to_index[future]
            try:
                embeddings[i] = future.result()
            except Exception as exc:
                print(f"Embedding generated an exception: {exc}")
                # Fallback to a zero vector if one fails
                embeddings[i] = np.zeros(1024, dtype='float32')
                
    return np.array(embeddings)

def generate_embedding(text: str) -> np.ndarray:
    """Generate a single embedding using Ollama."""
    query = f"Represent this sentence for searching relevant passages: {text}"
    return get_embedding_from_ollama(query)
