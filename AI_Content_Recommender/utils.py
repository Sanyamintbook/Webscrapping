def map_difficulty_to_int(difficulty_str: str) -> int:
    """Map difficulty strings to comparable integer values."""
    mapping = {
        "Beginner": 1,
        "Intermediate": 2,
        "Advanced": 3
    }
    return mapping.get(str(difficulty_str).strip(), 1)

def build_student_semantic_text(profile) -> str:
    """Combine student profile fields into a single semantic string for embedding."""
    interests = " ".join(profile.learning_interests) if profile.learning_interests else ""
    comp_interests = " ".join(profile.competitive_interests) if profile.competitive_interests else ""
    
    text = (f"Grade: {profile.grade} "
            f"Language: {profile.language} "
            f"Level: {profile.level} "
            f"Learning Interests: {interests} "
            f"Competitive Interests: {comp_interests} "
            f"Learning Goal: {profile.learning_goal}")
    return text.strip()
