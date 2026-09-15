import pandas as pd
import random

# Load the existing data
file_path = r'c:\Users\Sanyami Jain\Documents\Webscrapping\AI_Content_Recommender\data\content.xlsx'
df = pd.read_excel(file_path)

# New records to add
new_records = [
    {
        'Content_ID': 'BOOK_001',
        'Module': 'Study Material',
        'Title': 'ncert-books-for-class-11-maths',
        'Description': 'Study Material for IIT JEE Mathematics',
        'Subject': 'Mathematics',
        'Topic': 'IIT JEE Preparation',
        'Subtopic': 'Class 11 Maths',
        'Grade': 11,
        'Difficulty': 'Hard',
        'Language': 'English',
        'Tags': 'IIT, JEE, Mathematics, Class 11, NCERT',
        'Educational_Score': 9.5,
        'Safety': 'Safe',
        'Content_Type': 'Book',
        'URL': r'c:\Users\Sanyami Jain\Documents\Webscrapping\book\ncert-books-for-class-11-maths.pdf'
    },
    {
        'Content_ID': 'BOOK_002',
        'Module': 'Study Material',
        'Title': 'NCERT-Class-11-Biology',
        'Description': 'Study Material for NEET Biology',
        'Subject': 'Biology',
        'Topic': 'NEET Preparation',
        'Subtopic': 'Class 11 Biology',
        'Grade': 11,
        'Difficulty': 'Hard',
        'Language': 'English',
        'Tags': 'NEET, Biology, Class 11, NCERT',
        'Educational_Score': 9.5,
        'Safety': 'Safe',
        'Content_Type': 'Book',
        'URL': r'c:\Users\Sanyami Jain\Documents\Webscrapping\book\NCERT-Class-11-Biology.pdf'
    },
    {
        'Content_ID': 'NEWS_002',
        'Module': 'News',
        'Title': 'Times of India Homepage',
        'Description': 'News Portal - Times of India Homepage',
        'Subject': 'General Knowledge',
        'Topic': 'Current Affairs',
        'Subtopic': 'General News',
        'Grade': 10,
        'Difficulty': 'Medium',
        'Language': 'English',
        'Tags': 'News, Current Affairs, India',
        'Educational_Score': 7.0,
        'Safety': 'Safe',
        'Content_Type': 'News',
        'URL': 'https://timesofindia.indiatimes.com/'
    },
    {
        'Content_ID': 'NEWS_003',
        'Module': 'News',
        'Title': 'IIT Kanpur hosts meet on urban healthcare challenges',
        'Description': 'IIT Kanpur hosts meet on urban healthcare challenges',
        'Subject': 'Healthcare',
        'Topic': 'Urban Healthcare',
        'Subtopic': 'IIT Kanpur',
        'Grade': 12,
        'Difficulty': 'Medium',
        'Language': 'English',
        'Tags': 'Healthcare, IIT, Kanpur, Urban Challenges',
        'Educational_Score': 8.0,
        'Safety': 'Safe',
        'Content_Type': 'News',
        'URL': 'https://timesofindia.indiatimes.com/city/kanpur/iit-kanpur-hosts-meet-on-urban-healthcare-challenges/articleshow/132318837.cms'
    },
    {
        'Content_ID': 'NEWS_004',
        'Module': 'News',
        'Title': 'NEET UG 2026 result expected release updates',
        'Description': 'NEET UG 2026 result expected release updates',
        'Subject': 'Education',
        'Topic': 'Medical Exams',
        'Subtopic': 'NEET Results',
        'Grade': 12,
        'Difficulty': 'Medium',
        'Language': 'English',
        'Tags': 'NEET, Exams, Medical, Results',
        'Educational_Score': 8.5,
        'Safety': 'Safe',
        'Content_Type': 'News',
        'URL': 'https://timesofindia.indiatimes.com/education/news/neet-ug-2026-result-expected-to-be-released-soon-at-neet-nta-nic-in-heres-all-aspirants-need-to-know-before-results-are-announced/articleshow/132326767.cms'
    },
    {
        'Content_ID': 'NEWS_005',
        'Module': 'News',
        'Title': 'LeT, IS operatives among 34 killed in Khuzdar attack: BLA',
        'Description': 'LeT, IS operatives among 34 killed in Khuzdar attack: BLA',
        'Subject': 'World Politics',
        'Topic': 'International Security',
        'Subtopic': 'Terrorism',
        'Grade': 12,
        'Difficulty': 'Hard',
        'Language': 'English',
        'Tags': 'World News, Security, Politics',
        'Educational_Score': 6.0,
        'Safety': 'Mature',
        'Content_Type': 'News',
        'URL': 'https://timesofindia.indiatimes.com/world/pakistan/let-is-operatives-among-34-killed-in-khuzdar-attack-bla/articleshow/132378858.cms'
    }
]

new_df = pd.DataFrame(new_records)

# Combine datasets
df = pd.concat([df, new_df], ignore_index=True)

# Update grades to random values between 1 and 12 for every record
df['Grade'] = [random.randint(1, 12) for _ in range(len(df))]

# Save back to excel
df.to_excel(file_path, index=False)
print("Updated excel successfully with new records and random grades.")
