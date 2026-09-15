import pandas as pd
from typing import List
from models import ContentItem

def load_metadata(file_path: str) -> List[ContentItem]:
    """Loads excel file and formats rows into ContentItem objects with semantic text."""
    df = pd.read_excel(file_path)
    
    # Ensure all NaN values are replaced with empty strings for text processing
    df = df.fillna("")
    
    items = []
    for _, row in df.iterrows():
        # Build semantic text
        semantic_text = (
            f"Module: {row.get('Module', '')} "
            f"Title: {row.get('Title', '')} "
            f"Description: {row.get('Description', '')} "
            f"Subject: {row.get('Subject', '')} "
            f"Topic: {row.get('Topic', '')} "
            f"Subtopic: {row.get('Subtopic', '')} "
            f"Grade: {row.get('Grade', '')} "
            f"Difficulty: {row.get('Difficulty', '')} "
            f"Tags: {row.get('Tags', '')}"
        ).strip()
        
        # Ensure semantic_text has single spaces where there might be multiples
        semantic_text = " ".join(semantic_text.split())
        
        try:
            educational_score = float(row.get("Educational_Score", 0.0))
        except ValueError:
            educational_score = 0.0
            
        item = ContentItem(
            content_id=str(row.get("Content_ID", "")),
            module=str(row.get("Module", "")),
            title=str(row.get("Title", "")),
            description=str(row.get("Description", "")),
            subject=str(row.get("Subject", "")),
            topic=str(row.get("Topic", "")),
            subtopic=str(row.get("Subtopic", "")),
            grade=str(row.get("Grade", "")),
            difficulty=str(row.get("Difficulty", "")),
            language=str(row.get("Language", "")),
            tags=str(row.get("Tags", "")),
            educational_score=educational_score,
            safety=str(row.get("Safety", "")),
            content_type=str(row.get("Content_Type", "")),
            url=str(row.get("URL", "")),
            semantic_text=semantic_text
        )
        items.append(item)
    
    return items
