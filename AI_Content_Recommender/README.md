# AI-Powered Student Content Recommendation System

This is a Streamlit application designed to recommend educational and leisure content to students based on semantic embeddings and specific business rules. It uses FAISS for rapid semantic similarity search and Sentence Transformers for embedding generation.

## Setup Instructions

1. Ensure you have Python 3 installed.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Make sure your `data/content.xlsx` is populated correctly.
4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Features
- Generates semantic text embeddings for each content item and student profile.
- Filters recommendations using strict business rules (matching grade, language, ensuring safety, and limiting maximum difficulty).
- Groups recommendations smoothly into categories: Courses, News, Competitive, Tests, and Leisure.
