import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# -------- LOAD DATA --------
df = pd.read_csv("final_dataset.csv")

def clean_title(title):
    title = str(title).lower()
    title = re.sub(r'[^a-zA-Z ]', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title

df['Title'] = df['Title'].apply(clean_title) 

# -------- VECTORIZE --------
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df['text'])
def shorten_title(title):
    words = title.split()
    
    # Fix reversed words like "assistant human"
    if "human" in words and "assistant" in words:
        return "Human Resources Assistant"
    
    return " ".join(words[:5]).title()
# -------- FUNCTION --------
def predict_job_title(input_text, sector=None):
    
    # Filter by sector (IMPORTANT)
    if sector:
        df_filtered = df[df['sector'] == sector]
    else:
        df_filtered = df

    texts = df_filtered['text']
    
    # Transform input
    input_vec = vectorizer.transform([input_text])
    
    # Transform dataset
    dataset_vec = vectorizer.transform(texts)
    
    # Similarity
    similarity = cosine_similarity(input_vec, dataset_vec)
    
    # Get best match
    index = similarity.argmax()
    
    return shorten_title(df_filtered.iloc[index]['Title'])


if __name__ == "__main__":
    print(predict_job_title("Python developer with web experience", sector="IT"))
