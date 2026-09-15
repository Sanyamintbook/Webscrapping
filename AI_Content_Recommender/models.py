from dataclasses import dataclass
from typing import List

@dataclass
class ContentItem:
    content_id: str
    module: str
    title: str
    description: str
    subject: str
    topic: str
    subtopic: str
    grade: str
    difficulty: str
    language: str
    tags: str
    educational_score: float
    safety: str
    content_type: str
    url: str
    semantic_text: str = ""

@dataclass
class StudentProfile:
    name: str
    age: int
    grade: str
    language: str
    level: str
    learning_interests: List[str]
    competitive_interests: List[str]
    learning_goal: str
