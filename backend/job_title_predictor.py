import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

# 🔥 Global variables (lazy loading)
df = None
vectorizer = None


# -------- CLEAN FUNCTION --------
def clean_title(title):
    title = str(title).lower()
    title = re.sub(r'[^a-zA-Z ]', ' ', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title


# -------- SHORTEN TITLE --------
def shorten_title(title):
    words = title.split()

    # Fix reversed words
    if "human" in words and "assistant" in words:
        return "Human Resources Assistant"

    return " ".join(words[:5]).title()


# 🚀 LAZY LOAD FUNCTION (IMPORTANT)
def load_data():
    global df, vectorizer

    if df is None:
        print("🔄 Loading dataset...")

        df = pd.read_csv("final_dataset.csv")

        df['Title'] = df['Title'].apply(clean_title)

        vectorizer = TfidfVectorizer(max_features=5000)
        vectorizer.fit(df['text'])

        print("✅ Dataset loaded successfully")


# -------- MAIN FUNCTION --------
def predict_job_title(input_text, sector=None):
    try:
        load_data()  # 🔥 load only when needed

        # Filter by sector
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

    except Exception as e:
        print("ERROR:", e)
        return "Error"


# -------- TEST --------
if __name__ == "__main__":
    print(predict_job_title("Python developer with web experience", sector="IT"))