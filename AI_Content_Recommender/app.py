import streamlit as st
import os
from metadata_loader import load_metadata
from recommendation_engine import recommend, get_faiss_index
from models import StudentProfile

DATA_PATH = "data/content.xlsx"

st.set_page_config(page_title="Student Content Recommender", layout="wide")

# st.cache_data.clear() # Uncomment to clear cache manually if needed
def load_data():
    return load_metadata(DATA_PATH)

def initialize_system():
    items = load_data()
    # Pre-build or load the FAISS index
    if items:
        get_faiss_index(items)
    return items

def main():
    st.title("🎓 Student Content Recommendation System")
    st.write("Personalized content recommendations based on semantic AI.")

    # Load items and ensure index is built
    items = initialize_system()

    # Sidebar Student Profile Form
    st.sidebar.header("📝 Student Profile")
    with st.sidebar.form("student_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=1, max_value=100, value=12)
        
        # Populate grades, languages from data dynamically or hardcoded
        grade_options = sorted(list(set([i.grade for i in items if i.grade]))) if items else ["6", "7", "8"]
        grade = st.selectbox("Grade", grade_options)
        
        lang_options = sorted(list(set([i.language for i in items if i.language]))) if items else ["English"]
        language = st.selectbox("Language", lang_options)
        
        level = st.selectbox("Current Level", ["Beginner", "Intermediate", "Advanced"])
        
        # Dynamically populate Learning Interests and Competitive Interests
        all_subjects = set()
        all_topics = set()
        for i in items:
            if i.subject:
                all_subjects.update([s.strip() for s in str(i.subject).split(',')])
            if i.topic:
                all_topics.update([t.strip() for t in str(i.topic).split(',')])
                
        learning_options = sorted(list(all_subjects)) if all_subjects else ["Math", "Science", "Programming"]
        comp_options = sorted(list(all_topics)) if all_topics else ["Olympiad", "Hackathon"]
        
        # Ensure IIT and NEET are present
        if "IIT JEE Preparation" not in comp_options:
            comp_options.append("IIT JEE Preparation")
        if "NEET Preparation" not in comp_options:
            comp_options.append("NEET Preparation")
            
        learning_interests = st.multiselect("Learning Interests", learning_options)
        competitive_interests = st.multiselect("Competitive Interests", comp_options)
            
        learning_goal = st.text_area("Learning Goal")
        
        submit = st.form_submit_button("Recommend Content")

    if submit:
        if not name:
            st.error("Please enter a name.")
            return
            
        st.success(f"Generating recommendations for {name}...")
        
        profile = StudentProfile(
            name=name,
            age=age,
            grade=grade,
            language=language,
            level=level,
            learning_interests=learning_interests,
            competitive_interests=competitive_interests,
            learning_goal=learning_goal
        )
        
        recommendations = recommend(profile, items, top_k=50)
        
        if not recommendations:
            st.warning("No recommendations found matching your criteria.")
            return
            
        # Group recommendations by module
        modules = ["Course", "News", "Competitive", "Test", "Leisure"]
        grouped_results = {m: [] for m in modules}
        
        for item, score in recommendations:
            norm_score = max(0.0, min(1.0, (score + 1) / 2))
            # Relaxed threshold so Biology matches better
            if norm_score < 0.55:
                continue
                
            mod = item.module
            if mod in grouped_results:
                grouped_results[mod].append((item, norm_score))
            else:
                grouped_results.setdefault("Other", []).append((item, norm_score))

        # Render sections
        for mod, recs in grouped_results.items():
            # Handle pluralization
            heading = f"{mod}s" if mod != "News" else "News"
            st.header(f"Recommended {heading}")
            
            if not recs:
                st.info(f"No highly relevant {heading.lower()} found for your specific interests.")
                st.divider()
                continue
                
            # Using columns for card layout
            cols = st.columns(3)
            for idx, (item, norm_score) in enumerate(recs):
                with cols[idx % 3]:
                    with st.container(border=True):
                        st.subheader(item.title)
                        st.caption(f"{item.subject} | {item.topic}")
                        st.write(item.description)
                        st.write(f"**Difficulty:** {item.difficulty}")
                        st.write(f"**Tags:** {item.tags}")
                        
                        st.progress(norm_score, text=f"Similarity: {norm_score:.0%}")
                        
                        st.link_button("Open Content", item.url if item.url else "#")
            st.divider()

if __name__ == "__main__":
    main()
