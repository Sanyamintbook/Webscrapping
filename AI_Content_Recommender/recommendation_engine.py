import os
import faiss
import numpy as np
from typing import List, Tuple
from models import ContentItem, StudentProfile
from utils import map_difficulty_to_int
import embedding_service

INDEX_PATH = "vector_db/content_index.faiss"

def build_faiss_index(items: List[ContentItem]):
    """Generates and saves a FAISS index from the content items."""
    if not items:
        return None
        
    texts = [item.semantic_text for item in items]
    embeddings = embedding_service.generate_embeddings(texts)
    
    # Normalize for cosine similarity via Inner Product
    faiss.normalize_L2(embeddings)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    
    faiss.write_index(index, INDEX_PATH)
    return index

def get_faiss_index(items: List[ContentItem]):
    """Loads the FAISS index if it exists, otherwise builds it."""
    if os.path.exists(INDEX_PATH):
        return faiss.read_index(INDEX_PATH)
    else:
        return build_faiss_index(items)

def llm_commonsense_filter(student_profile: StudentProfile, candidate_tuples: List[Tuple[ContentItem, float]]) -> List[Tuple[ContentItem, float]]:
    import requests
    import json
    import os
    
    if not candidate_tuples:
        return []
        
    OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://10.80.100.214:11434")
    OLLAMA_CHAT_MODEL = os.environ.get("OLLAMA_CHAT_MODEL", "qwen3:8b")
    
    # Check if student provided explicit interests. If not, just return FAISS results.
    if not student_profile.learning_interests and not student_profile.competitive_interests:
        return candidate_tuples
        
    candidates_dict = {i: tup for i, tup in enumerate(candidate_tuples)}
    candidates_text = "\n".join([f"ID {i}: {tup[0].title} (Subject: {tup[0].subject}, Tags: {tup[0].tags})" for i, tup in candidates_dict.items()])
    
    prompt = f"""You are an AI Content Recommender. 
A student has the following profile:
Grade: {student_profile.grade}
Learning Interests: {student_profile.learning_interests}
Competitive Interests: {student_profile.competitive_interests}
Learning Goal: {student_profile.learning_goal}

Here are the candidate content items:
{candidates_text}

Select ONLY the IDs of the items that are highly relevant to this student's specific interests. Use common sense (e.g. do not recommend Biology for a Mathematics student). Think wildly but logically. 
Respond ONLY with a valid JSON array of integers representing the selected IDs. Do not include any other text or markdown formatting. Example: [0, 2, 5]"""

    try:
        response = requests.post(f"{OLLAMA_BASE_URL}/api/generate", json={
            "model": OLLAMA_CHAT_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.0
            }
        }, timeout=120)
        response.raise_for_status()
        result_text = response.json().get("response", "[]").strip()
        
        selected_ids = json.loads(result_text)
        if not isinstance(selected_ids, list):
            selected_ids = []
            
        filtered = [candidates_dict[i] for i in selected_ids if i in candidates_dict]
        return filtered
    except Exception as e:
        print("LLM Filter Error:", e)
        return [] # Safe fallback: return nothing if the LLM crashes to prevent massive misalignment

def recommend(student_profile: StudentProfile, items: List[ContentItem], top_k: int = 50) -> List[Tuple[ContentItem, float]]:
    """Retrieves top K semantic matches and applies business rules."""
    from utils import build_student_semantic_text
    
    if not items:
        return []
    
    # 1. Build semantic embedding for the student
    query_text = build_student_semantic_text(student_profile)
    query_embedding = embedding_service.generate_embedding(query_text)
    
    # Normalize query for cosine similarity
    query_embedding = np.expand_dims(query_embedding, axis=0)
    faiss.normalize_L2(query_embedding)
    
    # 2. Get the index
    index = get_faiss_index(items)
    
    # 3. Search FAISS
    k_search = min(len(items), top_k * 5)
    similarities, indices = index.search(query_embedding, k_search)
    
    results = []
    student_diff_val = map_difficulty_to_int(student_profile.level)
    
    for i in range(len(indices[0])):
        idx = indices[0][i]
        sim_score = similarities[0][i]
        
        if idx < 0 or idx >= len(items):
            continue
            
        item = items[idx]
        
        # Difficulty must not exceed student level
        item_diff_val = map_difficulty_to_int(item.difficulty)
        if item_diff_val > student_diff_val:
            continue
            
        # Safety must equal Safe
        if item.safety != "Safe":
            continue
            
        results.append((item, float(sim_score)))
        if len(results) >= top_k:
            break
            
    # Apply Qwen3 8B dynamic LLM filtering
    results = llm_commonsense_filter(student_profile, results)
    
    return results
